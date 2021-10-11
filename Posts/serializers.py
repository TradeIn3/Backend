from rest_framework import serializers
from .models import Post, SavedPost, PostQuestion, Order, Reserved
import re
class PostQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostQuestion
        fields=['id','post','user','question','time','date','is_answered','answered_date','answered_time','answer']

class PostSavedSerializer(serializers.ModelSerializer):
    class Meta:
        model=SavedPost
        fields=['post','user']
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['id','title','description','price','year','category','time','date','image','is_donate','is_donate','brand','author','user','is_sold']

    def is_valid_form(self,validate_data):
        self.ValidatePrice(validate_data['price'])
        self.ValidateTitle(validate_data['title'])
        self.ValidateDescription(validate_data['description'])
        return True

    
    def ValidatePrice(self,price):
        if price == "":
            raise serializers.ValidationError("Invalid price.")
        if int(price) <= 0 :
            raise serializers.ValidationError("Invalid price.")
        for char in price:
            if char<'0' and char>'9':
                raise serializers.ValidationError("Invalid price.")
        return price
        
            

    def ValidateTitle(self,title):
        if title=="":
            raise serializers.ValidationError("Invalid title")
        if len(title)>2 and len(title)<=100:
            return title
        else: 
            raise serializers.ValidationError("2-100 characters only")

    def ValidateDescription(self,description):
        if description=="":
             raise serializers.ValidationError("Invalid description")
        if len(description)>5 and len(description)<=250:
            return description
        else: 
            raise serializers.ValidationError("5-250 characters only")        



class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Order
        fields = '__all__'
        depth = 2

class ReservedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserved
        fields = '__all__'
        depth = 2        