# The `RegistrationSerializer` class in Django is used for serializing and validating user
# registration data, ensuring passwords match and checking for existing usernames and emails before
# saving the user.
from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        
    def save(self,):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        
        if User.objects.filter(username=user.username).exists():
            raise serializers.ValidationError("Username already exists")
        
        if User.objects.filter(email=user.email).exists():
            raise serializers.ValidationError("Email already exists")
        
        user.set_password(password)
        user.save()
        return user
