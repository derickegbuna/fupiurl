from django.shortcuts import render

# Create your views here.
from audioop import reverse
from datetime import datetime
from email import header
from gc import collect
import imp
from itertools import chain, count, tee
from logging import warning
from multiprocessing import context
import random
import string
from tabnanny import check
from textwrap import shorten
from typing import Counter
from unicodedata import name
from unittest import result
from urllib import request, response
from django.forms import URLField
from django.shortcuts import redirect,render,get_list_or_404,get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseNotFound, JsonResponse
import requests
from .models import RegisteredUser,UnregisteredUser,ShortenedURL, User_limit,Visitor,Userprofile,CustomizedURL,NormalURL,Landing_HIT
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib import messages
from django_user_agents.utils import get_user_agent
from django.core import serializers
import json
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re
from django.db.models import Sum,Count
from collections import defaultdict
from django.db import connection
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<FUNCTIONS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<FUNCTIONS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<FUNCTIONS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
characters=string.ascii_letters+string.digits
url='https://fupi.io/'
custom_prefix='https://fupi.io/'
size=5
max_norm=5
max_custom=5
# if we start with size 4,we have 14,776,336 possible links to generate and we have to check if generated links are still less than 14,776,336
# if we start with size 5,we have 916,132,832 possible links to generate and we have to check if generated links are still less than 916,132,832
# GENERATE OUTPUTURL
def randomFUNC(size,chars):
    result=''.join(random.choice(chars) for _ in range(size))
    return result
# TO CHECK IF THE INPUTURL IS VALID 
regex = re.compile(
    r'^(?:http|ftp)s?://' #http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' #...or ip
    r'(?::\d+)?' #optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
# TO ACCEPT WWW OR SOMETHING LIKE google.com AND ADD http:// 
def validateURL(url):
    url_form_field=URLField()
    try:
        url=url_form_field.clean(url)
    except ValidationError:
        return False
    return True
# TO CHECK IF THE LINK IS AVAILABLE ON THE INTERNET
def does_URL_exists(url):
    try:
        get=requests.get(url)
        if get.status_code==200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False
# Getting Visitor IP address note we have(HTTP_CLIENT_IP, HTTP_X_FORWARDED_FOR, HTTP_X_FORWARDED, HTTP_X_CLUSTER_CLIENT_IP, HTTP_FORWARDED_FOR, HTTP_FORWARDED, REMOTE_ADDR, HTTP_CF_CONNECTING_IP)
def get_ip(request):
    try:
        address=request.META.get('HTTP_X_FORWARDED_FOR')
        if address:
            ip=address.split(',')[-1].strip()
        else:
            ip=request.META.get('REMOTE_ADDR')
        return ip
    except:
        return ('ip could not be found')
def get_loc(ip):
    response=requests.get('https://geolocation-db.com/json/'+ip+'&position=true').json()
    location=response['country_name']
    state=response['state']
    city=response['city']
    return location,state,city
def deviceType(request):
    if get_user_agent(request).is_pc:
        device='Desktop'
    elif get_user_agent(request).is_mobile:
        device='Mobile'
    elif get_user_agent(request).is_tablet:
        device='Tablet'
    elif get_user_agent(request).is_bot:
        device='Bot'
    else:
        device='Others'
    return device

def userAGENT(request):
    deviceName=request.user_agent.device.family
    deviceOS=request.user_agent.os.family
    deviceOSversion=request.user_agent.os.version_string
    device_OS=deviceOS+' '+deviceOSversion
    browserName=request.user_agent.browser.family
    browserVersion=request.user_agent.browser.version_string
    browser=browserName+' '+browserVersion
    return deviceName,device_OS,browser

# TO CHECK NUMBERS OF URL(CUSTOM & NORM) CREATED BY USER TO SET MONTHLY LIMIT
def checklimit(request):
    ip=get_ip(request)
    t=datetime.today()
    if request.user.is_authenticated:
        _limit=ShortenedURL.objects.filter(user=request.user).filter(date__year=t.year,date__month=t.month)
    else:
        _limit=ShortenedURL.objects.filter(ip=ip).filter(date__year=t.year,date__month=t.month)
    c_limit=_limit.filter(type_of_url='Customized').count()
    n_limit=_limit.filter(type_of_url='Normal').count()
    numURL=User_limit.objects.filter(user=request.user)
    if numURL:
        numURL.update(url_count=_limit.count())
    else:
        User_limit.objects.create(user=request.user,ip=ip,url_count=_limit.count())
    return c_limit,n_limit

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<VIEWS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def error404(request):
    return render(request,'error404.html')
def URLRedirect(request,pk):
    uri=ShortenedURL.objects.filter(txID=pk).values('inputURL')
    ip=get_ip(request)
    # ip='82.131.33.249'#Estonia
    # ip='178.75.186.96' #Finland
    if uri:
        loc=get_loc(ip)
        location=loc[0]
        loc_state=loc[1]
        loc_city=loc[2]
        device_Type=deviceType(request)
        deviceName,device_OS,browser=userAGENT(request)
        for data in uri.values_list('user',flat=True):
            user=data
        for data in uri.values_list('inputURL',flat=True):
            inputURL=data
        for data in uri.values_list('outputURL',flat=True):
            outputURL=data
        for data in uri.values_list('hitcount',flat=True):
            hitcount=data+1
        for data in uri.values_list('type_of_url',flat=True):
            type_of_url=data
        Visitor.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=pk,user=user,inputURL=inputURL,outputURL=outputURL,type_of_url=type_of_url,type_of_device=device_Type,deviceName=deviceName,deviceOS=device_OS,browser=browser)
        uri.update(hitcount=hitcount)
        RegisteredUser.objects.filter(txID=pk).update(hitcount=hitcount)
        UnregisteredUser.objects.filter(txID=pk).update(hitcount=hitcount)
        return redirect(inputURL)
    else:
        location=get_loc(ip)
        msg='https://fupi.io/'
        context={'msg':f'{msg}{pk}'}
        return render(request,'error404.html',context)
