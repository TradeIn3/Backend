from rest_framework import serializers
from .models import Profile
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['user_id','password']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = ['image']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['user_id','first_name','last_name','email','password','city','district','address','pincode','phone','image']

    def is_valid_form(self,validate_data):
        self.ValidateUsername(validate_data['user_id'])
        self.ValidateFirstName(validate_data['first_name'])
        self.ValidateLastName(validate_data['last_name'])
        self.ValidateEmail(validate_data['email'])
        self.ValidatePassword(validate_data['password'])
        return True
    
    def ValidateUsername(self,username):
        if username=="" :
             raise serializers.ValidationError("Invalid username")
        if len(username) < 3 or len(username) > 30:
            raise serializers.ValidationError("username 3-30 characters are allowed")
        if username[0].isnumeric():
            raise serializers.ValidationError("can't start with a number")   
        pattern=re.compile(r"[A-Za-z0-9_@]+$")
        if re.fullmatch(pattern, username):
            return username
        else:
            raise serializers.ValidationError("Invalid username")

    def ValidateFirstName(self,name):
        if name=="" :
            raise serializers.ValidationError("Invalid firstname")
        if len(name) < 2 or len(name)>50:
            raise serializers.ValidationError("firstname 2-50 characters are allowed")
        pattern=re.compile(r"[A-Za-z]+$")
        if re.fullmatch(pattern, name):
            return name
        else:
            raise serializers.ValidationError("Invalid firstname")

    def ValidateLastName(self,name):
        if name=="" :
            raise serializers.ValidationError("Invalid lastname")
        if len(name) < 2 or len(name)>50:
            raise serializers.ValidationError("lastname 2-50 characters are allowed")
        pattern=re.compile(r"[A-Za-z]+$")
        if re.fullmatch(pattern, name):
            return name
        else:
            raise serializers.ValidationError("Invalid lastname")
    
    def ValidateEmail(self,email):  
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            return email
        else:
            raise serializers.ValidationError("Invalid email")


    def ValidatePassword(self,password):
        SpecialSym =['$', '@', '#', '%','!','^','*','+','-','/','-','_','.','?']
        val = True
          
        if len(password) < 8:
            raise serializers.ValidationError("weak password")        
              
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("weak password")    
              
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("weak password")    
              
        if not any(char.islower() for char in password):
            raise serializers.ValidationError("weak password")    
              
        if not any(char in SpecialSym for char in password):
            raise serializers.ValidationError("weak password")    
        
        return password

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['city','district','address','pincode','phone','first_name','last_name']

    def is_valid_form(self,validate_data):
        self.ValidatePincode(validate_data['pincode'])
        self.ValidatePhone(validate_data['phone'])
        self.ValidateCity(validate_data['city'])
        self.ValidateDistrict(validate_data['district'])
        self.ValidateFirstName(validate_data['first_name'])
        self.ValidateLastName(validate_data['last_name'])
        return True

    
    def ValidatePhone(self,phone):
        regex = r"^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
        if(re.fullmatch(regex, phone)):
            return phone
        else:
            raise serializers.ValidationError("Invalid phone")

    def ValidatePincode(self,pincode):
        regex = r'[0-9]+$'
        if len(pincode) != 6 and re.fullmatch(regex,pincode):
            raise serializers.ValidationError("Invalid pincode")
        return pincode

    def ValidateCity(self,city):
        regex=r'[a-zA-z]+$'
        if len(city)>2 and re.fullmatch(regex,city):
            return city
        else: 
            raise serializers.ValidationError("Invalid city")

    def ValidateDistrict(self,district):
        regex=r'[a-zA-z]+$'
        if len(district)>2 and re.fullmatch(regex,district):
            return district
        else: 
            raise serializers.ValidationError("Invalid district")        

    def ValidateFirstName(self,name):
        if name=="" :
            raise serializers.ValidationError("Invalid firstname")
        if len(name) < 2 or len(name)>50:
            raise serializers.ValidationError("firstname 2-50 characters are allowed")
        pattern=re.compile(r"[A-Za-z]+$")
        if re.fullmatch(pattern, name):
            return name
        else:
            raise serializers.ValidationError("Invalid firstname")

    def ValidateLastName(self,name):
        if name=="" :
            raise serializers.ValidationError("Invalid lastname")
        if len(name) < 2 or len(name)>50:
            raise serializers.ValidationError("lastname 2-50 characters are allowed")
        pattern=re.compile(r"[A-Za-z]+$")
        if re.fullmatch(pattern, name):
            return name
        else:
            raise serializers.ValidationError("Invalid lastname")
