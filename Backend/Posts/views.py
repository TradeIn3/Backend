from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post, SavedPost
from Profile.models import Profile
from .serializers import PostSerializer,PostSavedSerializer
from django.http import Http404
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
import datetime
import jwt
from django.conf import settings
from rest_framework import exceptions

class PostCreateView(APIView):
    serializer_class=PostSerializer
    # permission_classes = [IsAuthenticated]
    def post(self,request):
        post_serializer=PostSerializer(data=request.data)
        user=Profile.object.filter(user_id=request.data['author'])
        if(user.city=="" or user.district=="" or user.address=="" or user.pincode=="" or user.phone==""):
            return Response("please complete your details",status=status.HTTP_204_NO_CONTENT)
        if post_serializer.is_valid() and post_serializer.is_valid_form(request.data):
            post_serializer.save()
            data=post_serializer.data
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostEditView(APIView):
    serializer_class=PostSerializer
    # permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            user_data=Profile.objects.get(user_id=request.data['user_id'])
        except Profile.DoesNotExist:
            return Response("user doesn't exists",status=status.HTTP_204_NO_CONTENT)  
        try:
            post=Post.objects.get(author=request.data['user_id'],id=request.data['post_id'])   
        except Post.DoesNotExist:
             return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT) 

        post_update_serializer=PostSerializer(post,data=request.data)   


        if post_update_serializer.is_valid() and post_update_serializer.is_valid_form(request.data):
            post_update_serializer.save()
            data=post_serializer.data
            return Response(data,status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class PostDeleteView(APIView):
    serializer_class=PostSerializer
    def delete(self,request,post_id,user_id):
        try:
            user_data=Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response("user doesn't exists",status=status.HTTP_204_NO_CONTENT)  
        try:
            post=Post.objects.get(author=user_id,id=post_id)   
        except Post.DoesNotExist:
            return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT)

        try:
            Post.objects.filter(author=user_id,id=post_id).delete()
            return Response("post deleted successfully.",status=status.HTTP_200_OK)
        except:
            return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT)


class PostUserRetriveView(APIView):
    def get(self,request):
        authorization_header = request.headers.get('Authorization')
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired.')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing.')

        user = Profile.objects.filter(user_id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')

        posts=Post.objects.filter(author=payload['user_id'])
        data=[]
        for post in posts:
            temp={}
            save=SavedPost.objects.filter(post=post.id,user=payload['user_id'])
            temp['title']=post.title
            temp['description']=post.description
            temp['year']=post.year
            temp['id']=post.id
            temp['price']=post.id
            temp['category']=post.category
            temp['date']=post.date
            temp['time']=post.time
            temp['is_donate']=post.is_donate
            temp['is_saved']=(save!=None)
            data.append(temp)

        return Response(data,status=status.HTTP_200_OK)

class PostUserCityRetriveView(APIView):
    def get(self,request):
        authorization_header = request.headers.get('Authorization')
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired.')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing.')

        user = Profile.objects.filter(user_id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')
        city=Profile.objects.get(user_id=payload['user_id']).city
        users=Profile.objects.filter(city=city)
        data=[]
        for user in users:
            posts=Post.objects.filter(author=user.user_id)
            for post in posts:
                save=SavedPost.objects.filter(post=post.id,user=payload['user_id'])
                temp={}
                temp['title']=post.title
                temp['description']=post.description
                temp['year']=post.year
                temp['id']=post.id
                temp['price']=post.id
                temp['category']=post.category
                temp['date']=post.date
                temp['time']=post.time
                temp['is_donate']=post.is_donate
                temp['user_id']=user.user_id
                temp['first_name']=user.first_name
                temp['last_name']=user.last_name
                temp['address']=user.address
                temp['phone']=user.phone
                temp['pincode']=user.pincode
                temp['email']=user.email
                temp['city']=user.city
                temp['district']=user.district
                temp['is_owner']=(user.user_id==payload['user_id'])
                temp['is_saved']=(save!=None)
                data.append(temp)

        return Response(data,status=status.HTTP_200_OK)


class PostSavedView(APIView):
    serializer_class=PostSavedSerializer
    # permission_classes = [IsAuthenticated]
    def post(self,request,post_id,user_id):
        post_saved_serializer=PostSavedSerializer(data=request.data)
        try:
            user_data=Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response("user doesn't exists",status=status.HTTP_204_NO_CONTENT)  
        try:
            post=Post.objects.get(id=post_id)   
        except Post.DoesNotExist:
            return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT)
        if post_saved_serializer.is_valid() :
            post_saved_serializer.save()
            return Response("saved",status=status.HTTP_201_CREATED)
        return Response(post_saved_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