def home(request):
    ip=get_ip(request)
    # ip='82.131.33.249'
    # ip='178.75.186.96' #Finland
    # ip='95.216.174.53' #Finland

    loc=get_loc(ip)
    location=loc[0]
    loc_state=loc[1]
    loc_city=loc[2]

    device_Type=deviceType(request)
    deviceName,device_OS,browser=userAGENT(request)

    hit=Landing_HIT.objects.filter(ip=ip)
    if hit.exists():
        count=hit.values_list('hit_count',flat=True)
        for count in count:
            hit=count
        hit_count=hit+1
        Landing_HIT.objects.filter(ip=ip).update(hit_count=hit_count)
    else:
        Landing_HIT.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,type_of_device=device_Type,deviceName=deviceName,deviceOS=device_OS,browser=browser)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # instead of user we gonna use IP as unique identifier
    clicks=Landing_HIT.objects.aggregate(Sum('hit_count'))
    clicks_hit=clicks['hit_count__sum']
    fupi_total_clicks=Visitor.objects.count()
    fupi_total_links=ShortenedURL.objects.count()
    fupi_total_visitors=fupi_total_links+clicks_hit
    # USERS GADGET PERCENTAGE
    userdeskTOP=ShortenedURL.objects.filter(type_of_device='Desktop').count()
    usertabLET=ShortenedURL.objects.filter(type_of_device='Tablet').count()
    usermobILE=ShortenedURL.objects.filter(type_of_device='Mobile').count()
    usertotal=userdeskTOP+usertabLET+usermobILE
    if usertotal == 0:
        usertotal=1
    userdeskTOP_Percent=str(round(100*userdeskTOP/usertotal))+'%'
    usertabLET_Percent=str(round(100*usertabLET/usertotal))+'%'
    usermobILE_Percent=str(round(100*usermobILE/usertotal))+'%'
    context={
        'total_clicks':fupi_total_clicks,
        'total_links_created':fupi_total_links,
        'total_visitors':fupi_total_visitors,
        'total_desktop':userdeskTOP_Percent,
        'total_tablet':usertabLET_Percent,
        'total_mobile':usermobILE_Percent,
    }
    return render(request,'home.html',context)
def signup(request):
    if request.user.is_authenticated:
        return redirect(profile)
    else:
        form=CreateUserForm
        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Account successfully created')
                return redirect(loginpage)
        context={'form':form,}
        return render(request,'signup.html',context)
def loginpage(request):
    if request.user.is_authenticated:
        return redirect(profile)
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect(profile)
            else:
                messages.info(request,'Username Or Password is incorrect')
                return render(request,'login.html')
        context={}
        return render(request,'login.html',context)
