from rest_framework import serializers

from inmueble_app.models import Inmueble, Company, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ['inmueble']


class InmuebleSerializer(serializers.ModelSerializer):
    len_address = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
<<<<<<< HEAD
    company_name = serializers.CharField(source='company.name', read_only=True)
    # company_data = CompanySerializer(read_only=True)
=======

>>>>>>> parent of 25b4be5 (primer deploy dajngo)
    def get_len_address(self, object):
        return len(object.address)

    class Meta:
        model = Inmueble
        fields = '__all__'

    def validate(self, data):
        if data['address'] == data['pais']:
            raise serializers.ValidationError('The address cannot be equal to the country')
        else:
            return data

    def validate_imagen(self, data):
        if len(data) <= 2:
            raise serializers.ValidationError('The url is too short')
        else:
            return data


class CompanySerializer(serializers.ModelSerializer):
    inmuebles = InmuebleSerializer(many=True, read_only=True)

    # inmuebles = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='inmueble-show'
    # )

    class Meta:
        model = Company
        fields = '__all__'

# def lenColumn(value):
#     if len(value) <= 2:
#         raise serializers.ValidationError('The address is too short')
#
#
# class InmuebleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     address = serializers.CharField(validators=[lenColumn])
#     pais = serializers.CharField()
#     description = serializers.CharField()
#     imagen = serializers.CharField()
#     active = serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Inmueble.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.address = validated_data.get('address', instance.address)
#         instance.pais = validated_data.get('pais', instance.pais)
#         instance.description = validated_data.get('description', instance.description)
#         instance.imagen = validated_data.get('imagen', instance.imagen)
#         instance.active = validated_data.get('active', instance.active)
#
#         instance.save()
#
#         return instance
#
#     def validate(self, data):
#         if data['address'] == data['pais']:
#             raise serializers.ValidationError('The address cannot be equal to the country')
#         else:
#             return data
#
#     def validate_imagen(self, data):
#         if len(data) <= 2:
#             raise serializers.ValidationError('The url is too short')
#         else:
#             return data
