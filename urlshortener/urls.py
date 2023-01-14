
from django.urls import path
from . import views
urlpatterns=[
    path('<str:pk>/',views.URLRedirect,name='redirectURL'),
    path('',views.home,name='home'),
    path('?/=signup/',views.signup,name='signup'),
    path('?/=login/',views.loginpage,name='login'),
    path('?/=profile/',views.profile,name='profile'),
    path('?/=tracklink/',views.tracklink,name='tracklink'),
    path('?/=insights/<int:pk>',views.insights,name='insights'),
    path('?/=visitors/<int:pk>',views.Visitors,name='visitors'),
    path('?/=shortener/',views.shortener,name='shortener'),
    path('?/=custom/',views.customshortener,name='customize'),
    path('?/=error404',views.error404,name='error404'),
    path('?/=logout/',views.logoutuser,name='logout'),
]