def shortener(request):
    num_of_short=checklimit(request)[1]
    # After checking limit if user has exceeded 
    # limit then send an error msg and suggest they suscribe 
    # so they can shorten and customize more link
    # ip='82.131.33.249'
    # ip='178.75.186.96' #Finland
    ip=get_ip(request)
    inputURL=request.POST.get('inputurl')
    txt=re.search("^fupi.io|http://fupi.io|https://fupi.io", inputURL, re.IGNORECASE)
    if not txt:
        if request.method=='POST' and num_of_short < max_norm:
            loc=get_loc(ip)
            location,loc_state,loc_city=loc
            type_of_url='Normal'
            device_Type=deviceType(request)
            device_Name,device_OS,browser=userAGENT(request)
            _url=randomFUNC(size,characters)
            if re.match(regex, inputURL) is not None:
                if does_URL_exists(inputURL):
                    while ShortenedURL.objects.filter(outputURL=_url).exists():
                        _url=randomFUNC(size,characters)
                        break
                    outputURL=url+_url
                    if request.user.is_authenticated:
                        user=request.user.username
                        userID=request.user
                        RegisteredUser.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=userID,inputURL=inputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser,type_of_url=type_of_url)
                        ShortenedURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=inputURL,outputURL=outputURL,type_of_url=type_of_url)
                        NormalURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=inputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser)
                    else:
                        user='anonymous'
                        UnregisteredUser.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=inputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser,type_of_url=type_of_url)
                        ShortenedURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=inputURL,outputURL=outputURL,type_of_url=type_of_url)
                        NormalURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=inputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser)
                    return JsonResponse(data={'result':outputURL,'inputURL':inputURL,'id':_url})
                else:
                    return JsonResponse(data={'result':'Invalid URL! This link you\'re trying to shorten can\'t be reached on the internet.','inputURL':inputURL,'id':0})                
            elif validateURL(inputURL):
                newinputURL='http://'+inputURL
                if does_URL_exists(newinputURL):
                    while ShortenedURL.objects.filter(outputURL=_url).exists():
                        _url=randomFUNC(size,characters)
                        break
                    outputURL=url+_url
                    if request.user.is_authenticated:
                        user=request.user.username
                        userID=request.user
                        RegisteredUser.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=userID,inputURL=newinputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser,type_of_url=type_of_url)
                        ShortenedURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=newinputURL,outputURL=outputURL,type_of_url=type_of_url)
                        NormalURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=newinputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser)
                    else:
                        user='anonymous'
                        UnregisteredUser.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=newinputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser,type_of_url=type_of_url)
                        ShortenedURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=newinputURL,outputURL=outputURL,type_of_url=type_of_url)
                        NormalURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=newinputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser)
                    return JsonResponse(data={'result':outputURL,'inputURL':newinputURL,'id':_url})
                else:
                    return JsonResponse(data={'result':'Invalid URL! This link you\'re trying to shorten can\'t be reached on the internet.','inputURL':newinputURL,'id':0})
            else:
                return JsonResponse(data={'result':'Invalid URL! This link you\'re trying to shorten is not valid.','inputURL':inputURL,'id':0})
        else:
            return JsonResponse(data={'result':'You have exceeded the number of url links you can shorten for this month.','inputURL':'Limit Exceeded!','id':0})
    else:
        return JsonResponse(data={'result':'This is already a fupi link.','inputURL':inputURL,'id':0})
# TO PREVENT UNSAFE AND RESERVED CHARACTERSS from being used for customization
def is_safe(uri):
    reserved=['&','$','+',',','/',':',':','=','?','@','#',' ','>','<','{','}','[',']','|','\\','^','%','~']
    empty=[e for e in uri if e in reserved]
    if not empty:
        return True
    else:
        return False
