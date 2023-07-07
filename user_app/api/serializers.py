from rest_framework import serializers
from django.contrib.auth.models import User
<<<<<<< HEAD
# from user_app.models import Account
=======
>>>>>>> parent of 25b4be5 (primer deploy dajngo)

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only= True)

    class Meta:
        model = User
<<<<<<< HEAD
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone']
=======
        fields = ['username', 'email', 'password', 'password2']
>>>>>>> parent of 25b4be5 (primer deploy dajngo)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'Invalid password confirmation'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'This email already exists'})

<<<<<<< HEAD
        # account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account = User.objects.create_user(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            password=self.validated_data['password']
        )
        account.set_password = self.validated_data['password']
        account.phone = self.validated_data['phone']
=======
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(self.validated_data['password'])
>>>>>>> parent of 25b4be5 (primer deploy dajngo)
        account.save()

        return account