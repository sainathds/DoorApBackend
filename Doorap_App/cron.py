from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import traceback
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control
from datetime import date
import requests
import json
import ast
from django.http import HttpResponse



def Update_Status():
    try:
        current_date = date.today()
        
        offer = Offers.objects.all()
        for i in offer:
            
            if i.expirydate == current_date:
                Offers.objects.filter(id = i.id).update(offercode_status = "Expired")
        
    except:
        
        pass


