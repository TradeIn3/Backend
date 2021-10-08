from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post, SavedPost, PostImage, PostQuestion, Order, Reserved
from Profile.models import Profile
from .serializers import PostSerializer,PostSavedSerializer,PostQuestionSerializer,OrderSerializer,ReservedSerializer
from django.http import Http404
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
import datetime
import jwt
from django.conf import settings
from rest_framework import exceptions
from datetime import date,datetime,timezone
import time
import razorpay
import os
import json

def timesince_calulate(date,time):
    timesince=""
    if(date.today()!=date):
            days=date.today() - date
            if days==1:
                timesince="{} day ago".format(date.today() - date)
            else:
                timesince="{} days ago".format(date.today() - date)
                    
    else:        
        if (datetime.now().hour != time.hour):
            hours=datetime.now().hour-time.hour
            if hours==1:
                timesince="{} hour ago".format(datetime.now().hour-time.hour)
            else:
                timesince="{} hours ago".format(datetime.now().hour-time.hour)
        else:
            minutes=datetime.now().minute-time.minute
            if minutes<=1:
                timesince="{} min ago".format(datetime.now().minute-time.minute)
            else:
                timesince="{} mins ago".format(datetime.now().minute-time.minute)
    return timesince

class PostCreateView(APIView):
    serializer_class=PostSerializer
    # permission_classes = [IsAuthenticated]
    def post(self,request):
        post_serializer=PostSerializer(data=request.data)
        user=Profile.object.filter(user_id=request.data['user'])
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
    def put(self,request,post_id):
        post_serializer=PostSerializer(data=request.data)
        try:
            user_data=Profile.objects.get(user_id=request.data['username'])
        except Profile.DoesNotExist:
            return Response("user doesn't exists",status=status.HTTP_204_NO_CONTENT)  
        try:
            post=Post.objects.get(author=request.data['username'],id=post_id)   
        except Post.DoesNotExist:
             return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT) 

        post_update_serializer=PostSerializer(post,data=request.data)   ;


        if post_update_serializer.is_valid() and post_update_serializer.is_valid_form(request.data):
            post_update_serializer.save()
            data=post_serializer.data
            return Response(data,status=status.HTTP_200_OK)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class PostDeleteView(APIView):
    serializer_class=PostSerializer
    permission_classes=[AllowAny]
    def delete(self,request):
        user_id=request.GET['username']
        post_id=request.GET['post_id']
        try:
            user_data=Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response("user doesn't exists",status=status.HTTP_204_NO_CONTENT)  
        try:
            post=Post.objects.get(user=user_id,id=post_id)   
        except Post.DoesNotExist:
            return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT)

        try:
            Post.objects.filter(user=user_id,id=post_id).delete()
            return Response("post deleted successfully.",status=status.HTTP_200_OK)
        except:
            return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT)

