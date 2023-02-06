from blog.models import User, Post, Category, Tag, Comment
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from django.http.response import JsonResponse

class UserSerializer(serializers.ModelSerializer):
    token_details = serializers.SerializerMethodField('get_token_details')
    class Meta:
        model = User
        fields = ['email', 'phone_no', 'city', 'country','image','id','token_details']
    extra_kwargs = {
			'token_detail': {'read_only': True},
    }
    def get_token_details(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
        


class PostSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = Post

        fields = ['author','category','title','text','tag','created_date','published_date','image']   
    
        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id','name']     
         

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name']        

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    cpassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'cpassword', 'email')
        

    def validate(self, attrs):
        if attrs['password'] != attrs['cpassword']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
  
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


     