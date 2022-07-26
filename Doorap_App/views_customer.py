import random
import string
import traceback
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
import json
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
# from .customAuthentication import CustAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import *
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
import calendar
from django.conf import settings
from django.core.mail import send_mail
import random
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import types
from six import text_type
from django.contrib.auth import authenticate
from django.db.models.expressions import RawSQL
from datetime import datetime
from datetime import timedelta
import time
from dateutil import parser
from django.db.models import Q
import stripe
#*************************************************************************** START CUSTOMER APP API  *****************************************************************

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Banner(request):
    try:
        banner = BannerMaster.objects.all().order_by('-id').values()
        # serializer = BannerMasterSerializers(BannerMaster.objects.all(),many=True)
        
        return Response({'status':200,'msg':'Banner List','payload':list(banner)})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_location_wise_vendor(request):
    try:
        data = request.data
        category_id = data.get('category_id',None)
        lat = data.get('lat',None)
        lng = data.get('lng',None)
        customer_id = data.get('customer_id',None)
        
        customer_obj = MyUser.objects.get( id = customer_id)
        distance = 10
        vendor_list = []
        
        query = 'SELECT t.id, (6371  * acos (cos ( radians(%f) )* cos( radians(t.google_address_lat))* cos( radians(t.google_address_lng) - radians(%f)) + sin ( radians(%f))* sin( radians(t.google_address_lat)))) AS distance FROM Doorap_DB.Doorap_App_vendordetails t HAVING distance < %d' %(float(lat),float(lng),float(lat),distance)   #raw query
        
        
        result = VendorDetails.objects.raw(query)
        
        [vendor_list.append(vendor.id) for vendor in result]
        
        vendor_obj = VendorDetails.objects.filter(id__in = vendor_list ,is_available = True)
        print(vendor_obj)
        category_obj = CategoryMaster.objects.get( id = category_id)
        
        temp_list = []
        for i in vendor_obj:
            
            data = VenderServices.objects.filter(fk_category = category_obj ,fk_vendor = i).values('fk_vendor__id','fk_vendor__full_name','fk_vendor__profile_image','fk_category__category_name').distinct()
            
            like_dislike = LikeDislike.objects.filter( fk_vendor = i , fk_customer = customer_obj )
            
            if data.exists():
                
                for i in data:
                    rating = ReviewsandFeedback.objects.filter(fk_vendor__id = i['fk_vendor__id']).values('rating')
                    count = ReviewsandFeedback.objects.filter(fk_vendor__id = i['fk_vendor__id']).count()
                    total_rateing = 0
                    for k in rating:
                        total_rateing = total_rateing + k['rating']
                    
                    if total_rateing == 0 and count == 0:
                        i['rating'] = 0.0
                    else:
                        i['rating'] = total_rateing / count
                    if like_dislike.exists():
                        for j in like_dislike: 
                            i['like_dislike'] = j.like_dislike
                            print(j.like_dislike)
                    else:
                        i['like_dislike'] = False
                temp_list.append(data[0]) 
        
        if len(temp_list) < 0:
            return Response({'status':403,'msg':'Vendor not found.'})
        else:  
            return Response({'status':200,'msg':'Vendor List.','payload':temp_list})     
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
 
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def show_vendor_by_category(request):
    try:
        data = request.data
        category_id = data.get('category_id',None)
        category_obj = CategoryMaster.objects.get(id = category_id)
        data = VenderServices.objects.filter( fk_category = category_obj).values('fk_category','fk_vendor__id','fk_vendor__full_name','fk_vendor__profile_image').distinct()
        if data.exists():
            return Response({'status':200,'msg':'Vendor List by Category.','payload':data})
        else:
            return Response({'status':403,'msg':'Vendor not found.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
        
        
        
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_All_Services(request):
    try:
        data = request.data
        search = data.get('search',None)
        print(search)
        if search:
            print("-------search")
            data = ServiceMaster.objects.filter(service_name__icontains = search).values('id','service_name','service_image','fk_category','fk_category__category_name',).order_by('service_name') 
            if data.exists():
                return Response({'status':200,'msg':'Search Data.','payload':list(data)})                        
            else:
                return Response({'status':200,'msg':'Services not found.','payload':list(data)})    
        else:
            print("--------by default")
            data = ServiceMaster.objects.all().values('id','service_name','service_image','fk_category','fk_category__category_name').order_by('service_name')
            
            return Response({'status':200,'msg':'Services List.','payload':list(data)})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
        

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Vendor_by_Services(request):
    try:
        data = request.data
        service_id = data.get('service_id',None)
        service_obj = ServiceMaster.objects.get(id = service_id)
        
        vendor_data = VenderServices.objects.filter(fk_service = service_obj).values('fk_vendor__id','fk_vendor__full_name','fk_vendor__profile_image','rating').order_by('fk_vendor__full_name')
        if vendor_data.exists():
            temp_dict = {}
            temp_dict['service_name'] = service_obj.service_name,
            temp_dict['vendor_data'] = vendor_data
            
            return Response({'status':200,'msg':'Vendor List.','payload':temp_dict})
        else:
            return Response({'status':200,'msg':'Vendor not found.','payload':vendor_data})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
        


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Vendor_profile(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        category_id = data.get('category_id',None)
        
        data = VenderServices.objects.filter(fk_vendor__id = vendor_id , fk_category__id = category_id).values('fk_vendor__id','fk_vendor__full_name','fk_category__id','fk_category__category_name','fk_vendor__abount_me','fk_vendor__profile_image','fk_vendor__business_name').distinct()
        
        reviews = ReviewsandFeedback.objects.filter(fk_vendor__id = vendor_id).order_by('-id').values('fk_orderdetails__fk_category__category_name','feedback','review_date','rating')
        
        
        rating = ReviewsandFeedback.objects.filter(fk_vendor__id = data[0]['fk_vendor__id']).values('rating')
        count = ReviewsandFeedback.objects.filter(fk_vendor__id = data[0]['fk_vendor__id']).count()
        total_rateing = 0
        
        for k in rating:
            total_rateing = total_rateing + k['rating']
        
        if total_rateing == 0 and count == 0:
            for i in data:
                i['rating'] = 0.0
                i['average_count' ] = str(count)
        else:
            for i in data:
                i['rating'] = total_rateing / count
                i['average_count' ] = str(count)
            
        # review_list = []
        # review_and_feedback1 = {
            # "service_name":"Tap Repair",
            # "feedback":"Very talented. Completed task according to specification.",
            # "total_price":1480,
            # "price_per_hour":45.00,
            # "date":"May 2022 - Jun 2022",
            # "hour":39
            # }
        # review_and_feedback2 = {
        # "service_name":"Tap Repair",
        # "feedback":"Very talented. Completed task according to specification.",
        # "total_price":1480,
        # "price_per_hour":45.00,
        # "date":"May 2022 - Jun 2022",
        # "hour":39
        # }
        # review_list.append(review_and_feedback1)
        # review_list.append(review_and_feedback2)
        if data.exists():
            temp_dict = {}
            temp_dict['vendor_profile'] = data
            temp_dict['review_and_feedback'] = reviews
            return Response({'status':200,'msg':'Vendor Profile.','payload':temp_dict})
        else:
            return Response({'status':200,'msg':'Vendor profile not found'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})




@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Services_list_by_vendor(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        category_id = data.get('category_id',None)
        
        vendor_obj = VendorDetails.objects.get( id = vendor_id)
        category_obj = CategoryMaster.objects.get( id = category_id)
        
        vender_data = VenderServices.objects.filter(fk_vendor = vendor_obj , fk_category = category_obj).values('fk_category__id','fk_category__category_name','fk_vendor__id','fk_vendor__full_name','fk_vendor__profile_image').distinct()
        temp_dict = {}
        
        temp_dict['vender_data'] = vender_data
        
        
        service_list = VenderServices.objects.filter(fk_vendor = vendor_obj, fk_category = category_obj).values('id','fk_service__id','fk_service__service_name','fk_service__service_image')
        
        if service_list.exists():
            temp_dict['service_data'] = service_list
            print(temp_dict)
            return Response({'status':200,'msg':'Vendor Services.','payload':temp_dict})
        else:
            return Response({'status':403,'msg':'Vendor Services not found.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Vendor_Facility(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        category_id = data.get('category_id',None)
        service_id = data.get('service_id',None)
        vender_service_id = data.get('vender_service_id',None)
        
        vendor_obj = VendorDetails.objects.get(id = vendor_id)
        category_obj = CategoryMaster.objects.get(id = category_id)
        service_obj = ServiceMaster.objects.get(id = service_id)
        vender_service_obj = VenderServices.objects.get(id = vender_service_id)
        
        
        temp_dict = {}
        service_data = VenderServices.objects.filter(fk_vendor = vendor_obj , fk_category = category_obj , fk_service = service_obj).values('id','fk_vendor','fk_vendor__id','fk_category','fk_service','fk_service__service_name','fk_service__service_image','price','hour')
        
        facility_data = VenderFacility.objects.filter(fk_vender_service = vender_service_obj).values('id','fk_vender_service','fk_vender_facility','fk_vender_facility__facility_name')
        
        facility_data1 = VenderFacility.objects.filter(fk_vender_service = vender_service_obj)
        
        facility_list = []
        
        for i in facility_data1:
            facility_list.append(i.fk_vender_facility.id)
            exclude_facility = ServiceFacility.objects.filter(fk_service = service_obj).exclude(id__in = facility_list).values('id','fk_service','facility_name')
        
        temp_dict['service_data'] = service_data
        temp_dict['include_facility'] = facility_data
        temp_dict['exclude_facility'] = exclude_facility
        return Response({'status':200,'msg':'Show Vendor Facility','payload':temp_dict})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong'})
        
#************************************************************ Cart Api and Order Api Start *****************************************************


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Item_Add_to_Cart(request):    #Item Add to Cart 
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        customer_id = data.get('customer_id',None)
        service_id = data.get('vendor_service_id',None)
        quantity = data.get('quantity',None)
        price = data.get('price',None)
        hour = data.get('hour',None)
        category_id = data.get('category_id',None)
        country = data.get('country',None)
        
        
        vendor_obj = VendorDetails.objects.get(id = vendor_id)
        customer_obj = MyUser.objects.get( id = customer_id)
        service_obj = VenderServices.objects.get( id = service_id)
        
        country_obj = CountryMaster.objects.get(country_name = country)
        category_obj = CategoryMaster.objects.get( id = category_id)
        
        # tax_obj = CommisionMaster.objects.get(fk_country = country_obj , fk_category = category_obj ,user_type ="Customer")
        
        if  AddtoCart.objects.filter(fk_vendor = vendor_obj , fk_customer = customer_obj , fk_vender_service__fk_category = category_obj).exists():
            print("previous........")
            
            if AddtoCart.objects.filter(fk_vendor = vendor_obj , fk_customer = customer_obj , fk_vender_service = service_obj).exists():
                cart_obj = AddtoCart.objects.get(fk_vendor = vendor_obj , fk_customer = customer_obj , fk_vender_service = service_obj)
                
                new_quantity = cart_obj.quantity + quantity
                new_total = price * new_quantity
                AddtoCart.objects.filter( id = cart_obj.id).update(quantity = new_quantity , sub_total = new_total )
                return Response({'status':200,'msg':'Data Added Successfully.'})
            else:
                total = quantity * price
                AddtoCart.objects.create(fk_vendor = vendor_obj , fk_category = category_obj ,fk_customer = customer_obj , fk_vender_service = service_obj , price = price , hour = hour, quantity = quantity,sub_total = total)
                
                return Response({'status':200,'msg':'Data Added Successfully.'})
                
        elif AddtoCart.objects.filter(fk_vendor = vendor_obj , fk_customer = customer_obj).filter(~Q(fk_vender_service__fk_category = category_obj)).exists():
            print("---------")
            return Response({'status':403,'msg':'Sorry! You have already added service for another category.To add service of this category please complete booking of first category or remove items from your cart.'})
            
        elif AddtoCart.objects.filter( fk_customer = customer_obj,fk_vender_service__fk_category = category_obj).filter(~Q(fk_vendor = vendor_obj)).exists():
            print("*************")
            return Response({'status':403,'msg':'Sorry! You have already added service for another vendor.To add service of this vendor please complete booking of first vendor or remove items from your cart.'})
            
        elif AddtoCart.objects.filter( fk_customer = customer_obj).filter(~Q(fk_vendor = vendor_obj,fk_vender_service__fk_category = category_obj)).exists():
            print("................")
            return Response({'status':403,'msg':'Sorry! you have already added service for another category.To add service of this category please complete booking of first category or remove items from your cart.'})
            
        else:
            print("---------------------new")
            total = quantity * price
            AddtoCart.objects.create(fk_vendor = vendor_obj , fk_category = category_obj ,fk_customer = customer_obj , fk_vender_service = service_obj , price = price , hour = hour, quantity = quantity,sub_total = total)   # add data to add to cart table
            return Response({'status':200,'msg':'Data Added Successfully.'})
        
        
        return Response({'status':200,'msg':'Data Added Successfully.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Update_Item_Quantity(request):     #Item Increase Quantity
    try:
        data = request.data
        cart_id = data.get('cart_id',None)
        quantity = data.get('quantity',None)
        customer_id = data.get('customer_id',None)
        price = data.get('price',None)
        category_id = data.get('category_id',None)
        country = data.get('country',None)
        
        customer_obj = MyUser.objects.get(id = customer_id)
        
        sub_total = quantity * price
        AddtoCart.objects.filter(id = cart_id).update(quantity = quantity , sub_total = sub_total)
        
        
        return Response({'status':200,'msg':"Item Quantity Add Successfully."})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
        

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Item_Minus(request):    #Item Decrease Quantity
    try:
        data = request.data
        cart_id = data.get('cart_id',None)
        quantity = data.get('quantity',None)
        customer_id = data.get('customer_id',None)
        price = data.get('price',None)
        category_id = data.get('category_id',None)
        country = data.get('country',None)
        
        customer_obj = MyUser.objects.get(id = customer_id)
        
        sub_total = quantity * price
        AddtoCart.objects.filter(id = cart_id).update(quantity = quantity , sub_total = sub_total)
        
        country_obj = CountryMaster.objects.get(country_name = country)
        category_obj = CategoryMaster.objects.get( id = category_id)
        
        tax_obj = CommisionMaster.objects.get(fk_country = country_obj , fk_category = category_obj ,user_type ="Customer")
        
        
        data = AddtoCart.objects.filter(fk_customer = customer_obj)
        sub_total = 0
        calculate_time = 0
        item_count = AddtoCart.objects.filter(fk_customer = customer_obj).count()
        for i in data:
            calculate_time = calculate_time + int(i.hour)
            sub_total = i.sub_total + sub_total 
        
        average_time = calculate_time / item_count
        tax = tax_obj.commision            
        convenience_fee = sub_total * tax / 100
        total_amount = sub_total + convenience_fee
        
        info =[{
            "average_time":int(average_time),
            "sub_total":sub_total,
            "item_count":item_count,
            "convenience_fee":convenience_fee,
            "total_amount":total_amount
        }]
        cart = AddtoCart.objects.filter(fk_customer = customer_obj).values('id','fk_vendor','fk_vendor__fk_country','fk_vendor__fk_country__country_name','fk_customer','fk_vender_service','fk_vender_service__fk_service__service_name','fk_vender_service__fk_service__service_image','quantity','price','hour')
        temp_dict = {}
        temp_dict['cart_data'] = cart
        temp_dict['calculation'] = info 
        
        return Response({'status':200,'msg':"Item Quantity Decrease Successfully.",'payload':temp_dict})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
  
  
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Delete_Item_to_Cart(request):       #Item Delete to Cart
    try:
        data = request.data
        cart_id = data.get('cart_id',None)
        customer_id = data.get('customer_id',None)
        customer_obj = MyUser.objects.get(id = customer_id)
        offer_id = data.get('offer_id',None)
        applied_id = data.get('applied_id',None)
        applied_status = data.get('applied_status',None)
        item_count = AddtoCart.objects.filter(fk_customer = customer_obj).count()
        if item_count == 0:
            
            return Response({'status':403,'msg':'Cart is Empty.'})
        else:
            if AddtoCart.objects.filter( id = cart_id).exists():
                AddtoCart.objects.filter( id = cart_id).delete()
                if applied_status =="True":
                    item_count = AddtoCart.objects.filter(fk_customer = customer_obj).count()
                    if item_count == 0:
                        AppliedOfferCode.objects.filter(id = applied_id).delete()
                        offer_obj = Offers.objects.get(id = offer_id )
                        if offer_obj.used_offercode == 0:
                            pass
                        else:
                            update_offercode = offer_obj.used_offercode - 1
                            Offers.objects.filter(id = offer_obj.id).update(used_offercode = update_offercode)
                    else:
                        pass
                return Response({'status':200,'msg':"Item Removed Successfully."})
            else:
                return Response({'status':403, 'msg':'Something went wrong.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'status':'Something went wrong.'})
        
        

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Promocode_check(request):
    try:
        data = request.data
        customer_id = data.get('customer_id',None)
        category_id = data.get('category_id',None)
        country_name = data.get('country_name',None)
        coupon = data.get('coupon',None)
        cancel_status = data.get('cancel_status',None)
        applied_id = data.get('applied_id',None)
        
        customer_obj = MyUser.objects.get( id = customer_id)
        country_obj = CountryMaster.objects.get(country_name = country_name)
        category_obj = CategoryMaster.objects.get( id = category_id)
        
        print(country_name)
        
        if OrderDetails.objects.filter(user_promocode__contains = coupon , fk_customer = customer_obj , fk_category = category_obj , customer_country = country_name).exists():
            print("---------")
            return Response({'status':403,'msg':'Sorry! You have already used promocode '+ coupon+'.'})
        else:
            if Offers.objects.filter(fk_country = country_obj , fk_category = category_obj ,offer_code__contains = coupon).exists():
                if Offers.objects.filter(fk_country = country_obj , fk_category = category_obj ,offer_code__contains = coupon,offercode_status ="Active").exists():
                    offer_code = Offers.objects.get(fk_country = country_obj , fk_category = category_obj ,offer_code__contains = coupon)
                   
                    if cancel_status == "False":
                        AppliedOfferCode.objects.create(fk_customer = customer_obj , fk_offer = offer_code , is_applied = True) 
                    
                        offer_obj = Offers.objects.get(fk_country = country_obj , fk_category = category_obj ,offer_code__contains = coupon)
                        update_offercode = offer_obj.used_offercode + 1
                        Offers.objects.filter(id = offer_obj.id).update(used_offercode = update_offercode)
                        
                        return Response({'status':200,'msg':'Applied Sucessfully'})
                    else:
                        
                        AppliedOfferCode.objects.filter(id = applied_id).delete()
                        offer_obj = Offers.objects.get(fk_country = country_obj , fk_category = category_obj ,offer_code__contains = coupon)
                        if offer_obj.used_offercode == 0:
                            pass
                        else:
                            update_offercode = offer_obj.used_offercode - 1
                            Offers.objects.filter(id = offer_obj.id).update(used_offercode = update_offercode)
                        
                        return Response({'status':200,'msg':'Promocode code cancel successfully.'})
                else:
                    return Response({'status':403,'msg':'Promocode is Expired.'})
            else:
                return Response({'status':403,'msg':'Invalid Promocode.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})



def Slot(vendor_id,slot_date):
    vendor_obj = VendorDetails.objects.get(id = vendor_id)
    slot_details = OrderDetails.objects.filter(fk_vendor = vendor_obj , booking_date = slot_date,order_status = "Accept")
    temp_list = []
    for i in slot_details:
        print(i.booking_start_time)
        print(i.booking_end_time)
        data = {
        'from_time':i.booking_start_time,
        'to_time':i.booking_end_time,
        }
        
        temp_list.append(data)
    return temp_list
    

def Slot_available_Notavailable(vendor_id,day,slot_date):
    try:
        
        if day =="Monday":
            status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_monday','is_available')
            for i in status:
                i['is_status'] = i['is_monday']
                if i['is_monday'] == True :
                    data = Slot(vendor_id,slot_date)   
                    return data
                else:
                    temp_list = []
                    return temp_list
        elif day =="Tuesday":
            status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_tuesday','is_available')
            for i in status:
                i['is_status'] = i['is_tuesday']
                if i['is_tuesday'] == True :
                    data = Slot(vendor_id,slot_date)   
                    return data
                else:
                    temp_list = []
                    return temp_list
        elif day =="Wednesday":
            status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_wednesday','is_available')
            for i in status:
                i['is_status'] = i['is_wednesday']
                if i['is_wednesday'] == True :
                    data = Slot(vendor_id,slot_date)   
                    return data
                else:
                    temp_list = []
                    return temp_list
        elif day =="Thursday":
            status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_thursday','is_available')
            for i in status:
                i['is_status'] = i['is_thursday']
                if i['is_thursday'] == True:
                    data = Slot(vendor_id,slot_date)   
                    return data
                else:
                    temp_list = []
                    return temp_list
                
        elif day =="Friday":
            status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_friday','is_available')
            for i in status:
                
                i['is_status'] = i['is_friday']
                if i['is_friday'] == True :
                    data = Slot(vendor_id,slot_date)   
                    return data
                else:
                    temp_list = []
                    return temp_list
        elif day =="Saturday":
            status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_saturday','is_available')
            for i in status:
                i['is_status'] = i['is_saturday']
                if i['is_saturday'] == True  :
                    data = Slot(vendor_id,slot_date)   
                    return data
                else:
                    temp_list = []
                    return temp_list
        elif day =="Sunday":
            status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_sunday','is_available')
            for i in status:
                i['is_status'] = i['is_sunday']
                if i['is_sunday'] == True :
                    data = Slot(vendor_id,slot_date)   
                    return data
                else:
                    temp_list = []
                    return temp_list
        else:
            pass
            
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})



def Slot_status(vendor_id, day):
    if day =="Monday":
        status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_monday')
        for i in status:
            i['is_status'] = i['is_monday']
            return status     
    elif day =="Tuesday":
        status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_tuesday')
        for i in status:
            i['is_status'] = i['is_tuesday']
            return status
            
    elif day =="Wednesday":
        status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_wednesday')
        for i in status:
            i['is_status'] = i['is_wednesday']
            return status
            
    elif day =="Thursday":
        status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_thursday')
        for i in status:
            i['is_status'] = i['is_thursday']
            return status
            
    elif day =="Friday":
        status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_friday')
        for i in status: 
            i['is_status'] = i['is_friday']
            return status
    elif day =="Saturday":
        status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_saturday')
        for i in status:
            i['is_status'] = i['is_saturday']
            return status
            
    elif day =="Sunday":
        status = VendorDetails.objects.filter(id = vendor_id).values('from_time','to_time','is_sunday')
        for i in status:
            i['is_status'] = i['is_sunday']
            return status
    else:
        pass        
 
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Next_Six_Date(request):
    try:
        # data = request.data
        data = json.loads(request.body.decode('utf-8'))
        vendor_id = data['vendor_id']
        category_id = data['category_id']
        
        vendor_data = VendorDetails.objects.filter(id = vendor_id).values('full_name','profile_image')
        category_data = CategoryMaster.objects.get(id = category_id)
        
        for i in vendor_data:
            # print(i)
            i['category_name'] = category_data.category_name
        
        cur_date = datetime.now().date()
        
        main_list = []
    
        sub_dict = {}
        temp_list = []
        
        
        day = calendar.day_name[cur_date.weekday()]
        
        data = Slot_available_Notavailable(vendor_id , day,cur_date)   # call function slot_available
        status = Slot_status(vendor_id , day)   # call function slot status
        
        sub_dict['date'] = f"{cur_date.year}-{cur_date.month if cur_date.month >= 10 else '0'+str(cur_date.month)}-{cur_date.day if cur_date.day >= 10 else '0'+str(cur_date.day)}"
        
        sub_dict['slot_details'] = data
        sub_dict['status'] = status[0]
        main_list.append(sub_dict)
        # temp_list.append( f"{cur_date.year}-{cur_date.month if cur_date.month >= 10 else '0'+str(cur_date.month)}-{cur_date.day}")
        
        next_dict = {}
        for i in range(0,6):
            cur_date = cur_date + timedelta(days=1)
            
            day = calendar.day_name[cur_date.weekday()]
        
            data = Slot_available_Notavailable(vendor_id , day,cur_date)   
            status = Slot_status(vendor_id , day)   
            
            next_dict = {'date' :f"{cur_date.year}-{cur_date.month if cur_date.month >= 10 else '0'+str(cur_date.month)}-{cur_date.day if cur_date.day >= 10 else '0'+str(cur_date.day)}",
            'slot_details' : data,
            'status' : status[0]
            }
            
            main_list.append(next_dict)
            
        payload = {
        "vendor_data":vendor_data,
        "data":main_list
        }
        return Response({'status':200,'msg':'Date Details','payload':payload})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
 
        


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Save_Order_Details(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        customer_id = data.get('customer_id',None)
        quantity = data.get('quantity',None)
        address = data.get('address',None)
        customer_country = data.get('customer_country',None)
        city = data.get('city',None)
        zip_code = data.get('zip_code',None)
        lat = data.get('lat',None)
        lng = data.get('lng',None)
        sub_total = data.get('sub_total',None)
        discount = data.get('discount',None)
        convenience_fee = data.get('convenience_fee',None)
        total_amount = data.get('total_amount',None)
        duration = data.get('duration',None)
        booking_date = data.get('booking_date',None)
        booking_start_time = data.get('booking_start_time',None)
        booking_end_time = data.get('booking_end_time',None)
        promocode = data.get('promocode',None)
        services_id = data.get('vendor_services_id',None)
        vendor_country_id = data.get('vendor_country_id',None)
        vendor_country_name = data.get('vendor_country_name',None)
        category_id = data.get('category_id',None)
        current_booking_time = data.get('current_booking_time',None)
        current_booking_date = data.get('current_booking_date',None)
        applied_id = data.get('applied_id',None)
        payment_intent_id = data.get('payment_intent_id',None)
        
        
        country_obj = CountryMaster.objects.get(id = vendor_country_id , country_name = vendor_country_name)
        category_obj = CategoryMaster.objects.get(id = category_id)
        customer_obj = MyUser.objects.get( id = customer_id)
        vendor_obj = VendorDetails.objects.get( id = vendor_id)
        
        vendor_tax = CommisionMaster.objects.get( fk_category = category_obj , fk_country = country_obj , user_type ="Vendor")
        
        print(vendor_tax.commision)
        vendor_tax = sub_total * vendor_tax.commision / 100
        vendor_pay_amount = sub_total - vendor_tax
        # city_obj = CityMaster.objects.get(city_name = city)
        
        order_id = "OID"+ str(random.randint(100000,999999))
        while OrderDetails.objects.filter(order_id=order_id).exists():
          order_id = "OID"+ str(random.randint(100000,999999))
        
        
        OrderDetails.objects.create(order_id = order_id , fk_vendor = vendor_obj , customer_city = city, customer_country = customer_country , fk_category = category_obj , fk_customer = customer_obj ,  quantity = quantity , address = address ,  zip_code = zip_code , lat = lat , lng = lng , sub_total = sub_total , discount = discount , convenience_fee = convenience_fee , total_amount = total_amount , duration = duration , booking_date = booking_date , booking_start_time = booking_start_time , booking_end_time = booking_end_time , user_promocode = promocode , vendor_pay_amount = vendor_pay_amount,current_booking_time = current_booking_time,current_booking_date = current_booking_date , vendor_convenience_fee = vendor_tax , payment_intent_id = payment_intent_id)
        
        
        order_obj = OrderDetails.objects.get(order_id = order_id)
        for i in services_id:
            service_obj = VenderServices.objects.get(id = i)
            add_to_cart_obj = AddtoCart.objects.get(fk_vender_service = service_obj , fk_customer = customer_obj)
            
            OrderService.objects.create( fk_order = order_obj , fk_vendor = vendor_obj , fk_service = service_obj , service_quantity = add_to_cart_obj.quantity , hour = add_to_cart_obj.hour)
            
        payload ={ 'id':order_obj.id,
        'order_id':order_obj.order_id}
        AddtoCart.objects.filter(fk_customer = customer_obj).delete()
        if applied_id == 0:
            pass
        else:
            AppliedOfferCode.objects.filter(id = applied_id).delete()
        user_obj = MyUser.objects.get( email = vendor_obj.fk_user)
        
        Send_Message(user_obj.id,"Vendor_Order",customer_obj.name )
        return Response({'status':200,'msg':'Order Details Save Sucessfully.','payload':payload})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
        

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Stripe_payment(request):
    try:
        data = request.data
        user_id = data.get('user_id',None)
        total_amount = data.get('amount',None)
        user_email = data.get('email',None)
        
        
        
        stripe.api_key = "sk_test_51LHr4UI0Jl0TyufY5lwPfz7zMPSPYd0MUZ7FhDN9n7bCIA7XNqB6G6PlQdVd0lmdrxxoEUg7zXYg2XLIRcPo9c1B00oT6zqkeT"
        customer = stripe.Customer.create(email=user_email)
        ephemeralKey = stripe.EphemeralKey.create(
        customer=customer['id'],
        stripe_version='2020-08-27',
        )
        
        paymentIntent = stripe.PaymentIntent.create(
        amount=total_amount * 100,
        currency='usd',
        customer=customer['id'],
        payment_method_types=[ "card"],
        )
        
        
        MyUser.objects.filter(id = user_id).update( stripe_customer_id = customer['id'])
        payload = {
        "customer_id":customer['id'],
        "client_secret":paymentIntent.client_secret,
        "ephemeral_key":ephemeralKey.secret,
        "payment_intent_id":paymentIntent.id
        }
        
        # print("----------",customer['id'])
        
        # print(ephemeralKey.secret)
        return Response({'status':200,'msg':'Success','payload':payload})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
        

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def card(request):
    try:
        data = request.data
        user_id = data.get('user_id',None)
        total_amount = data.get('amount',None)
        
        stripe.api_key = "sk_test_51LHr4UI0Jl0TyufY5lwPfz7zMPSPYd0MUZ7FhDN9n7bCIA7XNqB6G6PlQdVd0lmdrxxoEUg7zXYg2XLIRcPo9c1B00oT6zqkeT"
        
        # setupIntent = stripe.SetupIntent.create(customer=customer['id'],)
        
        # customer = stripe.Customer.create()
          # ephemeralKey = stripe.EphemeralKey.create(
            # customer=customer['id'],
            # stripe_version='2020-08-27',
          # )
          # stripe.api_version = '2020-08-27;automatic_payment_methods_beta=v1'

          
        # setupIntent = stripe.SetupIntent.create(customer='cus_M6oK49jEagudtc',)
        # payment_menthod = stripe.PaymentMethod.list(customer='cus_M6oK49jEagudtc', type="card")
        
        print(setupIntent)
        print(payment_menthod)
        
        # response = stripe.PaymentIntent.create(
            # amount=total_amount,
            # currency='usd',
            # customer=customer['id'],
            # payment_method=paymentIntent.id,
            # off_session=True,
            # confirm=True,
          # )
        
        # payload = {
        # "customer_id":customer['id'],
        # "client_secret":paymentIntent.client_secret,
        # "ephemeral_key":ephemeralKey.secret
        # }
        # print(customer['id'])
        # print(paymentIntent.client_secret)
        # print(ephemeralKey.secret)
        return Response({'status':200,'msg':'Success'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})



    
        

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Like_Dislike(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        customer_id = data.get('customer_id',None)
        category_id = data.get('category_id',None)
        like_dislike = data.get('like_dislike',None)
        
        vendor_obj = VendorDetails.objects.get( id = vendor_id)
        customer_obj = MyUser.objects.get( id = customer_id)
        category_obj = CategoryMaster.objects.get( id = category_id)
        if LikeDislike.objects.filter(fk_vendor = vendor_obj , fk_customer = customer_obj , like_dislike = True).exists():
           
           LikeDislike.objects.filter(fk_vendor = vendor_obj , fk_customer = customer_obj , like_dislike = True).delete()
           return Response({'status':200,'msg':'Success.'})
        else:
            
            LikeDislike.objects.create(fk_vendor = vendor_obj , fk_customer = customer_obj , like_dislike = like_dislike)
            return Response({'status':200,'msg':'Success.'})
    except:
        return Response({'status':403,'msg':'Something went wrong.'})
  
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Like_Dislike_vendor(request):
    try:
        data = request.data
        customer_id = data.get('customer_id',None)
        
        data = LikeDislike.objects.filter(fk_customer__id = customer_id,like_dislike = True).values('id','fk_vendor__full_name','fk_vendor__profile_image','like_dislike')
        
        for i in data:
            i['rating'] = 5
        return Response({'status':200,'msg':'Show Like Vendor.','payload':data})
    except:
        return Response({'status':200,'msg':'Something went wrong.'})
  


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Get_Cart_data(request):
    try:
        data = request.data
        customer_id = data.get('customer_id',None)
        category_id = data.get('category_id',None)
        country_name = data.get('country_name',None)
        
        customer_obj = MyUser.objects.get( id = customer_id)
        country_obj = CountryMaster.objects.get(country_name = country_name)
        category_obj = CategoryMaster.objects.get( id = category_id)
        
        if AddtoCart.objects.filter(fk_customer = customer_obj).exists():
            tax_obj = CommisionMaster.objects.get(fk_country = country_obj , fk_category = category_obj ,user_type ="Customer")
            
            data = AddtoCart.objects.filter(fk_customer = customer_obj)
            sub_total = 0
            calculate_time = 0
            item_count = AddtoCart.objects.filter(fk_customer = customer_obj).count()
            
            for i in data:
                calculate_time = calculate_time + int(i.hour)
                sub_total = i.sub_total + sub_total       #calculate sub total
            
            
            # average_time = calculate_time / item_count
               
            if AppliedOfferCode.objects.filter(fk_customer = customer_obj).exists():
                
                applied_obj = AppliedOfferCode.objects.get(fk_customer = customer_obj)
                
                
                apply_promocode_calculation = sub_total * applied_obj.fk_offer.discount / 100
                        
                apply_promocode_subtotal = sub_total - apply_promocode_calculation
                
                tax = tax_obj.commision
                
                convenience_fee = apply_promocode_subtotal * tax / 100
                
                
                total_amount = apply_promocode_subtotal + convenience_fee
                
                info =[{
                    "average_time":int(calculate_time),
                    "sub_total":sub_total,
                    "discount": apply_promocode_calculation,
                    "offer_id": applied_obj.fk_offer.id,
                    "discount_percent":applied_obj.fk_offer.discount,
                    "item_count":item_count,
                    "convenience_fee":convenience_fee,
                    "total_amount":total_amount,
                    "applied_id":applied_obj.id,
                    "is_promocde_applied":applied_obj.is_applied,
                    "prmocode_msg":f"{applied_obj.fk_offer.offer_code} Applied Sucessfully.",
                    "promocode":applied_obj.fk_offer.offer_code
                }]
                cart = AddtoCart.objects.filter(fk_customer = customer_obj).values('id','fk_vendor','fk_vendor__fk_country','fk_vendor__fk_country__country_name','fk_customer','fk_vender_service','fk_vender_service__fk_service__service_name','fk_vender_service__fk_service__service_image','quantity','price','hour')
                temp_dict = {}
                
                temp_dict['cart_data'] = cart
                temp_dict['calculation'] = info
                
                return Response({'status':200,'msg':'Cart Data','payload':temp_dict})
            else:
                
                tax = tax_obj.commision
                convenience_fee = sub_total * tax / 100
                total_amount = sub_total + convenience_fee
                
                info =[{
                    "average_time":int(calculate_time),
                    "sub_total":sub_total,
                    "discount": 0.0,
                    "offer_id": 0,
                    "discount_percent":0.0,
                    "item_count":item_count,
                    "convenience_fee":convenience_fee,
                    "total_amount":total_amount,
                    "applied_id":0,
                    "is_promocde_applied":False,
                    "prmocode_msg":"",
                    "promocode":""
                }]
                
                cart = AddtoCart.objects.filter(fk_customer = customer_obj).values('id','fk_vendor','fk_vendor__fk_country','fk_vendor__fk_country__country_name','fk_customer','fk_vender_service','fk_vender_service__fk_service__service_name','fk_vender_service__fk_service__service_image','quantity','price','hour')
                temp_dict = {}
                temp_dict['cart_data'] = cart
                temp_dict['calculation'] = info 
               
                return Response({'status':200,'msg':'Cart Data.','payload':temp_dict})
        else:
            return Response({'status':403,'msg':'Cart is Empty.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
        
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Cart_Quantity(request):
    try:
        data = request.data
        customer_id = data.get('customer_id',None)
        item_count = AddtoCart.objects.filter(fk_customer__id = customer_id ).count()
        data = AddtoCart.objects.filter(fk_customer__id = customer_id).values('fk_category','fk_vendor').distinct()
        if data.exists():
            payload ={
            "item_count":item_count,
            'category_id':data[0]['fk_category'],
            'vendor_id':data[0]['fk_vendor']
            }
        else:
            payload ={
            "item_count":item_count,
            'category_id':0,
            'vendor_id':0
            }
        return Response({'status':200,'msg':'Cart Quantity.','payload':payload})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})





        
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Current_Order(request):
    try:
        data = request.data
        customer_id = data.get('customer_id',None)
        
        customer_obj = MyUser.objects.get(id = customer_id)

        status_list = ['Completed','Cancelled','Rejected']
        order_details = OrderDetails.objects.filter(fk_customer = customer_obj).exclude(order_status__in = status_list).order_by('-id').values('id','order_id','fk_vendor','fk_vendor__profile_image','fk_vendor__full_name','fk_vendor__google_address','fk_vendor__google_address_lat','fk_vendor__google_address_lng','fk_vendor__address_line_one','fk_vendor__address_line_two','fk_vendor__fk_country__country_name','fk_vendor__fk_city__city_name','duration','total_amount','order_status')
         
        for k in order_details:
            temp_dict = {}
            service_list = []
            order_service = OrderService.objects.filter(fk_order__id = k['id'])
            for j in order_service:
                service_list.append(j.fk_service.fk_service.service_name)
            temp_dict['service_name'] = service_list
                
            k['service'] = temp_dict
            k['rating'] = 5
        return Response({'status':200 ,'msg':'Customer Current Order.','payload':order_details}) 
    except:
        traceback.print_exc()
        return Response({'status':403 ,'msg':'Something went wrong.'})
        

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Customer_All_Order(request):
    try:
        data = request.data
        customer_id = data.get('customer_id',None)
        customer_obj = MyUser.objects.get(id = customer_id)
        
        # status = ['Accept','Started']
        
        order_details = OrderDetails.objects.filter(fk_customer = customer_obj).order_by('-id').values('id','fk_customer','fk_customer__name','order_id','fk_vendor','fk_vendor__full_name','booking_date','total_amount','order_status','booking_start_time','quantity','booking_date')
       
        return Response({'status':200,'msg':'Customer Orders','payload':order_details})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong'})
        

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Customer_Detail_Order(request):
    try:
        data = request.data
        sid = data.get('id',None)
        order_id = data.get('order_id',None)
        
        order_data =OrderDetails.objects.filter( id = sid).values('id','order_id','fk_customer','fk_vendor','booking_date','order_status','booking_start_time','address')
        order_service = OrderService.objects.filter(fk_order__id = sid).values('fk_service__fk_service__service_name','fk_service__fk_service__service_image','fk_service__price','fk_service__hour')
        vendor_details = OrderService.objects.filter(fk_order__id = sid).values('fk_vendor__full_name','fk_vendor__profile_image','fk_service__fk_category__category_name').distinct()
        payment_information = OrderDetails.objects.filter( id = sid).values('quantity','sub_total','discount','convenience_fee','total_amount')
        feedback = ReviewsandFeedback.objects.filter(fk_orderdetails__id = sid).values('rating','feedback')
        print(feedback)
        payload ={'order_data':order_data[0],
        'order_service':order_service,
        'vendor_details':vendor_details[0],
        'payment_information':payment_information[0],
        'reviewandfeedback':feedback}
        
        return Response({'status':200,'msg':'Order Detailed.','payload':payload})
    except:
        print(traceback.print_exc())
        return Response({'status':403,'msg':'Something went wrong.'})
        
        
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Customer_Cancel_Order(request):
    try:
        data = request.data
        sid = data.get('id',None)
        order_id = data.get('order_id',None)
        vendor_id = data.get('vendor_id',None)
        stripe.api_key = "sk_test_51LHr4UI0Jl0TyufY5lwPfz7zMPSPYd0MUZ7FhDN9n7bCIA7XNqB6G6PlQdVd0lmdrxxoEUg7zXYg2XLIRcPo9c1B00oT6zqkeT"
        if OrderDetails.objects.filter( id = sid , order_id = order_id , order_status ="Started").exists():
            return Response ({'status':403,'msg':'Your Order has been started by vendor.You cannot cancel order.'})
        else:
            order_obj = OrderDetails.objects.get(id = sid , order_id = order_id)
            buying_date_time = datetime.combine(order_obj.current_booking_date, order_obj.current_booking_time)
            cur_date_time = datetime.now()
            
            diff = cur_date_time - buying_date_time
            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600
            
            
            if int(hours) < 1:
                refund = stripe.Refund.create(payment_intent=order_obj.payment_intent_id, amount=(int((str(order_obj.total_amount).split('.'))[0])) * 100)
                
                OrderDetails.objects.filter(id = sid, order_id = order_id).update(order_status = "Cancelled",stripe_refund_id = refund['id'] , stripe_refund_txtid = refund['balance_transaction'] , stripe_refund_status = refund['status'])
                
                # OrderDetails.objects.filter(id = sid, order_id = order_id).update(order_status = "Cancelled")
                
                vendor_obj = VendorDetails.objects.get(id = vendor_id)
                data = Send_Message(vendor_obj.fk_user.id,"Cancelled",None)
                
                return Response({'status':200,'msg':'Order Cancelled Successfully.'})
            else:
                return Response({'status':403,'msg':'Order Cannot Cancel after 1 hour.'})
            
    except:
        print(traceback.print_exc())
        return Response({'status':403,'msg':'Something went wrong.'})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Order_Completed(request):
    try:
        data = request.data
        sid = data.get('id',None)
        order_id = data.get('order_id',None)
        vendor_id = data.get('vendor_id',None)
        if OrderDetails.objects.filter( id = sid , order_id = order_id, order_status = "Pending"):
            return Response({'status':403,'msg':"You cannot complete order.Your order is not accepted or started."})
        else:
            OrderDetails.objects.filter( id = sid , order_id = order_id).update(order_status = "Completed")
            vendor_obj = VendorDetails.objects.get(id = vendor_id)
            Send_Message(vendor_obj.fk_user.id ,"Completed",None)
            return Response({'status':200,'msg':'Order Completed.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong'})
       
 
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,)) 
@csrf_exempt
def Customer_Reorder(request):
    try:
        data = request.data
        sid = data.get('id',None)
        order_id = data.get('order_id',None)
        order_obj = OrderDetails.objects.get(id = sid , order_id = order_id)
        
        order_service_obj = OrderService.objects.filter(fk_order__id = sid).values('fk_service__fk_category','fk_vendor','fk_service__price','hour','fk_service').distinct()
        order_service = OrderService.objects.filter(fk_order__id = sid)
        vendor_obj = VendorDetails.objects.get(id = order_service_obj[0]['fk_vendor'])
        category_obj = CategoryMaster.objects.get( id = order_service_obj[0]['fk_service__fk_category'])
        customer_obj = MyUser.objects.get(id = order_obj.fk_customer.id)
              
        if  AddtoCart.objects.filter(fk_vendor__id = order_service_obj[0]['fk_vendor'] , fk_customer__id = order_obj.fk_customer.id , fk_vender_service__fk_category__id = order_service_obj[0]['fk_service__fk_category']).exists():
            print("previous........")
            
            for i in order_service:
                print(i)
                if AddtoCart.objects.filter(fk_vendor__id = i.fk_vendor.id , fk_customer__id = order_obj.fk_customer.id , fk_vender_service__id = i.fk_service.id).exists():
                    cart_obj = AddtoCart.objects.get(fk_vendor__id = i.fk_vendor.id , fk_customer__id = order_obj.fk_customer.id , fk_vender_service__id = i.fk_service.id)
                    print("**********")
                    
                    new_quantity = int(cart_obj.quantity) + int(i.service_quantity)
                    print(new_quantity)
                    new_total = cart_obj.price * new_quantity
                    AddtoCart.objects.filter( id = cart_obj.id).update(quantity = new_quantity , sub_total = new_total )
                    
                else:
                    print("---------")
                    total = int(i.service_quantity) * i.fk_service.price
                    AddtoCart.objects.create(fk_vendor = vendor_obj , fk_category = category_obj ,fk_customer = customer_obj , fk_vender_service = i.fk_service , price = i.fk_service.price , hour = i.hour, quantity = i.service_quantity,sub_total = total)
                    
            return Response({'status':200,'msg':'ReOrder Successfully.'})
                
        elif AddtoCart.objects.filter(fk_vendor__id = order_service_obj[0]['fk_vendor'] , fk_customer__id = order_obj.fk_customer.id ).filter(~Q(fk_vender_service__fk_category__id = order_service_obj[0]['fk_service__fk_category'] )).exists():
            # print("---------")
            return Response({'status':403,'msg':'Sorry! You have already added service for another category.To add service of this category please complete booking of first category else discart items from cart.'})
            
        elif AddtoCart.objects.filter( fk_customer__id = order_obj.fk_customer.id,fk_vender_service__fk_category__id = order_service_obj[0]['fk_service__fk_category']).filter(~Q(fk_vendor__id = order_service_obj[0]['fk_vendor'])).exists():
            # print("*************")
            return Response({'status':403,'msg':'Sorry! You have already added service for another vendor.To add service of this vendor please complete booking of first vendor else discart items from cart.'})
            
        elif AddtoCart.objects.filter( fk_customer__id = order_obj.fk_customer.id).filter(~Q(fk_vendor__id = order_service_obj[0]['fk_vendor'],fk_vender_service__fk_category__id = order_service_obj[0]['fk_service__fk_category'])).exists():
            # print("................")
            return Response({'status':403,'msg':'Sorry! you have already added service for another category.To add service of this category please complete booking of first category else discart items from cart.'})
            
        else:
            print("]]]]]]]]]]]]]]]]]]]]]]]]]]]")
            vendor_obj = VendorDetails.objects.get(id = order_service_obj[0]['fk_vendor'])
            category_obj = CategoryMaster.objects.get( id = order_service_obj[0]['fk_service__fk_category'])
            customer_obj = MyUser.objects.get(id = order_obj.fk_customer.id)
              
            # AddtoCart.objects.filter(fk_customer = customer_obj).delete()
            for i in order_service:
                service_obj = VenderServices.objects.get(id = i.fk_service.id)
                total = int(i.service_quantity) * i.fk_service.price
                AddtoCart.objects.create(fk_vendor = vendor_obj , fk_category = category_obj ,fk_customer =  customer_obj, fk_vender_service = service_obj , price = i.fk_service.price , hour = i.hour, quantity = i.service_quantity,sub_total = total)   # add data to add to cart table
                
            return Response({'status':200,'msg':'ReOrder Sucessfully.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
 

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt 
def Logout_api(request):
    try:
        data = request.data
        sid = data.get('id',None)
        MyUser.objects.filter( id = sid).update(firebase_token = '')
        return Response({'status':200,'msg':'Logout Successfully.'})
    except:
        return Response({'status':403,'msg':'Something went wrong.'})

def Calculate_Hour_Minute_Second_Day(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
    
	return (days, hours, minutes, seconds)
  
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Nofification_Api(request):
    try:
        data = request.data
        user_id = data.get('user_id',None)
        notification = Notifications.objects.filter(fk_user__id = user_id).values('fk_user','notification','notification_date','is_seen')
        for i in notification:
            cur_date_time = datetime.now()
            cur_time = datetime.fromisoformat(str(cur_date_time) ).strftime('%Y-%m-%d %H:%M:%S')
            notification_time = datetime.fromisoformat(str(i['notification_date']) ).strftime('%Y-%m-%d %H:%M:%S')
            calculate_time = parser.parse(cur_time) - parser.parse(notification_time)
            data = Calculate_Hour_Minute_Second_Day(calculate_time.days * 24 * 3600 + calculate_time.seconds)
            if data[0] == 0 and data[1] == 0 and data [2] == 0 and data[3] != 0:
                i['notification_days'] = str(data[3]) + " seconds ago"
            elif data[0] == 0 and data[1] == 0 and data[2] != 0 and data[3] != 0:
                i['notification_days'] = str(data[2]) + " minutes ago"
            elif data[0] == 0 and data[1] != 0 and data[2] != 0 and data[3] != 0:
                i['notification_days'] = str(data[1]) + " hours ago"
            elif data[0] != 0 and data[1] != 0 and data[2] != 0 and data[3] != 0:
                i['notification_days'] = str(data[0]) + " days ago"
            else:
                i['notification_days'] = str(data[2]) + " 50 minutes ago"
                
        return Response({'status':200,'msg':'Show Notification.','payload':list(notification)})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Delete_Notification_Api(request):
    try:
        data = request.data
        notification_id = data.get('notification_id',None)
        user_id = data.get('user_id',None)
        if user_id == 0 and notification_id != 0:
            
            Notifications.objects.filter(id = notification_id).delete()
            return Response({'status':200,'msg':'Notification Deleted.'})
        else:
            Notifications.objects.filter(fk_user__id = user_id).delete()
            return Response({'status':200,'msg':'All Notification Deleted.'})
    
    except:
        return Response({'status':403,'msg':'Something went wrong.'})
        
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Nofication_Seen_Api(request):
    try:
        data = request.data
        notification_id = data.get('notification_id',None)
        Notifications.objects.filter(id = notification_id).update(is_seen = True)
        return Response({'status':200,'msg':'Notification View Successfully.'})
    except:
        return Response({'status':403,'msg':'Something went wrong.'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Reviews_Rating_Feedback(request):
    try:
        data = request.data
        sid = data.get('id',None)
        vendor_id = data.get('vendor_id',None)
        rating = data.get('rating',None)
        feedback = data.get('feedback',None)
        vendor_obj = VendorDetails.objects.get(id = vendor_id)
        order_obj = OrderDetails.objects.get(id = sid)
        cur_date = datetime.now().date()
        ReviewsandFeedback.objects.create(fk_orderdetails = order_obj , fk_vendor = vendor_obj , rating = rating , feedback = feedback , review_date = cur_date)
        return Response({'status':200,'msg':'Thank you for your Feedback.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Review_Feedback(request):
    try:
        data = request.data
        order_id = data.get('order_id',None)
        
        feedback = ReviewsandFeedback.objects.filter(fk_orderdetails__order_id = order_id).values('fk_vendor__full_name','fk_vendor__profile_image','rating','feedback')
        print(feedback)
        return Response({'status':200,'msg':'Review and Feedback.','payload':feedback})
    except:
        return Response({'status':403,'msg':'Something went wrong.'})


def send_notification(token_list, message_title, message_body, data_message,order_status,user_type):
    try:
        api_key = str(settings.API_KEY_NOTIFICATION)
        
        # push_service = FCMNotification(api_key=api_key)
        # message_title = "Delivered"
        # message_body = "Your post "+obj.post_id+" has been delivered"
        print(token_list)
        if token_list:
            url = "https://fcm.googleapis.com/fcm/send"
            payload = {
                "data" : data_message,
                "notification" : {
                    "title":message_title,
                    "body":message_body,
                    "order_status":order_status,
                    "user_type":user_type
                },
                "registration_ids":token_list
            }
            headers = {
                'Authorization':'key='+api_key,
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, data = json.dumps(payload))
            print(response.text)
            print(response.json)
        return "success"
    except:
        print(str(traceback.format_exc()))
        return "error"
        

def Send_Message(vendor_id , status,customer_name):
    if customer_name == None:
        pass
    user_obj = MyUser.objects.get(id = vendor_id)
    
    token_list = []
    token = user_obj.firebase_token
    if token:
        token_list.append(str(token))
    else:
        pass
    message_title = "Doorap"
    order_status = ""
    user_type = ""
    cur_date_time = datetime.now()
    if status =="Completed":
        order_status = "Completed"
        user_type = "Vendor"
        message_body = "Dear Vendor Customer Job Completed."
        Notifications.objects.create(fk_user = user_obj , notification = message_body , notification_date = cur_date_time)
    elif status == "Cancelled":
        order_status = "Cancelled"
        user_type = "Vendor"
        message_body = "Dear Vendor We are sorry to inform you that your job has been " +status + " by Customer."
        Notifications.objects.create(fk_user = user_obj , notification = message_body, notification_date = cur_date_time)
    elif status =="Vendor_Order":
        order_status = "Pending"
        user_type = "Vendor"
        message_body = "Dear Vendor you have receive a new job from " + str(customer_name)
        Notifications.objects.create(fk_user = user_obj , notification = message_body, notification_date = cur_date_time)
    else:
        order_status = "Cancelled"
        user_type = "Vendor"
        message_body = "Dear " + str(user_obj.name)+ " We would gladly like to inform you that your order has been "+status
        Notifications.objects.create(fk_user = user_obj , notification = message_body, notification_date = cur_date_time)
    data_message = {
        'title':message_title,
        "body":message_body,
        "order_status":order_status,
        "user_type":user_type,
        "action":"Program",
        "action_id":str(user_obj.id),
        "current_datetime":str(datetime.now()).split(".")[0],
        "image_url":"",
        
        "android_channel_id": "noti_push_app_2",
        "sound": "alarm.mp3",
        "click_action": "FLUTTER_NOTIFICATION_CLICK",
    }
    res = send_notification(token_list, message_title, message_body, data_message,order_status,user_type)
    print("notification responsre..................",res) 
                
        


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def test(request):
    try:
        data = request.data
        customer_id = data.get('customer_id',None)
        category_id = data.get('category_id',None)
        country_name = data.get('country_name',None)
        coupon = data.get('coupon',None)
        cancel_status = data.get('cancel_status',None)
        applied_id = data.get('applied_id',None)
        
        customer_obj = MyUser.objects.get( id = customer_id)
        country_obj = CountryMaster.objects.get(country_name = country_name)
        category_obj = CategoryMaster.objects.get( id = category_id)
        
        print(coupon)
        
        if OrderDetails.objects.filter(user_promocode__exact = coupon , fk_customer = customer_obj , fk_category = category_obj , customer_country = country_name).exists():
            print("---------fsdfsdfsdfsd")
            return Response({'status':403,'msg':'Sorry! You have already used promocode '+ coupon+'.'})
        else:
            if Offers.objects.filter(fk_country = country_obj , fk_category = category_obj ,offer_code__exact = coupon).exists():
                if Offers.objects.filter(fk_country = country_obj , fk_category = category_obj ,offer_code__exact = coupon,offercode_status ="Active").exists():
                    offer_code = Offers.objects.get(fk_country = country_obj , fk_category = category_obj ,offer_code__contains = coupon)
                   
                    if cancel_status == "False":
                        AppliedOfferCode.objects.create(fk_customer = customer_obj , fk_offer = offer_code , is_applied = True) 
                    
                        offer_obj = Offers.objects.get(fk_country = country_obj , fk_category = category_obj ,offer_code__contains = coupon)
                        update_offercode = offer_obj.used_offercode + 1
                        Offers.objects.filter(id = offer_obj.id).update(used_offercode = update_offercode)
                        
                        return Response({'status':200,'msg':'Applied Sucessfully'})
                    else:
                        
                        AppliedOfferCode.objects.filter(id = applied_id).delete()
                        offer_obj = Offers.objects.get(fk_country = country_obj , fk_category = category_obj ,offer_code__contains = coupon)
                        if offer_obj.used_offercode == 0:
                            pass
                        else:
                            update_offercode = offer_obj.used_offercode - 1
                            Offers.objects.filter(id = offer_obj.id).update(used_offercode = update_offercode)
                        
                        return Response({'status':200,'msg':'Promocode code cancel successfully.'})
                else:
                    return Response({'status':403,'msg':'Promocode is Expired.'})
            else:
                return Response({'status':403,'msg':'Invalid Promocode.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})