@login_required(login_url='login')
def customshortener(request): #For customize we can have symbols included
    no_of_custom=checklimit(request)[0]
    ip=get_ip(request)
    # ip='82.131.33.249'
    # ip='178.75.186.96' #Finland
    inputURL=request.POST.get('customizeinputURL')
    _url=request.POST.get('customizeoutputURL')
    checkuri=[]
    for i in _url:
        checkuri.append(i)
    txt=re.search("^fupi.io|http://fupi.io|https://fupi.io", inputURL, re.IGNORECASE)
    if not txt:
        # if request.method=='POST' and not inputURL and not _url:
        if no_of_custom < max_custom:
            if is_safe(checkuri):
                if request.user.is_authenticated and request.method=='POST' and inputURL and _url:
                    loc=get_loc(ip)
                    location,loc_state,loc_city=loc
                    user=request.user.username
                    userID=request.user
                    type_of_url='Customized'
                    device_Type=deviceType(request)
                    device_Name,device_OS,browser=userAGENT(request)
                    customURL=custom_prefix+_url
                    if re.match(regex, inputURL) is not None:
                        if does_URL_exists(inputURL):
                            if ShortenedURL.objects.filter(outputURL=customURL).exists():
                                validID=2
                                outputURL=' has already been taken. Try another?'
                                return JsonResponse(data={'ID':_url,'inputURL':inputURL,'outputURL':outputURL,'validID':validID})
                            else:
                                validID=1
                                outputURL=customURL
                                RegisteredUser.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=userID,inputURL=inputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser,type_of_url=type_of_url)
                                ShortenedURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=inputURL,outputURL=outputURL,type_of_url=type_of_url)
                                CustomizedURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=userID,inputURL=inputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser)
                            return JsonResponse(data={'ID':_url,'inputURL':inputURL,'outputURL':outputURL,'validID':validID})
                        else:
                            validID=0
                        return JsonResponse(data={'inputURL':inputURL,'outputURL':'Invalid URL! This link you\'re trying to customize can\'t be reached on the internet.','validID':validID})
                    elif validateURL(inputURL):
                        newinputURL='http://'+inputURL
                        if does_URL_exists(newinputURL):
                            if ShortenedURL.objects.filter(outputURL=customURL).exists():
                                validID=2
                                outputURL=' has already been taken. Try another?'
                                return JsonResponse(data={'ID':_url,'inputURL':newinputURL,'outputURL':outputURL,'validID':validID})
                            else:
                                validID=1
                                outputURL=customURL
                                RegisteredUser.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=userID,inputURL=newinputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser,type_of_url=type_of_url)
                                ShortenedURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=user,inputURL=newinputURL,outputURL=outputURL,type_of_url=type_of_url)
                                CustomizedURL.objects.create(ip=ip,location=location,loc_state=loc_state,loc_city=loc_city,txID=_url,user=userID,inputURL=newinputURL,outputURL=outputURL,type_of_device=device_Type,deviceName=device_Name,deviceOS=device_OS,browser=browser)
                            return JsonResponse(data={'ID':_url,'inputURL':newinputURL,'outputURL':outputURL,'validID':validID})
                        else:
                            validID=0
                            inputURL=newinputURL
                        return JsonResponse(data={'inputURL':inputURL,'outputURL':'Invalid URL! This link you\'re trying to customize can\'t be reached on the internet.','validID':validID})
                    else:
                        validID=0
                    return JsonResponse(data={'inputURL':inputURL,'outputURL':'Invalid URL! This link you\'re trying to customize is not valid.','validID':validID})
                else:
                    validID=0
                    inputURL='Error: Invalid Request!'
                return JsonResponse(data={'inputURL':inputURL,'outputURL':'Input field can not be empty','validID':validID})
            else:
                validID='inputERROR'
                msg='. - _'
                inputURL=f'A customized name can only contain the following symobls: '
            return JsonResponse(data={'inputURL':inputURL,'outputURL':'Invalid input error','validID':validID,'msg':msg})
        else:
            validID=0
            inputURL='You have exceeded the number of url links you can customize for this month.'
        return JsonResponse(data={'inputURL':inputURL,'outputURL':'Limit Exceeded!','validID':validID})
    else:
        validID=0
        return JsonResponse(data={'inputURL':inputURL,'outputURL':'This is already a fupi link.','validID':validID})
@login_required(login_url='login')
def profile(request):
    subscribed=Userprofile.objects.filter(user=request.user).values_list('subscribed',flat=True)
    subscription_plan=Userprofile.objects.filter(user=request.user).values_list('subscription_plan',flat=True)
    for sub in subscribed:
        subscribed=sub
    for plan in subscription_plan:
        plans=plan
    context={
        'plans':plans,'subscribed':subscribed,
        'customURL':custom_prefix
    }
    return render(request,'profile.html',context)
