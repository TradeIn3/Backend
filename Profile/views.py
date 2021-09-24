from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer, UserSerializer
from django.http import Http404
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
import datetime
import json
import jwt
from django.conf import settings
from rest_framework import exceptions
from Posts.models import Post



class UserProfileCreateView(APIView):
    serializer_class=ProfileSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        profile_data=Profile.objects.all()
        profile_serializer=ProfileSerializer(data=request.data)
        user=self.request.user
        user_data=Profile.objects.get(user_id=request.data['user_id'])
        if user_data:
            return Response("user already exits", status=status.HTTP_204_NO_CONTENT)
        if profile_serializer.is_valid() and profile_serializer.is_valid_form(request.data):
            profile_serializer.save()
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            return Response({
                                'user':profile_serializer.data,
                                'access_token': access_token,
                                'refresh_token':refresh_token
                            },status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class UsernameRetrieveView(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        user_data=Profile.objects.all();
        data=[]
        for user in user_data:
            temp={}
            temp['username']=user.user_id
            temp['first_name']=user.first_name
            temp['last_name']=user.last_name
            temp['address']=user.address
            temp['phone']=user.phone
            temp['pincode']=user.pincode
            temp['email']=user.email
            temp['city']=user.city
            temp['district']=user.district
            temp['image']=user.image
            data.append(temp)
        return Response(data,status=status.HTTP_200_OK)

class UserUpdateView(APIView):  
    serializer_class=ProfileUpdateSerializer
    permission_classes = [AllowAny]
    def put(self,request):
        try:
            user_data=Profile.objects.get(user_id=request.data['user_id'])
        except Profile.DoesNotExist:
            return Response("user doesn't exists",status=status.HTTP_404_NOT_FOUND)     

        profile_update_serializer=ProfileUpdateSerializer(user_data,data=request.data)   
        if profile_update_serializer.is_valid() and profile_update_serializer.is_valid_form(request.data):
            profile_update_serializer.save()
            return Response("updated successfully",status=status.HTTP_200_OK)
        return Response("Something went wrong !!", status=status.HTTP_400_BAD_REQUEST) 

class GetMyDetailsView(APIView):

    def get(self,request):
        authorization_header = request.headers.get('Authorization')
        if authorization_header == None:
            print("why?")
            raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired.')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing.')

        user = Profile.objects.get(user_id=payload['user_id'])
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')
        post_count=Post.objects.filter(user=payload['user_id'],is_donate=False,is_barter=False).count()
        donate_count=Post.objects.filter(user=payload['user_id'],is_donate=True,is_barter=False).count()
        barter_count=Post.objects.filter(user=payload['user_id'],is_donate=False,is_barter=True).count()
        print(user);
        temp={}
        temp['username']=user.user_id
        temp['first_name']=user.first_name
        temp['last_name']=user.last_name
        temp['address']=user.address
        temp['phone']=user.phone
        temp['pincode']=user.pincode
        temp['email']=user.email
        temp['city']=user.city
        temp['district']=user.district
        temp['image']=user.image
        temp['barter_count']=barter_count
        temp['post_count']=post_count
        temp['donate_count']=donate_count
        return Response(temp,status=status.HTTP_200_OK)    
       

class UserLoginView(APIView):
    serializer_class=UserSerializer
    permission_classes = [AllowAny]
    def post(self,request):
        username = request.data['user_id']
        password = request.data['password']
        if (username is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'username and password required')
        user = Profile.objects.filter(user_id=username,password=password).first()
        if(user is None):
            raise exceptions.AuthenticationFailed('Invalid username or password')
        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        return Response( {
            'access_token': access_token,
            'refresh_token': refresh_token,
        },status=status.HTTP_200_OK)

def ValidateUsername(username):
    if username=="" :
        return False
    if len(username) < 8 or len(username) > 30:
        return False
    if username[0].isnumeric():
        return False
    return True

class ChechUsernameView(APIView):
    permission_classes = [AllowAny]
    def get(self,request,username):
        if (ValidateUsername(username)==False):
            return Response("Invalid Username",status=status.HTTP_204_NO_CONTENT)
        
        user_data=Profile.objects.filter(user_id=username)

        if user_data:
            return Response("username already exists.",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Not found.", status=status.HTTP_200_OK)    
      



class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        refresh_token=request.data['refresh_token']
        if refresh_token is None:
            return Response('Authentication credentials were not provided.')
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            return Response('expired refresh token, please login again.',status=status.HTTP_400_BAD_REQUEST)

        user = Profile.objects.filter(user_id=payload.get('user_id')).first()
        if user is None:
            return Response("User doesn't exists.",status=status.HTTP_204_NO_CONTENT);

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        return Response({
                            'access_token': access_token,
                            'refresh_token':refresh_token
                        },status=status.HTTP_200_OK)





def generate_access_token(user):

    access_token_payload = {
        'token_type':'access',
        'user_id': user.user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow()
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'token_type':'refresh',
        'user_id': user.user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=14),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token
       