class PostUserRetriveView(APIView):
    permission_classes=[AllowAny]
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

        user = Profile.objects.filter(user_id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')

        posts=Post.objects.filter(user=payload['user_id'])
        data=[]
        for post in posts:
            temp={}
            post_images=[]
            questions=[]
            images=PostImage.objects.filter(post=post.id)
            for img in images:
                post_images.append(img.image)
            question=PostQuestion.objects.filter(post=post.id)
            for que in question:
                answered_timesince=""
                if(que.is_answered):
                    if(que.answered_date=="" or que.answered_time=="" or que.answer==""):
                        return Response("Invalid data",status=status.HTTP_400_BAD_REQUEST)
                    answered_timesince= timesince_calulate(que.answered_date,que.answered_time) 
                obj={}
                obj['id']=que.id
                obj['question']=que.question
                obj['timesince']=timesince_calulate(que.date,que.time)
                obj['user_id']=que.user.user_id
                obj['is_answered']=que.is_answered
                obj['answered_timesince']=answered_timesince
                obj['answer']=que.answer
                questions.append(obj)
            # 
            save=SavedPost.objects.filter(post=post.id,user=payload['user_id'])
            temp['title']=post.title
            temp['author']=post.author
            temp['description']=post.description
            temp['year']=post.year
            temp['id']=post.id
            temp['is_sold']=post.is_sold
            temp['price']=post.id
            temp['category']=post.category
            temp['timesince']=timesince_calulate(post.date,post.time)
            temp['is_donate']=post.is_donate
            temp['is_barter']=post.is_barter
            temp['is_saved']=(save!=None)
            temp['images']=post_images
            temp['questions']=questions
            data.append(temp) 
        return Response(data,status=status.HTTP_200_OK)

class PostRetriveView(APIView):
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
        # city=Profile.objects.get(user_id=payload['user_id']).district
        users=Profile.objects.all()
        sortby=request.GET['sortby']
        category=request.GET['category']
        donation=request.GET['donation']
        
        categories=['Furniture','Electronics & Appliances','Vehicles','Clothings','Handicrafts','Stationary','Pets','Beauty','miscellaneous']
        data=[]
        for user in users:
            post=None
            if category != "null":
                if category not in categories:
                    return Response("Invalid Category",status=status.HTTP_204_NO_CONTENT)
                posts=Post.objects.filter(user=user.user_id,category=category,is_sold=False)
            else:
                posts=Post.objects.filter(user=user.user_id,is_sold=False)    
            
            for post in posts:
                save=SavedPost.objects.filter(post=post.id,user=payload['user_id'])
                post_images=[]
                questions=[]
                images=PostImage.objects.filter(post=post.id)
                for img in images:
                    post_images.append(img.image)
                for que in questions:
                    answered_timesince=""
                    if(que.is_answered):
                        if(que.answered_date=="" or que.answered_time=="" or que.answer==""):
                            return Response("Invalid data",status=status.HTTP_400_BAD_REQUEST)
                        answered_timesince= timesince_calulate(que.answered_date,que.answered_time) 
                    obj={}
                    obj['id']=que.id
                    obj['question']=que.question
                    obj['timesince']=timesince_calulate(que.date,que.time)
                    obj['user_id']=que.user.user_id
                    obj['is_answered']=que.is_answered
                    obj['answered_timesince']=answered_timesince
                    obj['answer']=que.answer
                    questions.append(obj)
                temp={}
                temp['title']=post.title
                temp['description']=post.description
                temp['year']=post.year
                temp['id']=post.id
                temp['price']=post.id
                temp['category']=post.category
                temp['timesince']=timesince_calulate(post.date,post.time)
                temp['is_donate']=post.is_donate
                temp['user_id']=user.user_id
                temp['first_name']=user.first_name
                temp['last_name']=user.last_name
                temp['address']=user.address
                temp['phone']=user.phone
                temp['pincode']=user.pincode
                temp['email']=user.email
                temp['city']=user.city
                temp['is_sold']=post.is_sold
                temp['district']=user.district
                temp['is_owner']=(user.user_id==payload['user_id'])
                temp['is_saved']=(save!=None)
                temp['images']=post_images
                temp['questions']=questions
                data.append(temp)
        if category in categories:
            if sortby=="high":
                data.sort(key=lambda x:x.price,reverse=True)
            elif sortby=="low":
                data.sort(key=lambda x:x.price)
            else:
                data.sort(key=lambda x:x.id)

            if donation:
                tempdata=[]
                for x in data:
                    if x.is_donate:
                        tempdata.append(x)
                data=tempdata


        
        return Response(data,status=status.HTTP_200_OK)


class PostSavedView(APIView):
    serializer_class=PostSavedSerializer
    # permission_classes = [AllowAny]
    def post(self,request):
        post_id=request.GET['post_id']
        user_id=request.GET['user_id']
        verb=request.GET['verb']
        if verb=="save":
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
        elif verb=="unsave":
            try:
                user_data=Profile.objects.get(user_id=user_id)
            except Profile.DoesNotExist:
                return Response("user doesn't exists",status=status.HTTP_204_NO_CONTENT)  
            try:
                post=Post.objects.get(id=post_id)   
            except Post.DoesNotExist:
                return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT)
            try:
                post=SavedPost.objects.get(user=user_id,post=post_id)   
            except SavedPost.DoesNotExist:
                return Response("post is already unsaved",status=status.HTTP_204_NO_CONTENT)
            try:
                SavedPost.objects.filter(user=user_id,post=post_id).delete()
                return Response("unsaved.",status=status.HTTP_200_OK)
            except:
                return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT)

        else:
            return Response("incorrect verb",status=status.HTTP_204_NO_CONTENT)