@login_required(login_url='login')
def tracklink(request):
    user=request.user.username
    total_visitors=Visitor.objects.filter(user=user).count()
    # GADGET PERCENTAGE
    deskTOP=Visitor.objects.filter(user=user).filter(type_of_device='Desktop').count()
    tabLET=Visitor.objects.filter(user=user).filter(type_of_device='Tablet').count()
    mobILE=Visitor.objects.filter(user=user).filter(type_of_device='Mobile').count()
    total=deskTOP+tabLET+mobILE
    if total==0:
        total=1
    desktop_Percent=str(round(100*deskTOP/total))+'%'
    tablet_Percent=str(round(100*tabLET/total))+'%'
    mobile_Percent=str(round(100*mobILE/total))+'%'
    subscribed=Userprofile.objects.filter(user=request.user).values_list('subscribed',flat=True)
    subscription_plan=Userprofile.objects.filter(user=request.user).values_list('subscription_plan',flat=True)
    for sub in subscribed:
        subscribed=sub
    for plan in subscription_plan:
        plans=plan
    click=RegisteredUser.objects.filter(user=request.user).aggregate(Sum('hitcount'))
    created=RegisteredUser.objects.filter(user=request.user).count()
    visit=Visitor.objects.filter(user=request.user).count()
    clicks=click['hitcount__sum']
    normal=RegisteredUser.objects.filter(user=request.user).filter(type_of_url='Normal')
    customized=RegisteredUser.objects.filter(user=request.user).filter(type_of_url='Customized')
    context={
        'empty':'No Shortened Links Available',
        'cempty':'No Customized Links Available',
        'data':normal,'cdata':customized,'total_links':created,
        'total_clicks':clicks,'total_visitors':visit,
        'plans':plans,'subscribed':subscribed,
        'totalVisitor':total_visitors,'desktop':desktop_Percent,
        'tablet':tablet_Percent,'mobile':mobile_Percent
    }
    return render(request,'tracklink.html',context)
@login_required(login_url='login')
def insights(request,pk):
    tx=get_object_or_404(RegisteredUser,id=pk)
    txid=tx.txID
    inurl=RegisteredUser.objects.filter(txID=txid).values_list('inputURL',flat=True)
    outurl=RegisteredUser.objects.filter(txID=txid).values_list('outputURL',flat=True)
    for _ in inurl:
        inputurl=_
    for _ in outurl:
        outputurl=_
    vis=Visitor.objects.filter(txID=txid)
    tot=vis.count()
    if tot==0:
        tot=1
    loclick=vis.values('location').annotate(clicks=Count('ip'),perc=Count('location')*100/tot)
    u_=vis.values('ip','location').annotate(clicks=Count('ip'))
    lc=[x['location'] for x in u_]
    a=dict(Counter(lc))
    loc=[]
    for j in set(lc):
        if j in a:
            c='location'
            u_v='visitor'
            egb={c:j,u_v:a[j]}
            loc.append(egb)    
    # THIS MERGE 2 QUERYSET TOGETHER (LOCLICK AND LOC) TOGETHER WHERE 'LOCATION ARE THE SAME
    d=defaultdict(dict)
    for loc in (loclick,loc):
        for elem in loc:
            d[elem['location']].update(elem)
    n_loc=d.values()
    # ************************DEVICE PERCENTAGE********************************
    dee=vis.values('location','type_of_device').annotate(count=Count('type_of_device'))
    tot=dee.aggregate(Sum('count'))
    device=dee.values('type_of_device').annotate(count=Count('type_of_device'))
    des=device.filter(type_of_device='Desktop').values_list('count',flat=True)
    ta=device.filter(type_of_device='Tablet').values_list('count',flat=True)
    mo=device.filter(type_of_device='Mobile').values_list('count',flat=True)
    total=tot['count__sum']
    if des:
        for i in des:
            desk=str(round(i*100/total))+'%'
    else:
        desk=str(0)+'%'
    if ta:
        for i in ta:
            tab=str(round(i*100/total))+'%'
    else:
        tab=str(0)+'%'
    if mo:
        for i in mo:
            mob=str(round(i*100/total))+'%'
    else:
        mob=str(0)+'%'
    context={
        'inputurl':inputurl,'outputurl':outputurl,
        'loc':a,'data':n_loc,'total':tot,
        'desktop':desk,'tablet':tab,'mobile':mob,
        'total':total,'id':pk,
    }
    return render(request,'insights.html',context)
@login_required(login_url='login')
def Visitors(request,pk):
    subscribed=Userprofile.objects.filter(user=request.user).values_list('subscribed',flat=True)
    subscription_plan=Userprofile.objects.filter(user=request.user).values_list('subscription_plan',flat=True)
    for sub in subscribed:
        subscribed=sub
    for plan in subscription_plan:
        plans=plan
    outurl=RegisteredUser.objects.filter(id=pk).values_list('outputURL',flat=True)
    inurl=RegisteredUser.objects.filter(id=pk).values_list('inputURL',flat=True)
    txid=RegisteredUser.objects.filter(id=pk).values_list('txID',flat=True)
    for url in inurl:
        inputurl=url
    for url in outurl:
        outputurl=url
    for txid in txid:
        data=Visitor.objects.filter(txID=txid)
    context={
        'data':data,
        'id':pk,
        'inputurl':inputurl,'outputurl':outputurl,
        'plans':plans,'subscribed':subscribed,
    }
    return render(request,'visitors.html',context)
def logoutuser(request):
    logout(request)
    return redirect(home)