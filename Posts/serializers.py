from rest_framework import serializers
from .models import Post, SavedPost, PostQuestion, Order, Reserve, PostImage
import re
class PostQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostQuestion
        fields=['id','post','user','question','is_answered','answer']

class PostSavedSerializer(serializers.ModelSerializer):
    class Meta:
        model=SavedPost
        fields=['post','user']
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostImage
        fields=['post','image']        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['id','title','description','genre','price','category','color','condition','subcategory','time','date','is_donate','is_barter','brand','author','user','is_sold']

    def is_valid_form(self,validate_data):
        print(validate_data)
        self.ValidatePrice(validate_data['price'],validate_data['is_barter'],validate_data['is_donate'])
        self.ValidateTitle(validate_data['title'])
        self.ValidateDescription(validate_data['description'])
        self.ValidateCategory(validate_data['category'])
        self.ValidateSubCategory(validate_data['subcategory'])
        self.ValidateBrand(validate_data['brand'])
        self.ValidateColor(validate_data['color'])
        self.ValidateCondition(validate_data['condition'])
        return True

    
    def ValidatePrice(self,price,is_barter,is_donate):
        if is_barter or is_donate:
            return price
        if price == "":
            raise serializers.ValidationError("Invalid price.")
        if int(price) <= 0 :
            raise serializers.ValidationError("Invalid price.")
        for char in str(price):
            if char<'0' and char>'9':
                raise serializers.ValidationError("Invalid price.")
        return price
    def ValidateCategory(self,category):
        if category == "":
            raise serializers.ValidationError("Invalid category.")
    def ValidateSubCategory(self,subcategory):
        if subcategory == "":
            raise serializers.ValidationError("Invalid subcategory.")       
    def ValidateBrand(self,brand):
        if brand == "":
            raise serializers.ValidationError("Invalid brand.")                
    def ValidateColor(self,color):
        if color == "":
            raise serializers.ValidationError("Invalid color.")  
    def ValidateCondition(self,condition):
        if condition == "":
            raise serializers.ValidationError("Invalid condition.")              
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
        model = Reserve
        fields = '__all__'
        depth = 2        