from django.db import models
from Profile.models import Profile
from datetime import datetime, timedelta

def current_year():
    return datetime.date.today().year
    
class Post(models.Model):
    title = models.CharField(max_length=100,null=False, blank=False,default="")
    author = models.CharField(max_length=100,null=False, blank=False,default="")
    brand = models.CharField(max_length=100,null=False, blank=False,default="")
    condition = models.CharField(max_length=50,null=False, blank=False,default="")
    description = models.CharField(max_length=250,null=False, blank=False,default="")
    color = models.CharField(max_length=100,null=False, blank=False,default="")
    genre = models.CharField(max_length=100,null=False, blank=False, default="")
    price=models.IntegerField(null=True,blank=True,default="")
    category=models.CharField(max_length=100,default="")
    subcategory=models.CharField(max_length=100,default="")
    time=models.TimeField(auto_now=True)
    date=models.DateField(auto_now=True)
    is_donate=models.BooleanField(default=False)
    is_sold=models.BooleanField(default=False)
    is_barter=models.BooleanField(default=False)
    is_premium=models.BooleanField(default=False)
    user= models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return '%s' % (self.id)


class SavedPost(models.Model):
    user=models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return '%s' %(self.id)


class PostImage(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)
    image=models.TextField(default="",null=True,blank=True)
    def __str__(self):
        return '%s' %(self.id)

class PostQuestion(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    question=models.TextField(default="",null=True,blank=True)
    # time=models.TimeField(auto_now=True)
    # date=models.DateField(auto_now=True)
    is_answered=models.BooleanField(default=False)
    # answered_date=models.DateField(null=True,blank=True,default="")
    # answered_time=models.TimeField(null=True,blank=True,default="")
    answer=models.TextField(default="",null=True,blank=True)
    def __str__(self):
        return '%s' %(self.id)


class Order(models.Model):
    order_product = models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s' % (self.order_payment_id)

class Reserve(models.Model):
    reserve_product = models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    reserve_amount = models.CharField(max_length=25)
    isReserved = models.BooleanField(default=False)
    reserve_date = models.DateTimeField(auto_now=True)
    expire_date = models.DateTimeField(default=datetime.now()+timedelta(days=2))
    reserve_payment_id = models.CharField(max_length=100)
    def __str__(self):
       return '%s' % (self.reserve_payment_id)
