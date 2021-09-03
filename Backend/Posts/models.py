from django.db import models
from Profile.models import Profile
import datetime

def year_choices():
    return [(r,r) for r in range(1960, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year
class Post(models.Model):
    title = models.CharField(max_length=30,null=False, blank=False,default="")
    description = models.CharField(max_length=250,null=False, blank=False,default="")
    price=models.IntegerField(null=True,blank=True,default="")
    year = models.IntegerField(('year'), choices=year_choices(), default=current_year())
    image=models.ImageField(upload_to='static/profile',null=True,blank=True,default="")
    category=models.CharField(max_length=50,choices=(('Furniture','Furniture'),('Electronics & Appliances','Electronics & Appliances'),('Vehicles','Vehicles'),('Clothings','Clothings'),('Handicrafts','Handicrafts'),('Stationary','Stationary'),('Pets','Pets'),('Beauty','Beauty'),('miscellaneous','miscellaneous')),default="")
    time=models.TimeField(auto_now=True)
    date=models.DateField(auto_now=True)
    is_donate=models.BooleanField(default=False)
    author=models.ForeignKey(Profile, on_delete=models.CASCADE,default="")
    def __str__(self):
        return '%s' % (self.id)


class SavedPost(models.Model):
    user=models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return '%s %s' %(self.user.user_id,self.post.id)