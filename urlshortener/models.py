from django.db import models

# Create your models here.
from datetime import datetime
from email import header
import email
from email.policy import default
from itertools import count
from pickle import TRUE
from statistics import mode
from turtle import back
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import DateTimeField
from requests import request
SUBSCRIPTION_PLANS=(
    ('Free','Free'),
    ('Basic','Basic'),
    ('Premium','Premium'),
    ('Enterprise','Enterprise')
)
class Login_Session(models.Model):
    user=models.CharField(blank=True,null=True,max_length=150)
    ip=models.CharField(blank=True,null=True,max_length=25)
    type_of_device=models.CharField(blank=True,null=True,max_length=50)
    deviceName=models.CharField(blank=True,null=True,max_length=50)
    deviceOS=models.CharField(blank=True,null=True,max_length=50)
    browser=models.CharField(blank=True,null=True,max_length=50)
    location=models.CharField(blank=True,null=True,max_length=125)
    loc_state=models.CharField(blank=True,null=True,max_length=125)
    loc_city=models.CharField(blank=True,null=True,max_length=125)
    date=models.DateTimeField(auto_now_add=True)
class User_limit(models.Model):
    ip=models.CharField(blank=True,null=True,max_length=25)
    user=models.CharField(blank=True,null=True,max_length=150)
    url_count=models.IntegerField(default=0)
    last_update=models.DateTimeField(auto_now=True)
class UnregisteredUser(models.Model):
    ip=models.CharField(max_length=25,blank=True,null=True)
    txID=models.CharField(blank=True,null=True,max_length=100)
    user=models.CharField(blank=True,null=True,max_length=150)
    inputURL=models.CharField(blank=True,null=True,max_length=2048)
    outputURL=models.CharField(blank=True,null=True,max_length=25)
    hitcount=models.IntegerField(default=0)
    type_of_device=models.CharField(blank=True,null=True,max_length=10)
    deviceName=models.CharField(blank=True,null=True,max_length=50)
    deviceOS=models.CharField(blank=True,null=True,max_length=50)
    browser=models.CharField(blank=True,null=True,max_length=50)
    type_of_url=models.CharField(blank=True,null=True,max_length=13,default='Normal')
    location=models.CharField(blank=True,null=True,max_length=125)
    loc_state=models.CharField(blank=True,null=True,max_length=125)
    loc_city=models.CharField(blank=True,null=True,max_length=125)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('-date',)
class RegisteredUser(models.Model):
    ip=models.CharField(max_length=25,blank=True,null=True)
    txID=models.CharField(blank=True,null=True,max_length=100)
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    inputURL=models.CharField(blank=True,null=True,max_length=2048)
    outputURL=models.CharField(blank=True,null=True,max_length=2048)
    hitcount=models.IntegerField(default=0)
    type_of_device=models.CharField(blank=True,null=True,max_length=50)
    deviceName=models.CharField(blank=True,null=True,max_length=50)
    deviceOS=models.CharField(blank=True,null=True,max_length=50)
    browser=models.CharField(blank=True,null=True,max_length=50)
    type_of_url=models.CharField(blank=True,null=True,max_length=13)
    location=models.CharField(blank=True,null=True,max_length=125)
    loc_state=models.CharField(blank=True,null=True,max_length=125)
    loc_city=models.CharField(blank=True,null=True,max_length=125)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('-date',)
class Userprofile(models.Model):
    ip=models.CharField(max_length=25,blank=True,null=True)
    brand_name=models.CharField(blank=True,null=True,max_length=250)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    email=models.EmailField()
    subscribed=models.BooleanField(default=False)
    subscription_plan=models.CharField(blank=True,null=True,max_length=10,choices=SUBSCRIPTION_PLANS,default='Free')
    location=models.CharField(blank=True,null=True,max_length=125)
    loc_state=models.CharField(blank=True,null=True,max_length=125)
    loc_city=models.CharField(blank=True,null=True,max_length=125)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)
    class Meta:
        ordering=('-date',)
# SIGNAL FROM DJANGO DEFAULT CREATEUSER
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Userprofile.objects.create(user=instance,brand_name=instance.username,email=instance.email)
        print('New User Profile created!')
# post_save.connect(create_profile,sender=User)
@receiver(post_save,sender=User)
def update_profile(sender,instance,created,**kwargs):
    if created==False:
        instance.userprofile.save()
        print('Existing User Profile updated!')
