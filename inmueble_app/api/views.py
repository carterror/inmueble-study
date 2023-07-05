from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from inmueble_app.api.permissions import IsAdminOrReadOnly, IsCommentUserOrReadOnly
from inmueble_app.api.serializers import InmuebleSerializer, CompanySerializer, CommentSerializer
from inmueble_app.models import Inmueble, Company, Comment
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from inmueble_app.api.throttling import CommentListThrottle, CommentCreateThrottle
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from inmueble_app.api.pagination import InmueblePagination


# Create your views here.

class UserComment(generics.ListAPIView):
    serializer_class = CommentSerializer

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     comments = Comment.objects.filter(user__username=username)
    #     return comments
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return username


class CommentList(generics.ListCreateAPIView):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    throttle_classes = [CommentListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__username', 'active']

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        # print(Comment.objects.filter(inmueble=pk))
        return Comment.objects.filter(inmueble=pk)


class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCommentUserOrReadOnly, IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'comment-detail'


class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    # permission_classes = [IsCommentUserOrReadOnly]
    # throttle_classes = [CommentCreateThrottle]

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        inmueble = Inmueble.objects.get(pk=pk)
        user = self.request.user
        comment = Comment.objects.filter(user=user, inmueble=inmueble)

        if comment.exists():
            raise ValidationError('Comment already exists for this user')

        if inmueble.num_califications == 0:
            inmueble.avg_califications = serializer.validated_data['qualification']
        else:
            inmueble.avg_califications = (serializer.validated_data['qualification'] + inmueble.avg_califications) / 2
            inmueble.num_califications = inmueble.num_califications + 1

        inmueble.save()

        serializer.save(inmueble=inmueble, user=user)


class InmuebleList(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer


class InmuebleDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer


class InmuebleListFilter(generics.ListAPIView):
    pagination_class = InmueblePagination
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company__name', 'active']


class CompanyView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


# class CompanyVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Company.objects.all()
#         serializer = CompanySerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk):
#         queryset = Company.objects.all()
#         inmueble = get_object_or_404(queryset, pk=pk)
#         serializer = CompanySerializer(inmueble)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = CompanySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def update(self, request, pk):
#         try:
#             company = Company.objects.get(pk=pk)
#         except Company.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         serializer = CompanySerializer(company, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request, pk):
#         try:
#             company = Company.objects.get(pk=pk)
#         except Company.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         company.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class CompanyDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

#
# class CommentGAV(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class CommentDetailGAV(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
# class CompanyAV(APIView):
#     def get(self, request):
#         companies = Company.objects.all()
#         serializer = CompanySerializer(companies, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         de_serializer = CompanySerializer(data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data)
#         else:
#             return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CompanyDetailAV(APIView):
#     def get(self, request, pk):
#         try:
#             company = Company.objects.get(pk=pk)
#             serializer = CompanySerializer(company, context={'request': request})
#             return Response(serializer.data)
#         except Company.DoesNotExist:
#             return Response(data={'Error': 'No such Company'}, status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, pk):
#         try:
#             company = Company.objects.get(pk=pk)
#         except Company.DoesNotExist:
#             return Response(data={'Error': 'No such Company'}, status=status.HTTP_404_NOT_FOUND)
#
#         de_serializer = CompanySerializer(company, data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data)
#         else:
#             return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         try:
#             company = Company.objects.get(pk=pk)
#         except Company.DoesNotExist:
#             return Response(data={'Error': 'No such Inmueble'}, status=status.HTTP_404_NOT_FOUND)
#
#         if company.delete():
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class InmuebleAV(APIView):
#     def get(self, request):
#         inmuebles = Inmueble.objects.all()
#         serializer = InmuebleSerializer(inmuebles, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         de_serializer = InmuebleSerializer(data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data)
#         else:
#             return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class InmuebleDetailAV(APIView):
#     def get(self, request, pk):
#         try:
#             inmueble = Inmueble.objects.get(pk=pk)
#             serializer = InmuebleSerializer(inmueble)
#             return Response(serializer.data)
#         except Inmueble.DoesNotExist:
#             return Response(data={'Error': 'No such Inmueble'}, status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, pk):
#         try:
#             inmueble = Inmueble.objects.get(pk=pk)
#         except Inmueble.DoesNotExist:
#             return Response(data={'Error': 'No such Inmueble'}, status=status.HTTP_404_NOT_FOUND)
#
#         de_serializer = InmuebleSerializer(inmueble, data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data)
#         else:
#             return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         try:
#             inmueble = Inmueble.objects.get(pk=pk)
#         except Inmueble.DoesNotExist:
#             return Response(data={'Error': 'No such Inmueble'}, status=status.HTTP_404_NOT_FOUND)
#
#         if inmueble.delete():
#             return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
# @api_view(['GET', 'POST'])
# def inmueble_list(request):
#     if request.method == 'GET':
#         inmuebles = Inmueble.objects.all()
#         serializer = InmuebleSerializer(inmuebles, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         de_serializer = InmuebleSerializer(data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data)
#         else:
#             return Response(de_serializer.errors)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def inmueble_show(request, pk):
#     try:
#         inmueble = Inmueble.objects.get(pk=pk)
#     except Inmueble.DoesNotExist:
#         return Response(data={'Error': 'No such Inmueble'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = InmuebleSerializer(inmueble)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         de_serializer = InmuebleSerializer(inmueble, data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data)
#         else:
#             return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         if inmueble.delete():
#             return Response(status=status.HTTP_204_NO_CONTENT)
