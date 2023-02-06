from blog.models import User, Post, Category, Tag, Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, PostSerializer, CategorySerializer, SignupSerializer, TagSerializer, CommentSerializer
from rest_framework import status 
from django.http.response import JsonResponse
from rest_framework import authentication, permissions
from rest_framework import status as tstatus
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class SignupApiView(APIView):
	" API for signup "

	permission_classes = [AllowAny]

	def post(self, request):
		
		res = {}
		try:
			email = request.data.get("email", None)
			password = request.data.get("password", None)
			cpassword = request.data.get("cpassword", None)
			username = request.data.get('username', None)

			if email is None:
				res['status'] = False
				res['message'] = "Email is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

			if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
				res['status'] = False
				res['message'] = "Account already exist with this Email"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

			if username is None:
				res['status'] = False
				res['message'] = "Name is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)	

			if password is None or password != cpassword:
				res['status'] = False
				res['message'] = "Password not Match!"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

			data = request.data
			try:
				data._mutable = True
			except:
				pass
			data['username'] = email
			data['status'] = 'Active'
			
			serializer =  SignupSerializer(
				data=data, context={'request': request})
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				res_data = serializer.data
				user = User.objects.filter(id=res_data['id']).last()
				user.set_password(password)
				user.save()

				res['status'] = True
				res['message'] = "You've registered successfully"
				res['data'] = res_data
				return Response(res, status=tstatus.HTTP_200_OK)
			else:
				res['status'] = False
				error = next(iter(serializer.errors))
				res['message'] = serializer.errors[str(error)][0]
				res['data'] = res_data
				return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
		return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
	" API for login "

	permission_classes = [AllowAny]

	def post(self, request):
		
		res = {}
		username = request.data.get("username", None)
		password = request.data.get("password", None)
		if username is None:
			res['status'] = False
			res['message'] = "Email is required"
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

		if password is None:
			res['status'] = False
			res['message'] = "Password is required"
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
		print(User.objects.filter(username=username).last())
		user = authenticate(username=username, password=password)
		if user is None:
			res['status'] = False
			res['message'] = "Invalid Email or Password!"
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
		
		serializer = UserSerializer(
			user, read_only=True, context={'request': request})
		if serializer is None:
			res['status'] = False
			res['message'] = "Invalid Email or Password!!"
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

		else:
			
			res['status'] = True
			res['message'] = "Authenticated successfully"
			res['data'] = serializer.data
			return Response(res, status=tstatus.HTTP_200_OK)

class UserDetail(APIView):
    
	
	permission_classes = [IsAuthenticated]
	def get(self, request):
		
		res = {}
		try:
			
			user = User.objects.filter(id=request.user.id).last()
			
			if user is None:
				res['status'] = False
				res['message'] = "User not found."
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			serializer = UserSerializer(
				user, read_only=True, context={'request': request})
			if serializer:
				res['status'] = True
				res['message'] = 'User detail fetched successfully'
				res['data'] = serializer.data
				return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)


class PostList(APIView):

	permission_classes = [IsAuthenticated]
	
	def get(self, request):
		if request.method == 'GET':
			posts = Post.objects.filter().all()
			
			serializer = PostSerializer(posts, many=True)
			return Response(serializer.data)
	

	def post(self, request):
		
			if request.method == 'POST':
			
				serializer = PostSerializer(data=request.data)
				if serializer.is_valid():
					serializer.save()
					return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
				return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

	def delete(self, request, pk):
		 if request.method == 'DELETE':
				posts = Post.objects.filter(pk=pk).all()
				posts.delete()
				return Response({'message': 'Post was deleted successfully!'},status=status.HTTP_204_NO_CONTENT)		

class PostDetail(APIView):

	permission_classes = [IsAuthenticated]
	
	def get(self, request, pk):
		if request.method == 'GET':
			posts = Post.objects.filter(pk=pk).all()
			
			serializer = PostSerializer(posts, many=True)
			return Response(serializer.data)

class CategoryListDetail(APIView):

	permission_classes = [IsAuthenticated]
	def get(self, request):
		if request.method == 'GET':
			category = Category.objects.filter().all()
			
			serializer = CategorySerializer(category, many=True)
			
			return Response(serializer.data)

class CategoryDetail(APIView):

	permission_classes = [IsAuthenticated]
	def get(self, request, pk):
		if request.method == 'GET':
			category = Category.objects.filter(pk=pk).all()
			
			serializer = CategorySerializer(category, many=True)
			
			return Response(serializer.data)

	def post(self, request):
		
			if request.method == 'POST':
			
				serializer = CategorySerializer(data=request.data)
				if serializer.is_valid():
					serializer.save()
					return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
				return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

	def delete(self, request, pk):
		if request.method == 'DELETE':
			category = Category.objects.filter(pk=pk).all()
			category.delete()
			return Response({'message': 'Category was deleted successfully'},status=status.HTTP_204_NO_CONTENT)			

class TagDetail(APIView):

	permission_classes = [IsAuthenticated]
	def get(self, request):
		if request.method == 'GET':
			tag = Tag.objects.filter().all()
			
			serializer = TagSerializer(tag, many=True)
			return Response(serializer.data)

	def post(self, request):
		
			if request.method == 'POST':
			
				serializer = TagSerializer(data=request.data)
				if serializer.is_valid():
					serializer.save()
					return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
				return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

	def delete(self, request, pk):
		if request.method == 'DELETE':
			tag = Tag.objects.filter(pk=pk).all()
			tag.delete()
			return Response({'message': 'Tag was delete successfully'}, status=status.HTTP_204_NO_CONTENT)			

class CommentDetail(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		if request.method == 'GET':
			comment = Comment.objects.filter().all()
			
			serializer = CommentSerializer(comment, many=True)
			return Response(serializer.data)

	def post(self, request):
		
			if request.method == 'POST':
			
				serializer = CommentSerializer(data=request.data)
				if serializer.is_valid():
					serializer.save()
					return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
				return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

	def delete(self, request, pk):
		if request.method == 'DELETE':
			tag = Comment.objects.filter(pk=pk).all()
			tag.delete()
			return Response({'message': 'Comment was delete successfully'}, status=status.HTTP_204_NO_CONTENT)	
		
	
# class PostDetails(APIView):
# 	permission_classes = [IsAuthenticated]
# 	def get(self, request):
# 		if request.method == 'GET':
			



	