# post_save.connect(update_profile,sender=User)
class ShortenedURL(models.Model):
    ip=models.CharField(max_length=25,blank=True,null=True)
    txID=models.CharField(blank=True,null=True,max_length=100)
    user=models.CharField(blank=True,null=True,max_length=250)
    inputURL=models.CharField(blank=True,null=True,max_length=2048)
    outputURL=models.CharField(blank=True,null=True,max_length=25)#WE SAVING ONLY THE PK
    hitcount=models.IntegerField(default=0)#Any time URLRedirect is hit,check the PK and increase count by 1
    type_of_device=models.CharField(blank=True,null=True,max_length=50)
    deviceName=models.CharField(blank=True,null=True,max_length=50)
    deviceOS=models.CharField(blank=True,null=True,max_length=50)
    browser=models.CharField(blank=True,null=True,max_length=50)
    type_of_url=models.CharField(blank=True,null=True,max_length=13)
    location=models.CharField(blank=True,null=True,max_length=125)
    loc_state=models.CharField(blank=True,null=True,max_length=125)
    loc_city=models.CharField(blank=True,null=True,max_length=125)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('-hitcount',)
class Visitor(models.Model):
    ip=models.CharField(max_length=25,blank=True,null=True)
    txID=models.CharField(blank=True,null=True,max_length=100)
    user=models.CharField(blank=True,null=True,max_length=250)
    inputURL=models.CharField(blank=True,null=True,max_length=2048)
    outputURL=models.CharField(blank=True,null=True,max_length=25)
    type_of_url=models.CharField(blank=True,null=True,max_length=13)
    type_of_device=models.CharField(blank=True,null=True,max_length=10)
    deviceName=models.CharField(blank=True,null=True,max_length=50)
    deviceOS=models.CharField(blank=True,null=True,max_length=50)
    browser=models.CharField(blank=True,null=True,max_length=50)
    location=models.CharField(blank=True,null=True,max_length=125)
    loc_state=models.CharField(blank=True,null=True,max_length=125)
    loc_city=models.CharField(blank=True,null=True,max_length=125)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('-date',)
class Landing_HIT(models.Model):
    ip=models.CharField(blank=True,null=True,max_length=25)
    type_of_device=models.CharField(blank=True,null=True,max_length=10)
    deviceName=models.CharField(blank=True,null=True,max_length=50)
    deviceOS=models.CharField(blank=True,null=True,max_length=50)
    browser=models.CharField(blank=True,null=True,max_length=50)
    hit_count=models.IntegerField(default=1)
    location=models.CharField(blank=True,null=True,max_length=125)
    loc_state=models.CharField(blank=True,null=True,max_length=125)
    loc_city=models.CharField(blank=True,null=True,max_length=125)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('-date',)
class CustomizedURL(models.Model):
    ip=models.CharField(max_length=25,blank=True,null=True)
    txID=models.CharField(blank=True,null=True,max_length=100)
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    inputURL=models.CharField(blank=True,null=True,max_length=2048)
    outputURL=models.CharField(blank=True,null=True,max_length=25)
    type_of_device=models.CharField(blank=True,null=True,max_length=10)
    deviceName=models.CharField(blank=True,null=True,max_length=50)
    deviceOS=models.CharField(blank=True,null=True,max_length=50)
    browser=models.CharField(blank=True,null=True,max_length=50)
    location=models.CharField(blank=True,null=True,max_length=125)
    loc_state=models.CharField(blank=True,null=True,max_length=125)
    loc_city=models.CharField(blank=True,null=True,max_length=125)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('-date',)
class NormalURL(models.Model):
    ip=models.CharField(max_length=25,blank=True,null=True)
    txID=models.CharField(blank=True,null=True,max_length=100)
    user=models.CharField(blank=True,null=True,max_length=250)
    inputURL=models.CharField(blank=True,null=True,max_length=2048)
    outputURL=models.CharField(blank=True,null=True,max_length=25)
    type_of_device=models.CharField(blank=True,null=True,max_length=10)
    deviceName=models.CharField(blank=True,null=True,max_length=50)
    deviceOS=models.CharField(blank=True,null=True,max_length=50)
    browser=models.CharField(blank=True,null=True,max_length=50)
    location=models.CharField(blank=True,null=True,max_length=125)
    loc_state=models.CharField(blank=True,null=True,max_length=125)
    loc_city=models.CharField(blank=True,null=True,max_length=125)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('-date',)
class InvalidREDIRECT(models.Model):
    ip=models.CharField(max_length=25,blank=True,null=True)
    txID=models.CharField(blank=True,null=True,max_length=100)
    uri=models.CharField(blank=True,null=True,max_length=2048)
    date=models.DateTimeField(auto_now_add=True)