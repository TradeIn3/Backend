from django.db import models
# Create your models here.

class Profile(models.Model):
    user_id=models.CharField(max_length=60,unique=True,null=False,primary_key=True)
    first_name = models.CharField(max_length=50,null=False, blank=False)
    last_name = models.CharField(max_length=50,null=False, blank=False)
    email = models.EmailField(max_length=100,null=False, blank=False,unique=True)
    password=models.CharField(max_length=50,null=False,blank=False)
    city=models.CharField(max_length=100,null=True,blank=True)
    district=models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    pincode=models.IntegerField(null=True,blank=True)
    phone=models.IntegerField(null=True,blank=True)
    image=models.TextField(default="",null=True,blank=True)
    coins=models.IntegerField(default="200",null=False)

    def __str__(self):
        return '%s' % (self.user_id)

    def is_authenticated(self):
        pass