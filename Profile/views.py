from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer, UserSerializer, ImageSerializer
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
from Posts.models import Post, SavedPost, PostImage, PostQuestion, Order, Reserve
import cloudinary.uploader
from django.utils import timezone
 

class UserProfileCreateView(APIView):
    serializer_class=ProfileSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        profile_data=Profile.objects.all()
        profile_serializer=ProfileSerializer(data=request.data)
        user_data=Profile.objects.filter(user_id=request.data['user_id']).first()
        if user_data:
            return Response("user already exits", status=status.HTTP_204_NO_CONTENT)
        if profile_serializer.is_valid() and profile_serializer.is_valid_form(request.data):
            profile_serializer.save()
            user = Profile.objects.get(user_id=request.data['user_id'])
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            return Response({
                                'user':profile_serializer.data,
                                'access_token': access_token,
                                'refresh_token':refresh_token
                            },status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class ChangeProfileImageView(APIView):
    serializer_class=ImageSerializer
    def put(self,request):
        authorization_header = request.headers.get('Authorization')
        print(authorization_header)
        if authorization_header == None:
            raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired.')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing.')

        user = Profile.objects.filter(user_id=payload['user_id']).first()
        if(user['image']):
             cloudinary.uploader.destroy(user['image'],invalidate=True)   
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')

        image = request.data['image']
        if image!="undefined" and  image!="null":
            upload_data = cloudinary.uploader.upload(image,folder="profile")
            print(upload_data)
            request.data['image']=upload_data['public_id']
        else :
            return Response("Invalid image",status=status.HTTP_204_NO_CONTENT)    

        image_serializer=ImageSerializer(user,data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            return Response(upload_data['public_id'],status=status.HTTP_200_OK)

        return Response("Bad Request",status=status.HTTP_400_BAD_REQUEST)    



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
            temp['coins']=user.coins
            data.append(temp)
        return Response(data,status=status.HTTP_200_OK)


class UserUpdateView(APIView):  
    serializer_class=ProfileUpdateSerializer
    def put(self,request):
        try:
            user_data=Profile.objects.get(user_id=request.data['user'])
        except Profile.DoesNotExist:
            return Response("user doesn't exists",status=status.HTTP_404_NOT_FOUND)     

        profile_update_serializer=ProfileUpdateSerializer(user_data,data=request.data)   
        if profile_update_serializer.is_valid() and profile_update_serializer.is_valid_form(request.data):
            profile_update_serializer.save()
            return Response(profile_update_serializer.data,status=status.HTTP_200_OK)
        return Response(profile_update_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class GetMyDetailsView(APIView):
    def get(self,request):
        authorization_header = request.headers.get('Authorization')
        if authorization_header == None:
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
        temp['coins']=user.coins
        temp['barter_count']=barter_count
        temp['post_count']=post_count
        temp['donate_count']=donate_count
        return Response(temp,status=status.HTTP_200_OK)    

class GetUserDetailsView(APIView):
    def get(self,request):
        try:
            user = Profile.objects.get(user_id=request.GET['user'])
        except:
            return Response("User not found",status=status.HTTP_204_NO_CONTENT)    
            
        post_count=Post.objects.filter(user=request.GET['user'],is_donate=False,is_barter=False).count()
        donate_count=Post.objects.filter(user=request.GET['user'],is_donate=True,is_barter=False).count()
        barter_count=Post.objects.filter(user=request.GET['user'],is_donate=False,is_barter=True).count()
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
        temp['coins']=user.coins
        return Response(temp,status=status.HTTP_200_OK)   

class ProfileBuyView(APIView):
    def get(self,request):
        user = Profile.objects.filter(user_id=request.GET['user']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')
        data =[]
        try:
            posts = Post.objects.filter(user=user.user_id,is_donate=False,is_barter=False)
            for post in posts:
                temp = {} 
                post_images=[]
                images=PostImage.objects.filter(post=post.id)
                for img in images:
                    post_images.append(img.image)
                temp['title']=post.title
                temp['id']=post.id
                temp['price']=post.price
                temp['brand']=post.brand
                temp['is_donate'] = post.is_donate
                temp['is_barter'] = post.is_barter
                temp['image']=post_images[0]
                data.append(temp)
        except:    
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)    

        return Response(data,status=status.HTTP_200_OK)

class ProfileDonateView(APIView):
    def get(self,request):

        user = Profile.objects.filter(user_id=request.GET['user']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')

        data =[]
        try:
            posts = Post.objects.filter(user=user.user_id,is_donate=True,is_barter=False)
            for post in posts:
                temp = {} 
                post_images=[]
                images=PostImage.objects.filter(post=post.id)
                for img in images:
                    post_images.append(img.image)
                temp['title']=post.title
                temp['id']=post.id
                temp['price']=post.price
                temp['brand']=post.brand
                temp['is_donate'] = post.is_donate
                temp['is_barter'] = post.is_barter
                temp['image']=post_images[0]
                data.append(temp)
        except:    
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)    

        return Response(data,status=status.HTTP_200_OK)   

class ProfileExchangeView(APIView):
    def get(self,request):

        user = Profile.objects.filter(user_id=request.GET['user']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')

        data =[]
        try:
            posts = Post.objects.filter(user=user.user_id,is_donate=False,is_barter=True)
            for post in posts:
                temp = {} 
                post_images=[]
                images=PostImage.objects.filter(post=post.id)
                for img in images:
                    post_images.append(img.image)
                temp['title']=post.title
                temp['id']=post.id
                temp['price']=post.price
                temp['brand']=post.brand
                temp['is_donate'] = post.is_donate
                temp['is_barter'] = post.is_barter
                temp['image']=post_images[0]
                data.append(temp)
        except:    
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)    

        return Response(data,status=status.HTTP_200_OK)

class ProfileOrdersView(APIView):
    def get(self,request):

        user = Profile.objects.filter(user_id=request.GET['user']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')
        try:
            order = Order.objects.filter(user=user)
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)    

        data = []
        for s in order:
            temp = {}
            try:
                post = Post.objects.get(id=s.order_product.id)
                post_images=[]
                images=PostImage.objects.filter(post=post.id)
                for img in images:
                    post_images.append(img.image)
                x = s.order_date.date()    
                temp['title']=post.title
                temp['order_id']=s.order_payment_id
                temp['order_date']=x.strftime("%B %d, %Y")
                temp['user_address']=user.address
                temp['user_phone']=user.phone
                temp['user_city']=user.city
                temp['user_pincode']=user.pincode
                temp['user_name']=user.first_name+" "+user.last_name
                temp['total_amount']=post.price+15
                temp['id']=post.id
                temp['price']=post.price
                temp['brand']=post.brand
                temp['is_donate'] = post.is_donate
                temp['is_barter'] = post.is_barter
                temp['image']=post_images[0]
                data.append(temp)
            except:    
                return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)    

        return Response(data,status=status.HTTP_200_OK)

class ProfileReserveView(APIView):
    def get(self,request):
        user = Profile.objects.filter(user_id=request.GET['user']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')
        try:
            reserve = Reserve.objects.filter(user=user)
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)    

        data = []
        for s in reserve:
            if s.expire_date < timezone.now():
                continue
            temp = {}
            # try:
            post = Post.objects.get(id=s.reserve_product.id)
            post_images=[]
            images=PostImage.objects.filter(post=post.id)
            for img in images:
                post_images.append(img.image)
            x = s.expire_date.date()    
            y= s.expire_date.time()
            temp['title']=post.title
            temp['reserve_id']=s.reserve_payment_id
            temp['expire_date']=x.strftime("%B %d, %Y")
            temp['expire_time']="{:d}:{:02d}".format(y.hour,y.minute)
            temp['id']=post.id
            temp['price']=s.reserve_amount
            # temp['brand']=post.brand
            # temp['is_donate'] = post.is_donate
            # temp['is_barter'] = post.is_barter
            temp['image']=post_images[0]
            data.append(temp)
            # except:    
            #     return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)    

        return Response(data,status=status.HTTP_200_OK)        

class ProfileWishlistView(APIView):
    def get(self,request):
       
        user = Profile.objects.filter(user_id=request.GET['user']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')

        try:
            saved = SavedPost.objects.filter(user=user)
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)    

        
        data = []
        for s in saved:
            temp = {}
            try:
                post = Post.objects.get(id=s.post.id)
                post_images=[]
                images=PostImage.objects.filter(post=post.id)
                for img in images:
                    post_images.append(img.image)
                temp['title']=post.title
                temp['id']=post.id
                temp['price']=post.price
                temp['brand']=post.brand
                temp['is_donate'] = post.is_donate
                temp['is_barter'] = post.is_barter
                temp['image']=post_images[0]
                data.append(temp)
            except:    
                return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)    

        return Response(data,status=status.HTTP_200_OK)



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
        # if (ValidateUsername(username)==False):
        #     return Response("Invalid Username",status=status.HTTP_20)
        
        user_data=Profile.objects.filter(user_id=username).first()
        print(user_data,username)
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
       