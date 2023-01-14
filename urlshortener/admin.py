from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomizedURL, NormalURL, UnregisteredUser,RegisteredUser, User_limit,Userprofile,ShortenedURL,Visitor,Landing_HIT
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
@admin.register(UnregisteredUser)
class UnregisteredUserAdmin(admin.ModelAdmin):
    list_display=('ip','location','loc_state','loc_city','txID','inputURL','outputURL','type_of_url','type_of_device','hitcount')
@admin.register(RegisteredUser)
class RegisteredUserAdmin(admin.ModelAdmin):
    list_display=('ip','location','loc_state','loc_city','txID','user','inputURL','outputURL','type_of_url','type_of_device','hitcount')
@admin.register(Userprofile)
class UserprofileAdmin(admin.ModelAdmin):
    list_display=('ip','location','loc_state','loc_city','brand_name','email')
@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display=('ip','location','loc_state','loc_city','txID','user','inputURL','outputURL','type_of_url','hitcount','browser','type_of_device')
@admin.register(CustomizedURL)
class CustomizedURLAdmin(admin.ModelAdmin):
    list_display=('ip','location','loc_state','loc_city','txID','user','inputURL','outputURL','type_of_device')
@admin.register(NormalURL)
class NormalURLAdmin(admin.ModelAdmin):
    list_display=('ip','location','loc_state','loc_city','txID','user','inputURL','outputURL','type_of_device')
@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display=('ip','location','loc_state','loc_city','txID','user','inputURL','outputURL','type_of_url','type_of_device','browser')
@admin.register(Landing_HIT)
class Landing_HITAdmin(admin.ModelAdmin):
    list_display=('ip','location','loc_state','loc_city','type_of_device','deviceName','deviceOS','browser','hit_count')
@admin.register(User_limit)
class User_limit(admin.ModelAdmin):
    list_display=('ip','user','url_count','last_update')