class PostQuestionView(APIView):
    serializer_class=PostQuestionSerializer
    def post(self,request):
        post_question_serializer=PostQuestionSerializer(request.data)   
        try:
            user_data=Profile.objects.get(user_id=request.data['username'])
        except Profile.DoesNotExist:
            return Response("user doesn't exists",status=status.HTTP_204_NO_CONTENT) 
        try:
            post=Post.objects.get(id=request.data['post_id'])   
        except Post.DoesNotExist:
            return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT)
        if post_question_serializer.is_valid() :
            post_question_serializer.save()
            return Response("question created",status=status.HTTP_201_CREATED)
        return Response(post_question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        post_question_serializer=PostQuestionSerializer(request.data)   
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
        try:
            post=Post.objects.get(id=request.data['post_id'],user=payload['user_id'])   
        except Post.DoesNotExist:
            return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT)
        try:
            question=PostQuestion.objects.get(id=request.data['question_id'])   
        except PostQuestion.DoesNotExist:
            return Response("question doesn't exists",status=status.HTTP_204_NO_CONTENT)    

        if post_question_serializer.is_valid() :
                post_question_serializer.save()
                return Response("answered successfully",status=status.HTTP_201_CREATED)
        return Response(post_question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        post_question_serializer=PostQuestionSerializer(request.data)   
        try:
            user_data=Profile.objects.get(user_id=request.data['username'])
        except Profile.DoesNotExist:
            return Response("user doesn't exists",status=status.HTTP_204_NO_CONTENT) 
        try:
            post=Post.objects.get(id=request.data['post_id'])   
        except Post.DoesNotExist:
            return Response("post doesn't exists",status=status.HTTP_204_NO_CONTENT)
        try:
            question=PostQuestion.objects.get(id=request.data['question_id'],user=request.data['username'])   
        except PostQuestion.DoesNotExist:
            return Response("question doesn't exists",status=status.HTTP_204_NO_CONTENT)    
        if post_question_serializer.is_valid() :
            post_question_serializer.save()
            return Response("question created",status=status.HTTP_201_CREATED)
        return Response(post_question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# {
# "amount":1,
# "username":"Rohit@0301",
# "reserve_product":"1"
# }


class StartReservedPayment(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        # request.data is coming from frontend
        amount = request.data['amount']
        username = request.data['username']
        reserve_product = request.data['reserve_product']

        user = Profile.objects.get(user_id=username)
        post = Post.objects.get(id=reserve_product)

        if(user==None or post==None):
            return Response("Something went wrong")
        # setup razorpay client
        client = razorpay.Client(auth=(os.environ.get("RAZORPAY_PUBLIC_KEY"), os.environ.get("RAZORPAY_SECRET_KEY")))

        # create razorpay order
        payment = client.order.create({"amount": int(amount), 
                                    "currency": "INR", 
                                    "payment_capture": "1"})
        # we are saving an order with isReserved=False
        reserve = Reserved.objects.create(
                                    reserve_product=post,
                                    user=user,
                                    reserve_amount=amount, 
                                    reserve_payment_id=payment['id'])

        serializer = ReservedSerializer(reserve)

        """order response will be 
        {'id': 17, 
        'order_date': '23 January 2021 03:28 PM', 
        'order_product': '**product name from frontend**', 
        'order_amount': '**product amount from frontend**', 
        'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
        'isPaid': False}"""

        data = {
            "payment": payment,
            "order": serializer.data
        }
        return Response(data,status=status.HTTP_200_OK)


class HandleReservedPaymentSuccess(APIView):
    def post(self,request):
        res = json.loads(request.data["response"])

        """res will be:
        {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
        'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
        'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
        """

        ord_id = ""
        raz_pay_id = ""
        raz_signature = ""

        # res.keys() will give us list of keys in res
        for key in res.keys():
            if key == 'razorpay_order_id':
                ord_id = res[key]
            elif key == 'razorpay_payment_id':
                raz_pay_id = res[key]
            elif key == 'razorpay_signature':
                raz_signature = res[key]

        # get order by payment_id which we've created earlier with isPaid=False
        reserve = Reserved.objects.get(reserve_payment_id=ord_id)

        data = {
            'razorpay_order_id': ord_id,
            'razorpay_payment_id': raz_pay_id,
            'razorpay_signature': raz_signature
        }

        client = razorpay.Client(auth=(os.environ.get("RAZORPAY_PUBLIC_KEY"), os.environ.get("RAZORPAY_SECRET_KEY")))

        # checking if the transaction is valid or not if it is "valid" then check will return None
        check = client.utility.verify_payment_signature(data)

        if check is not None:
            return Response('Something went wrong',status=status.HTTP_400_BAD_REQUEST)

        # if payment is successful that means check is None then we will turn isPaid=True
        reserve.isReserved = True
        reserve.save()

     

        return Response("Successfull payment",status=status.HTTP_200_OK)


class StartProductPayment(APIView):
    def post(request):
        # request.data is coming from frontend
        amount = request.data['amount']
        username = request.data['username']
        order_product = request.data['order_product']

        user = Profile.objects.get(user_id=username)
        post = Post.objects.get(id=order_product, price=amount)
        reserve =Reserved.object.get(reserve_product=order_product)
        if(reserve):
            pass
        if(user==None or post==None):
            return Response("Something went wrong")
        # setup razorpay client
        client = razorpay.Client(auth=(os.environ.get("RAZORPAY_PUBLIC_KEY"), os.environ.get("RAZORPAY_SECRET_KEY")))

        # create razorpay order
        payment = client.order.create({"amount": int(amount), 
                                    "currency": "INR", 
                                    "payment_capture": "1"})

        # we are saving an order with isPaid=False
        order = Order.objects.create(order_product=post,
                                    user=user,
                                    order_amount=amount, 
                                    order_payment_id=payment['id'])

        serializer = OrderSerializer(order)

        """order response will be 
        {'id': 17, 
        'order_date': '23 January 2021 03:28 PM', 
        'order_product': '**product name from frontend**', 
        'order_amount': '**product amount from frontend**', 
        'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
        'isPaid': False}"""

        data = {
            "payment": payment,
            "order": serializer.data
        }
        return Response(data,status=status.HTTP_200_OK)



class HandleProductPaymentSuccess(APIView):
    def post(self,request):
        res = json.loads(request.data["response"])

        """res will be:
        {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
        'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
        'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
        """

        ord_id = ""
        raz_pay_id = ""
        raz_signature = ""

        # res.keys() will give us list of keys in res
        for key in res.keys():
            if key == 'razorpay_order_id':
                ord_id = res[key]
            elif key == 'razorpay_payment_id':
                raz_pay_id = res[key]
            elif key == 'razorpay_signature':
                raz_signature = res[key]

        # get order by payment_id which we've created earlier with isPaid=False
        order = Order.objects.get(order_payment_id=ord_id)

        data = {
            'razorpay_order_id': ord_id,
            'razorpay_payment_id': raz_pay_id,
            'razorpay_signature': raz_signature
        }

        client = razorpay.Client(auth=(os.environ.get("RAZORPAY_PUBLIC_KEY"), os.environ.get("RAZORPAY_SECRET_KEY")))

        # checking if the transaction is valid or not if it is "valid" then check will return None
        check = client.utility.verify_payment_signature(data)

        if check is not None:
            return Response('Something went wrong',status=status.HTTP_400_BAD_REQUEST)

        # if payment is successful that means check is None then we will turn isPaid=True
        order.isReserved = True
        order.save()

     

        return Response("Successfull payment",status=status.HTTP_200_OK)














# Product_categories = {
#     'Electronics':['Laptops','Power Banks','Pen drives & Storage','Tablets','Computer & Accessories','Headphones & earphones','Speakers','Camera & accessories','Gaming accessories'],
#     'Mobile':['Mobile','Mobile Accessories'],
#     'Appliances':['Televisions','Kitches Appliances','Air conditioners','Refrigerators','Washing machine','Microwaves','Chimneys','Dishwashers','Cooler'],
#     "Men's Fashion":['Clothing','Footware','Watches','Bags','Wallets','Luggage','Sunglasses','Accessories'],
#     "Women's Fashion":['Clothing','Footware','Watches','Fashion & Jewellery','Hanbags & clutches','Sunglasses'],
#     "Home":['kitchen & appliances','Furniture','Home Decor','Indoor Lighting','Art & Crafts','Garden & Outdoors'],
#     "Sports & Fitness":['Cycle','Exercies & Fitness','Sports accessories'],
#     "Baby Products":["Clothing","Footware","School bags","Toys and Games"],
#     "Vehicles":['Two wheelers & accessories','Four wheelers & accessories','others'],
#     "Others":['Stationary Products','Arts & Handicrafts','Beauty'],
# } 