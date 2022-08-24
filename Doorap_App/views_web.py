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
import datetime
import random
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import types
from six import text_type
from django.contrib.auth import authenticate
from django.db.models.expressions import RawSQL
import stripe


#Create Token with out password
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, obj):
        print("%%%%",obj)
        self.user = obj

        refresh = self.get_token(self.user)

        data = {}
        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)

        return data

#****************************************************

#************************************************************************ START VENDOR APP API ********************************************************************


#********************************* SignUp Api ********************************

@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def get_otp(request):
    try:
        data = request.data
        email = data.get('email', None)

        if (email == "" or email==None):
            return Response({'status': 403, "msg": 'Please check your request keys.'})
        elif MyUser.objects.filter(email=data['email']).exists():
            user_obj = MyUser.objects.get(email = email)
            if user_obj.is_vendor == True and user_obj.is_customer == True:
                return Response({'status': 403,  "msg": 'This Email already registered as Vendor and Customer..'})
            
            elif user_obj.is_vendor == True and user_obj.login_id == None and user_obj.login_type == None:
                temp_dict = {}
                temp_dict["otp"] = 0
                temp_dict["signup_msg"] = "This email is associated with Vendor. Do you want to continue as Customer?."
                temp_dict["is_vendor"] = "True"
                temp_dict["is_customer"] = "False"
                return Response({'status': 200,"msg":"","payload":temp_dict})
            elif user_obj.is_customer == True and user_obj.login_id == None and user_obj.login_type == None:
                temp_dict = {}
                temp_dict["otp"] = 0
                temp_dict["signup_msg"] = "This email is associated with Customer. Do you want to continue as Vendor?."
                temp_dict["is_vendor"] = "False"
                temp_dict["is_customer"] = "True"
                return Response({'status': 200,"msg":"","payload":temp_dict})
            else:
                temp_dict = {}
                temp_dict["otp"] = 0
                temp_dict["signup_msg"] = "This email is associated with Customer as Google. Do you want to continue as Vendor?."
                temp_dict["is_vendor"] = "False"
                temp_dict["is_customer"] = "True"
                return Response({'status': 200,"msg":"","payload":temp_dict})
                # if user_obj.is_vendor == True and user_obj.login_type == "Facebook":
                    # temp_dict = {}
                    # temp_dict["otp"] = 0
                    # temp_dict["signup_msg"] = "This email is associated with Vendor as Facebook. Do you want to continue as Customer?."
                    # temp_dict["is_vendor"] = "True"
                    # temp_dict["is_customer"] = "False"
                    # return Response({'status': 200,"msg":"","payload":temp_dict})
                # elif user_obj.is_vendor == True and  user_obj.login_type == "Google":
                    # temp_dict = {}
                    # temp_dict["otp"] = 0
                    # temp_dict["signup_msg"] = "This email is associated with Vendor as Google. Do you want to continue as Customer?."
                    # temp_dict["is_vendor"] = "True"
                    # temp_dict["is_customer"] = "False"
                    # return Response({'status': 200,"msg":"","payload":temp_dict})
                # elif user_obj.is_vendor == True and user_obj.login_type == "Apple":
                    # temp_dict = {}
                    # temp_dict["otp"] = 0
                    # temp_dict["signup_msg"] = "This email is associated with Vendor as Apple. Do you want to continue as Customer?."
                    # temp_dict["is_vendor"] = "True"
                    # temp_dict["is_customer"] = "False"
                    # return Response({'status': 200,"msg":"","payload":temp_dict})
                # elif user_obj.is_customer == True and user_obj.login_type == "Facebook" :
                    # temp_dict = {}
                    # temp_dict["otp"] = 0
                    # temp_dict["signup_msg"] = "This email is associated with Customer as Facebook. Do you want to continue as Vendor?."
                    # temp_dict["is_vendor"] = "False"
                    # temp_dict["is_customer"] = "True"
                    # return Response({'status': 200,"msg":"","payload":temp_dict})
                # elif user_obj.is_customer == True and user_obj.login_type == "Google":    
                    # temp_dict = {}
                    # temp_dict["otp"] = 0
                    # temp_dict["signup_msg"] = "This email is associated with Customer as Google. Do you want to continue as Vendor?."
                    # temp_dict["is_vendor"] = "False"
                    # temp_dict["is_customer"] = "True"
                    # return Response({'status': 200,"msg":"","payload":temp_dict})
                # elif user_obj.is_customer == True and user_obj.login_type == "Apple":    
                    # temp_dict = {}
                    # temp_dict["otp"] = 0
                    # temp_dict["signup_msg"] = "This email is associated with Customer as Apple. Do you want to continue as Vendor?."
                    # temp_dict["is_vendor"] = "False"
                    # temp_dict["is_customer"] = "True"
                    # return Response({'status': 200,"msg":"","payload":temp_dict})
                
                
                
        else:
            temp_dict = {}
            otp = random.randint(1000,9999)
            send_mail('Doorap Account Verification', f'Your OTP is {otp}.\nUse this OTP to complete your Account Verification.\nNote: Please do not share your OTP or password with anyone.\nIf you have any questions or if we can further assist you in any way, please feel free email us at noreplydoorap@gmail.com\nThank You,\nTeam Doorap', settings.EMAIL_HOST_USER, [email])
            temp_dict['otp'] = otp
            temp_dict["signup_msg"] = ""

            return Response({'status': 200, "msg": 'OTP Sent Successfully.', 'payload': temp_dict})
    except BaseException as e:
        traceback.print_exc()
        return Response({'status': 403, "msg": 'Something went wrong.'})


@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def sign_up(request):
    try:
        data = request.data
        name = data.get('name', None)
        email = data.get('email', None)
        password = data.get('password',None)
        firebase_token = data.get('firebase_token', None)
        is_vendor1 = data.get('is_vendor', None)
        is_customer1 = data.get('is_customer',None)

        if MyUser.objects.filter(email = email,is_vendor = True).exists():
            print("is_customer*************")
            user_obj = MyUser.objects.get(email=email)
            serializer1 = CustomerSignUp(user_obj,data = request.data)
            if serializer1.is_valid():

                serializer1.save()

                #generate token
                temp_obj = MyTokenObtainPairSerializer()
                token = temp_obj.validate(user_obj)

                temp_dict = {}
                temp_dict['id'] = serializer1.data.get('id',None)
                temp_dict['email'] = serializer1.data.get('email',None)
                temp_dict['firebase_token'] = serializer1.data.get('firebase_token',None)
                temp_dict['password'] = serializer1.data.get('password',None)
                temp_dict['api_token'] = token

                return Response({'status': 200, "msg": 'SignUp successfully.', 'payload': temp_dict})
            else:
                print(serializer1.errors)
                return Response({'status': 403, "msg": 'Something went wrong.'})
        elif MyUser.objects.filter(email = email , is_customer = True):
            print("is_vendor*************")
            user_obj = MyUser.objects.get(email=email)
            serializer1 = VenderSignUp(user_obj,data = request.data)
            if serializer1.is_valid():
                serializer1.save()

                #generate token
                temp_obj = MyTokenObtainPairSerializer()
                token = temp_obj.validate(user_obj)

                temp_dict = {}
                temp_dict['id'] = serializer1.data.get('id',None)
                temp_dict['email'] = serializer1.data.get('email',None)
                temp_dict['firebase_token'] = serializer1.data.get('firebase_token',None)
                temp_dict['password'] = serializer1.data.get('password',None)
                temp_dict['api_token'] = token


                return Response({'status': 200, "msg": 'SignUp successfully.', 'payload': temp_dict})
            else:
                print(serializer1.errors)
                return Response({'status': 403, "msg": 'Something went wrong.'})
        else:
            print("######################")
            if(email == "" or email == None) or (name == "" or name == None) or (password == "" or password == None) or (firebase_token == "" or firebase_token == None) or (is_vendor1 == "" or is_vendor1 == None) or (is_customer1 == "" or is_customer1 == None):
                return Response({'status':403, "msg":'Please check your request keys.'})
            else:
                print("***********New User")
                serializer1 = MyUserSerializer(data = request.data)
                if serializer1.is_valid():
                    serializer1.save()
                    host_url = request.build_absolute_uri().rsplit('/', 3)[0]
                    data = {
                        'email': email,
                        'password': password,
                    }
                    URL = f'{host_url}/gettoken/'
                    headers = {'content-Type':'application/json'}
                    json_data = json.dumps(data)
                    r = requests.post(url = URL,headers=headers, data=json_data)

                    temp_dict = {}
                    temp_dict['id'] = serializer1.data.get('id',None)
                    temp_dict['email'] = serializer1.data.get('email',None)
                    temp_dict['firebase_token'] = serializer1.data.get('firebase_token',None)
                    temp_dict['password'] = serializer1.data.get('password',None)

                    temp_dict['api_token'] = r.json()

                    return Response({'status': 200, "msg": 'SignUp successfully.', 'payload': temp_dict})
                else:
                    print(serializer1.errors)
                    return Response({'status': 403, "msg": 'Something went wrong.'})
    except BaseException as e:
        traceback.print_exc()
        return Response({'status': 403, "msg": 'Something went wrong.'})

# ****************************** End Signup Api **************



#*************************** Get Country and City Api ************************

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def get_states(request):
    try:
        states = CountryMaster.objects.all().values()
        return Response({'status': 200, "msg": "Country List", 'payload': list(states)})
    except:
        traceback.print_exc()
        return Response({'status':403,"msg":'Something went wrong.'})


@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def get_cities(request):
    try:
        data = request.data

        sid = data.get('id',None)

        if sid == "" or sid == None:
            return Response({'status':403, "msg":'Please check your request keys.'})
        else:
            city = CityMaster.objects.filter(fk_country = sid).values()
            return Response({'status': 200, "msg":"City List", 'payload': list(city)})
    except BaseException as e:
        traceback.print_exc()
        return Response({'status':403, "msg":'Something went wrong'})


#************************* End Get State and City Api ****************************

# ********************************** Save_profile Api *****************************

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
# @permission_classes((AllowAny,))
@csrf_exempt
def save_profile(request):
    try:
        data = request.data

        email = data.get('email',None)
        full_name = data.get('full_name',None)
        profile_image = request.FILES['profile_image']
        abount_me = data.get('abount_me' , None)
        business_name = data.get('business_name',None)
        mobile_no = data.get('mobile_no', None)
        google_address = data.get('google_address',None)
        google_address_lat = data.get('google_address_lat', None)
        google_address_lng = data.get('google_address_lng',None)
        address_line_one = data.get('address_line_one',None)
        address_line_two = data.get('address_line_two', None)
        fk_country = data.get('fk_country',None)
        fk_city = data.get('fk_city',None)
        zip_code = data.get('zip_code', None)
        is_profile_create = data.get('is_profile_create',None)

        if (full_name == "" or full_name == None) or (email == "" or email==None) or (profile_image == "" or profile_image == None) or (abount_me == "" or abount_me == None) or (business_name == "" or business_name == None) or (mobile_no == "" or mobile_no == None) or (google_address == "" or google_address == None) or (google_address_lat == "" or google_address_lat == None) or (google_address_lng == "" or google_address_lng  == None) or (address_line_one == "" or address_line_one == None)  or (fk_country == "" or fk_country == None) or (fk_city == "" or fk_city == None) or (zip_code == "" or zip_code == None):

            return Response({'status':403, "msg":'Please check your request keys.'})
        else:
            user_obj = MyUser.objects.get(email = email)

            country_obj = CountryMaster.objects.get(id=fk_country)
            city_obj = CityMaster.objects.get(id=fk_city)

            serializer1 = VenderDetailsSerializer(data=request.data,context={'user_obj':user_obj,'country_obj':country_obj,'city_obj':city_obj} )
            if serializer1.is_valid():
                serializer1.save()
                MyUser.objects.filter(email = email).update(is_profile_create = True)
                VendorDetails.objects.filter(fk_user__email = email).update(is_available= True)
                return Response({'status': 200,  'msg': "Profile Save Sucessfully"})
            else:
                print(serializer1.errors)
                return Response({'status':403, "msg":'Something went wrong'})

    except:
        traceback.print_exc()
        return Response({'status':403, "msg":'Something went wrong'})

#*********************************** End Save Profile Api *****************************



#************************************* Login Api ***************************************

@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def Vender_login(request):
    try:
        data = request.data
        email = data.get('email',None)
        password = data.get('password',None)
        firebase_token = data.get('firebase_token',None)
        if (email == "" or email == None)  or (firebase_token == "" or firebase_token == None):
           return Response({'status':403, "msg":'Please check your request keys.'})
        else:
            try:
                serializer = MyUserLoginSerializer(data = data)
                if serializer.is_valid(raise_exception = True):
                    host_url = request.build_absolute_uri().rsplit('/', 3)[0]
                    print(host_url,"----------------")
                    data = {
                        'email': email,
                        'password': password,
                    }
                    URL = f'{host_url}/gettoken/'
                    print("------------",URL)
                    headers = {'content-Type':'application/json'}
                    json_data = json.dumps(data)
                    r = requests.post(url = URL,headers=headers, data=json_data)

                    temp_dict = {}
                    if serializer.data.get('is_vendor',None) == True and serializer.data.get('is_customer',None) == True:
                        print("*****************1")
                        vender = serializer.data.get('is_vendor',None)
                        user_id = MyUser.objects.get(id = serializer.data.get('id',None))

                        temp_dict['id'] = serializer.data.get('id',None)
                        temp_dict['name'] = serializer.data.get('name',None)
                        temp_dict['email'] = serializer.data.get('email',None)
                        temp_dict['firebase_token'] = serializer.data.get('firebase_token',None)
                        temp_dict['is_vendor'] = serializer.data.get('is_vendor',None)
                        temp_dict['is_customer'] = serializer.data.get('is_customer',None)
                        temp_dict['is_profile_create'] = user_id.is_profile_create
                        temp_dict['api_token'] = r.json()
                        return Response({'status': 200, "msg": 'Logged In successfully.', 'payload': temp_dict})
                    elif serializer.data.get('is_vendor',None) == True:
                        print("*****************2")
                        vender = serializer.data.get('is_vendor',None)
                        user_id = MyUser.objects.get(id = serializer.data.get('id',None))

                        temp_dict['id'] = serializer.data.get('id',None)
                        temp_dict['name'] = serializer.data.get('name',None)
                        temp_dict['email'] = serializer.data.get('email',None)
                        temp_dict['firebase_token'] = serializer.data.get('firebase_token',None)
                        temp_dict['is_vendor'] = serializer.data.get('is_vendor',None)
                        temp_dict['is_customer'] = serializer.data.get('is_customer',None)
                        temp_dict['is_profile_create'] = user_id.is_profile_create
                        temp_dict['api_token'] = r.json()
                        return Response({'status': 200, "msg": 'Logged In successfully.', 'payload': temp_dict})
                    elif serializer.data.get('is_customer',None) == True:
                        print("*****************3")
                        vender = serializer.data.get('is_vendor',None)
                        user_id = MyUser.objects.get(id = serializer.data.get('id',None))
                        temp_dict['id'] = serializer.data.get('id',None)
                        temp_dict['name'] = serializer.data.get('name',None)
                        temp_dict['email'] = serializer.data.get('email',None)
                        temp_dict['firebase_token'] = serializer.data.get('firebase_token',None)
                        temp_dict['is_vendor'] = serializer.data.get('is_vendor',None)
                        temp_dict['is_customer'] = serializer.data.get('is_customer',None)
                        temp_dict['is_profile_create'] = user_id.is_profile_create
                        temp_dict['api_token'] = r.json()
                        return Response({'status': 200, "msg": 'Logged In Successfully.', 'payload': temp_dict})
                    else:
                        pass
                else:
                    return Response({"status": 403, "msg": 'Login failed'})
            except ValidationError as e:
                traceback.print_exc()
                return Response({"status": 403, "msg": 'Invalid credentials'})
            except:
                traceback.print_exc()
                return Response({"status": 403, "msg": 'Invalid credentials'})
    except:
        traceback.print_exc()
        return Response({'status':403, "msg":'Something went wrong'})

#************************************ End Login Api ***********************************


#*************************************** Forgot Password Api *****************************



@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def forgotPassword_get_otp(request):
    try:
        data = request.data
        email = data.get('email',None)

        if MyUser.objects.filter(email=email).exists():
            user_obj = MyUser.objects.get(email=email)

            otp = random.randint(1000,9999)

            send_mail('Doorap Account Verification', f'Your OTP is {otp}.\nUse this OTP to complete your Account Verification.\nNote: Please do not share your OTP or password with anyone.\nIf you have any questions or if we can further assist you in any way, please feel free email us at noreplydoorap@gmail.com\nThank you,\nTeam Doorap', settings.EMAIL_HOST_USER, [email])
            context ={
            'id': user_obj.id,
            'otp':otp
            }
            return Response({'status': 200, "msg": 'OTP Sent Successfully',"payload":context})
        else:
            return Response({'status': 403, "msg": 'Email id not found!'})
    except:
       traceback.print_exc()
       return Response({'status':403, "msg":'Something went wrong'})


@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def forgot_password(request):
    try:
       data = request.data

       user_id = data.get('id',None)
       password = data.get('password' , None)

       if password == "" or password == None:
            return Response({'status':403, "msg":'Please check your request keys.'})
       else:
            try:
                user_obj = MyUser.objects.get(id=user_id)
                serializer = ForgotPasswordSerializer(user_obj,data=data,context={'password':password})
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': 200, "msg": 'Your password has been changed successfully!', 'payload': serializer.data})
                else:
                    print(serializer.errors)
                    return Response({"status": 403, "msg": "Reset Operation Failed."})
            except MyUser.DoesNotExist:
                return Response({"status": 403, "msg": "Please check the user id."})
            except:
                traceback.print_exc()
                return Response({"status": 403, "msg": "Reset Operation Failed.f"})
    except Exception as e:
        return Response({"status": 403, "msg": "Reset Operation Failed.", "error": str(traceback.format_exc())})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def change_password(request):
    try:
       data = request.data

       user_id = data.get('id',None)

       old_password = data.get('old_password' , None)
       new_password = data.get('new_password',None)

       if (old_password == "" or old_password == None) or (new_password == "" or new_password == None):
            return Response({'status':403, "msg":'Please check your request keys.'})
       else:
            try:
                user_obj = MyUser.objects.get(id=user_id)
                serializer = ChangePasswordSerializer(user_obj,data=data,context={'old_password':old_password,'new_password':new_password})
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': 200, "msg": 'Your password has been reset successfully!', 'payload': serializer.data})
                else:
                    print(serializer.errors)
                    return Response({"status": 403, "msg": "Reset Operation Failed."})
            except MyUser.DoesNotExist:
                return Response({"status": 403, "msg": "Please check the user id."})
            except ValidationError as e:
                return Response({"status": 403, "msg": "Old password doesn't matched."})
            except:
                traceback.print_exc()
                return Response({"status": 403, "msg": "Reset Operation Failed.f"})
    except Exception as e:
        return Response({"status": 403, "msg": "Reset Operation Failed.", "error": str(traceback.format_exc())})



#**************************************** End Forgot Password Api **********************************



#**************************************** User Profile Api **************************************
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def view_profile(request):
    try:
        data = request.data
        user_id = data.get('id',None)
        # if MyUser.objects.filter(id = user_id).exists():
        obj = MyUser.objects.get(id = user_id)
        if obj:
            email = obj.email
            print("...........",email)
            if VendorDetails.objects.filter(fk_user__email = email).exists():
                if VendorDetails.objects.filter(fk_user__email = email ,user_status = "Approve").exists():
                    user_obj = VendorDetails.objects.get(fk_user__email = email)
                    user_details = VendorDetails.objects.filter(fk_user__email = email).values('id','fk_user','full_name','profile_image','abount_me','business_name','mobile_no','google_address','google_address_lat','google_address_lng','address_line_one','address_line_two','fk_city__city_name','fk_country__country_name','zip_code','user_status','is_available','fk_city','fk_country','is_service_created')
                    print(user_details)
                    return Response({'status': 200, "msg": 'Vender Details','payload':list(user_details),"is_approve":"true"})
                else:
                    user_details = VendorDetails.objects.filter(fk_user__email = email).values('id','fk_user','full_name','profile_image','abount_me','business_name','mobile_no','google_address','google_address_lat','google_address_lng','address_line_one','address_line_two','fk_city__city_name','fk_country__country_name','zip_code','user_status','is_available','fk_city','fk_country','is_service_created')
                    print(user_details)
                return JsonResponse({"status":200,"msg": 'Vender Details','payload':list(user_details),"is_approve":"false"})
            else:
                return Response({'status': 403, "msg": 'User Id DoesNotExist.'})
        else:
            return Response({'status': 403, "msg": 'User Id DoesNotExist.'})
    except BaseException as e:
        traceback.print_exc()
        return Response({'status': 403, "msg": 'Something went wrong.'})



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Edit_profile(request):
    try:
        data = request.data
        user_id = data.get('id',None)
        full_name = data.get('full_name',None)
        abount_me = data.get('abount_me',None)
        profile_image = data.get('profile_image',None)
        business_name = data.get('business_name',None)
        mobile_no = data.get('mobile_no',None)
        google_address = data.get('google_address',None)
        google_address_lat = data.get('google_address_lat',None)
        google_address_lng = data.get('google_address_lng',None)
        address_line_one = data.get('address_line_one',None)
        address_line_two = data.get('address_line_two',None)
        fk_country = data.get('fk_country', None)
        fk_city = data.get('fk_city',None)
        zip_code = data.get('zip_code',None)

        obj = MyUser.objects.get(id = user_id)
        email = obj.email
        user_obj = VendorDetails.objects.get(fk_user__email = email)

        # print("********",profile_image)
        country_obj = CountryMaster.objects.get(id=fk_country)

        city_obj = CityMaster.objects.get(id=fk_city)

        serializer = EditProfileSerializer(user_obj,data=request.data,context={'country_obj':country_obj,'city_obj':city_obj})

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200, "msg": 'Profile Updated Successfully!'})
        else:
            print(serializer.errors)
            return Response({'status': 403, "msg": 'Something went wrong.'})

    except BaseException as e:
        traceback.print_exc()
        return Response({'status': 403, "msg": 'Something went wrong.'})




@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def user_available(request):
    try:
        data = request.data
        user_id = data.get('id',None)
        is_available = data.get('is_available',None)
        if (user_id == "" or user_id == None) or ( is_available == "" or is_available == None):
            return Response({'status': 403, "msg": 'Something went wrong.'})
        else:
            obj = MyUser.objects.get(id = user_id)
            print(obj)
            if obj:
                VendorDetails.objects.filter(fk_user__email=obj.email).update(is_available=is_available)
                return Response({'status': 200, "msg": 'User Availability Set.'})
            else:
               return Response({'status': 403, "msg": 'Something went wrong.'})
    except:
        traceback.print_exc()
        return Response({'status': 403, "msg": 'Something went wrong.'})



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Add_Bank_Account(request):
    try:
        data = request.data
        user_id = data.get('id',None)
        account_no = data.get('Account_no',None)
        iban_code = data.get('IBAN_no',None)
        bic_code = data.get('BIC_code',None)
        bank_name = data.get('Bank_name',None)

        if (user_id == "" or user_id == None) or (account_no == "" or  account_no == None) or (iban_code == "" or  iban_code == None) or (bic_code == "" or bic_code == None) or (bank_name == "" or bank_name == None):
            return Response({'status':403, "msg":'Please check your request keys.'})
        else:
                # MyUser.objects.get(id = user_id)
                obj = MyUser.objects.get(id = user_id)
                if obj:
                    user_obj = VendorDetails.objects.get(fk_user__email = obj.email)
                    if Vender_AccountDetails.objects.filter(fk_vender = user_obj).exists():
                        account_obj = Vender_AccountDetails.objects.get(fk_vender = user_obj)
                        Vender_AccountDetails.objects.filter(id = account_obj.id).update(Account_no = account_no , IBAN_no = iban_code , BIC_code = bic_code , Bank_name = bank_name)
                        return Response({'status': 200, "msg": 'Bank Details Updated Successfully.'})
                    else:
                        serializer = AddBankAccountSerializer(data = request.data, context={'user_obj':user_obj})
                        if serializer.is_valid():
                            serializer.save()
                            return Response({'status': 200, "msg": 'Bank Details Added Successfully.'})
                        else:
                            print(serializer.errors)
                            return Response({'status': 403, "msg": 'Something went wrong.'})
                else:
                    return Response({'status': 403, "msg": 'Something went wrong.'})

    except:
        traceback.print_exc()
        return Response({'status': 403, "msg": 'Something went wrong.'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Bank_Account(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        bank_details = Vender_AccountDetails.objects.filter(fk_vender__fk_user__id = vendor_id).values('Account_no','IBAN_no','BIC_code','Bank_name')
        
        return Response({'status':200,'msg':'Show Bank Details.','payload':bank_details})
    except:
        return Response({'status':403,'msg':'Something went wrong.'})


#****************************************** End User Profile Api **********************************


#*************************************** Set Service and Availability api  **************************************
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def All_Category(request):     # Show All Category
    try:
        category = CategoryMaster.objects.all().values()
        data = CategoryMaster.objects.all()
        for i in data:
            print(i.category_name)
        if category:
            return Response({"status":200,"msg":"Category List","payload":list(category)})
        else:
            return Response({'status':403,'msg':'Something went wrong'})
    except:
        traceback.print_exc()
        return Response({"status":403 ,"msg":"Something went wrong"})



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Services(request):      #Show All Service
    try:
        data = request.data
        category_id = data.get('id',None)
        if category_id is not None:
            if ServiceMaster.objects.filter(fk_category__id = category_id ).exists():
                services = ServiceMaster.objects.filter(fk_category__id = category_id).values()
                return Response({'status':200,'msg':"Services List",'payload':list(services)})
            else:
                services = ServiceMaster.objects.filter(fk_category__id = category_id).values()
                return Response({'status':200,'msg':"Services List",'payload':list(services)})
        else:
            return Response({'status':403,'msg':'Something went wrong.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Facilities(request):       # Show All Facility
    try:
        data = request.data
        service_id = data.get('id',None)
        if service_id is not None:
            if ServiceFacility.objects.filter(fk_service__id = service_id).exists():
                facility = ServiceFacility.objects.filter(fk_service__id = service_id).values('id','fk_service','facility_name')
                return Response({'status':200, 'msg':'Facility List','payload':list(facility)})
            else:
                facility = ServiceFacility.objects.filter(fk_service__id = service_id).values('id','fk_service','facility_name')
                return Response({'status':200, 'msg':'Facility List','payload':list(facility)})
        else:
            
            return Response({'status':403,'msg':'Something went wrong'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong'})

import ast


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Add_Vendor_Custom_ServicesandFacility(request):   #Add Custom Service
    try:
        data = request.data
        vender_id = data.get('vendor_id',None)
        category_id = data.get('category_id',None)
        custom_service_name = data.get('custom_service_name',None)
        custom_service_image = request.FILES['custom_service_image']
        custom_service_price = data.get('custom_service_price',None)
        custom_service_time = data.get('custom_service_time',None)
        facility_list = data.get('custom_facility_name',None)
        
        
        custom_facility_name = json.loads(facility_list)
        
        user_obj = MyUser.objects.get(id = vender_id) 
        vender_obj = VendorDetails.objects.get(fk_user = user_obj) # vendor object
        category_obj = CategoryMaster.objects.get(id = category_id) # category object
        if VenderCustomService.objects.filter(custom_service_name = custom_service_name,fk_vendor = vender_obj,fk_category = category_obj ).exists():
            return Response({'status':403,'msg':'This Service is already Added.'})
        else:
            VenderCustomService.objects.create(fk_vendor = vender_obj , fk_category = category_obj, custom_service_image = custom_service_image , custom_service_name = custom_service_name, custom_service_price = custom_service_price , custom_service_time = custom_service_time)
            
            service_obj = VenderCustomService.objects.get(fk_vendor = vender_obj, fk_category = category_obj ,custom_service_name = custom_service_name)   # Vender Custom Service object
            for facility_name in custom_facility_name:
                VenderCustomFacility.objects.create(fk_custom_service = service_obj, custom_facility_name = facility_name)
                
            email = "noreplydoorap@gmail.com"
            send_mail('Notification about Custom Service', f'Dear Admin,\nThis email is to notify you that the vendor {vender_obj.full_name} has added the new service {custom_service_name},request you to review the new service and take an appropriate action on it.\nThank You,\nTeam Doorap', settings.EMAIL_HOST_USER, [email]) # send mail notfication to admin vendor is added no custom service
            
        return Response({'status':200,'msg':'Service Created Successfully.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})

#****************************************  Set Service and Availability Api *************************************

#********************************** Add , Edit , Delete Vender Services ***************************************

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Vender_SetServices(request):       #Show Vender Services
    try:
        data = request.data
        vender_id = data.get('id',None)
        user_obj = MyUser.objects.get(id = vender_id)

        vender_obj = VendorDetails.objects.get(fk_user = user_obj)  # Vender Details table object
        if VenderServices.objects.filter(fk_vendor = vender_obj).exists():
            service = VenderServices.objects.filter(fk_vendor = vender_obj).values('id','fk_vendor','fk_category','fk_category__category_name','fk_service','fk_service__service_name','fk_service__service_image','price','hour')
            # facility = VenderFacility.objects.filter(fk_vender_service__fk_vendor = vender_obj).values('id','fk_vender_service','fk_vender_facility','fk_vender_facility__facility_name')
            
            # facility = VenderFacility.objects.filter(fk_vender_service__fk_vendor = vender_obj).values('fk_vender_service__id','fk_vender_service__fk_category','fk_vender_service__fk_category__category_name','fk_vender_service__fk_category__category_image','fk_vender_service__fk_service','fk_vender_service__fk_service__service_name','fk_vender_service__fk_service__service_image','fk_vender_service__price','fk_vender_service__hour',)
            
            # services = service
            # for i in services: 
                # temp_list = []
                # temp_data = VenderFacility.objects.filter(fk_vender_service__fk_vendor = vender_obj, fk_vender_service=i['id']).values('id','fk_vender_service','fk_vender_facility','fk_vender_facility__facility_name')
                # data = [{'id': d['id'], 'fk_vender_service': d['fk_vender_service'], 'fk_vender_facility':d['fk_vender_facility'],'fk_vender_facility__facility_name':d['fk_vender_facility__facility_name']} for d in temp_data]
                # print(type(data))
                # temp_list.append(data)
                # i['vender_services'] = temp_list 
              
            # print(services)
                
            temp_dict = {}
            # temp_dict['vender_service'] = service
            
            # temp_dict['vender_service'].append(facility)
            temp_dict['vender_service'] = service
            return Response({'status':200,'msg':'Vender Services List.','payload':temp_dict})
        else:
            return Response({'status':403,'msg':'Something went wrong.'})

    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Vender_Add_Services(request):   # Vender Add Services
    try:
        data = request.data
        vender_id = data.get('vender_id',None)
        category_id = data.get('category_id',None)
        service_id = data.get('service_id',None)
        facility_id_list = data.get('facility_id_list',None)
        price = data.get('price',None)
        hour = data.get('hour',None)

        facility_id = json.loads(facility_id_list) # convert json data into dictionary

        user_obj = MyUser.objects.get(id = vender_id)  # Vender Details table object
        vender_obj = VendorDetails.objects.get(fk_user = user_obj)
        print(vender_obj)
        category_obj = CategoryMaster.objects.get(id = category_id) # CategoryMaster object
        service_obj = ServiceMaster.objects.get(id = service_id)  # Service Master Object

        if VenderServices.objects.filter(fk_vendor__fk_user__id = vender_id, fk_service__id = service_id).exists():
            return Response({'status':403,'msg':'Service already Added.'})
        else:
            VenderServices.objects.create(fk_vendor = vender_obj, fk_category = category_obj, fk_service = service_obj,price = price , hour = hour)
            vender_service_obj = VenderServices.objects.get(fk_vendor = vender_obj,fk_service = service_obj)  # Vender Services object
            for k in facility_id:
                service_facility_obj = ServiceFacility.objects.get(id = k)  # Service Facility object
                VenderFacility.objects.create(fk_vender_service = vender_service_obj , fk_vender_facility = service_facility_obj)
        VendorDetails.objects.filter(id = vender_obj.id).update(is_service_created = True)
        return Response({'status':200,'msg':'Service Added Successfully.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Edit_Vendor_Services(request):     #Edit Services Api
    try:
        data = request.data
        data_id = data.get('data_id',None)
        vendor_id = data.get('vender_id',None)
        category_id = data.get('category_id',None)
        service_id = data.get('service_id',None)
        facility_id_list = data.get('facility_id_list',None)
        price = data.get('price',None)
        hour = data.get('hour',None)

        facility_list = json.loads(facility_id_list)

        user_obj = MyUser.objects.get(id = vendor_id)


        vender_obj = VendorDetails.objects.get(fk_user = user_obj)

        category_obj = CategoryMaster.objects.get(id = category_id)
        service_obj = ServiceMaster.objects.get(id = service_id)

        if VenderServices.objects.filter(fk_vendor = vender_obj,fk_category = category_obj, fk_service = service_obj).exclude(id=data_id).exists():
            return Response({'status':403,'msg':'Already Added.'})
        else:
            VenderServices.objects.filter(id = data_id).update(fk_vendor = vender_obj , fk_category = category_obj , fk_service = service_obj, price = price, hour = hour)
            vender_service_obj = VenderServices.objects.get(fk_vendor = vender_obj, fk_service = service_obj)
            
            data = VenderFacility.objects.filter(fk_vender_service = vender_service_obj).delete()
            
            
            for k in facility_list:
                service_facility_obj = ServiceFacility.objects.get(id = k)  # Service Facility object
                print(service_facility_obj)
                print(vender_service_obj)
                
                
                VenderFacility.objects.update_or_create(fk_vender_service = vender_service_obj,fk_vender_facility = service_facility_obj)
            return Response({'status':200,'msg':'Service Updated Successfully.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Delete_Vendor_Services(request):   #Delete Services Api
    try:
        data = request.data
        data_id = data.get('id',None)
        vendor_id = data.get('vendor_id',None)
        VenderServices.objects.get(id = data_id).delete()
        vendor_obj = MyUser.objects.get( id = vendor_id)
        print(vendor_obj)
        if VenderServices.objects.filter(fk_vendor__fk_user = vendor_obj).exists():
            return Response({'status':200,'msg':'Service Deleted Successfully.'})
        else:
            VendorDetails.objects.filter(fk_user = vendor_obj).update(is_service_created = False)
            return Response({'status':200,'msg':'Service Deleted Successfully.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})

#********************************** End Vender Service *****************************************

#********************************** Set Vendor Schedule Api **********************************


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def show_set_schedule(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)

        user_obj = MyUser.objects.get(id = vendor_id)
        vendor_obj = VendorDetails.objects.get(fk_user = user_obj)

        schedule = VendorDetails.objects.filter(fk_user = user_obj).values('is_monday','is_tuesday','is_wednesday','is_thursday','is_friday','is_saturday','is_sunday','from_time','to_time','is_set_status')

        return Response({'status':200,'msg':'Vendor Schedule','payload':list(schedule)})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong'})



class UserDetailInfo(generics.GenericAPIView):

    def post(self,request):
        try:
            data = request.data
            vendor_data = data.get('data',None)
            vendor_id = data.get('vendor_id',None)
            
            user_obj = MyUser.objects.get(id = vendor_id)

            vendor_obj = VendorDetails.objects.get(fk_user = user_obj)
            # data_list = json.loads(vendor_data)
            print(vendor_data['is_monday'])

            VendorDetails.objects.filter(id = vendor_obj.id).update(is_monday = vendor_data['is_monday'] ,is_tuesday = vendor_data['is_tuesday'], is_wednesday = vendor_data['is_wednesday'] , is_thursday = vendor_data['is_thursday'] , is_friday = vendor_data['is_friday'] , is_saturday = vendor_data['is_saturday'] , is_sunday = vendor_data['is_sunday'], from_time = vendor_data['from_date'] , to_time = vendor_data['to_date'],is_set_status=True)


            return Response({'status':200,'msg':'Your schedule updated successfully.'})

        except:
            traceback.print_exc()
            return Response({'status':403,'msg':'Something went wrong'})

    

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def vendor_facility(request):
    try:
        data = request.data
        user_id = data.get('vendor_id',None)
        service_id = data.get('service_id',None)
        
        user_obj = MyUser.objects.get( id = user_id)
        vendor_obj = VendorDetails.objects.get( fk_user = user_obj)
        service_obj = ServiceMaster.objects.get( id = service_id)
        
        vender_service_obj = VenderServices.objects.get(fk_vendor = vendor_obj , fk_service = service_obj)
        
        print(vender_service_obj)
        facility = VenderFacility.objects.filter(fk_vender_service = vender_service_obj).values('id','fk_vender_service','fk_vender_facility','fk_vender_facility__facility_name')
        
        return Response({'status':200, 'msg':'Vendor Facility List','vendor_facility':list(facility)})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong'})
#********************************** End Vendor Schedule Api **********************************

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Order_to_Vendor(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        order_status = data.get('order_status',None)
        
        user_obj = MyUser.objects.get( id = vendor_id)
        vendor_obj = VendorDetails.objects.get( fk_user = user_obj)
        
        if order_status == "Pending" or order_status == "Started" or order_status == "Accepted" or order_status == "Cancelled" or order_status == "Completed":
            
            order_obj = OrderDetails.objects.filter( fk_vendor = vendor_obj,order_status = order_status).order_by('-id')
            
            order_details = OrderDetails.objects.filter(fk_vendor = vendor_obj , order_status = order_status ).order_by('-id').values('id','order_id','fk_vendor','fk_customer','fk_customer__name','duration','customer_city','customer_country','address','lat','lng','zip_code','vendor_pay_amount','order_status')
             
            for k in order_details:
                temp_dict = {}
                service_list = []
                order_service = OrderService.objects.filter(fk_order__id = k['id']).order_by('-id')
                for j in order_service:
                    # data = { 'service_name':j.fk_service.fk_service.service_name}
                    service_list.append(j.fk_service.fk_service.service_name)
                temp_dict['service_name'] = service_list
                    
                k['service'] = temp_dict
            return Response({'status':200,'msg':'Show Vendor Order.','payload':order_details})
        else:
            return Response({'status':403,'msg':'Order status not found'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})




@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Order_Accept_Decline(request):
    try:
        data = request.data
        sid = data.get('id',None)
        order_id = data.get('order_id',None)
        order_status = data.get('order_status',None)
        customer_id = data.get('customer_id',None)
        stripe.api_key = "sk_test_51LHr4UI0Jl0TyufY5lwPfz7zMPSPYd0MUZ7FhDN9n7bCIA7XNqB6G6PlQdVd0lmdrxxoEUg7zXYg2XLIRcPo9c1B00oT6zqkeT"
        
        order_obj = OrderDetails.objects.get(id = sid , order_id = order_id)
        OrderDetails.objects.filter( id = sid , order_id = order_id).update(order_status = order_status)
        Send_Message(customer_id , order_status , sid,order_obj.fk_vendor.full_name)
        if order_status == "Rejected":
            refund = stripe.Refund.create(payment_intent=order_obj.payment_intent_id, amount=(int((str(order_obj.total_amount).split('.'))[0])) * 100)
            OrderDetails.objects.filter( id = sid , order_id = order_id).update(stripe_refund_id = refund['id'] , stripe_refund_txtid = refund['balance_transaction'] , stripe_refund_status = refund['status'])
            return Response({'status':200,'msg':'You have miss an opportunity!.'})
        elif order_status == "Cancelled":
            refund = stripe.Refund.create(payment_intent=order_obj.payment_intent_id, amount = (int((str(order_obj.total_amount).split('.'))[0])) * 100)
            OrderDetails.objects.filter( id = sid , order_id = order_id).update(stripe_refund_id = refund['id'] , stripe_refund_txtid = refund['balance_transaction'] , stripe_refund_status = refund['status'])
            return Response({'status':200,'msg':'Order '+(order_status)+' Successfully.'})
        else:
            return Response({'status':200,'msg':'Order '+(order_status)+' Successfully.'})
        
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
        


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Order_Start_Job(request):
    try:
        data = request.data
        sid = data.get('id',None)
        order_id = data.get('order_id',None)
        order_status = data.get('order_status',None)
        customer_id = data.get('customer_id',None)
        vendor_id = data.get('vendor_id',None)
        if OrderDetails.objects.filter(fk_vendor__fk_user__id = vendor_id ,order_status = order_status).exists():
            return Response({'status':403,'msg':'You have already started job.Please complete your previous job and start a new job.'})
        else:
            OrderDetails.objects.filter( id = sid , order_id = order_id).update(order_status = order_status)
            vendor_obj = VendorDetails.objects.get(fk_user__id = vendor_id)
            Send_Message(customer_id , order_status , sid,vendor_obj.full_name)
            return Response({'status':200,'msg':'You are ready to start new job.'})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})
        


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Running_Job(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        
        user_obj = MyUser.objects.get(id = vendor_id)
        vendor_obj = VendorDetails.objects.get(fk_user = user_obj)
        # order_obj = OrderDetails.objects.filter( fk_vendor = vendor_obj,order_status = "Started")
            
        order_details = OrderDetails.objects.filter(fk_vendor = vendor_obj , order_status = "Started" ).order_by('-id').values('id','order_id','fk_vendor','fk_customer','fk_customer__name','duration','customer_city','customer_country','lat','lng','zip_code','address','vendor_pay_amount','order_status')
        
        for k in order_details:
            temp_dict = {}
            service_list = []
            order_service = OrderService.objects.filter(fk_order__id = k['id'])
            for j in order_service:
                # data = { 'service_name':j.fk_service.fk_service.service_name}
                service_list.append(j.fk_service.fk_service.service_name)
            temp_dict['service_name'] = service_list
                
            k['service'] = temp_dict
        
        return Response({'status':200,'msg':'Show Running Jobs.','payload':order_details})
        
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})     
        

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Vendor_Detail_Order(request):
    try:
        data = request.data
        sid = data.get('id',None)
        order_id = data.get('order_id',None)
        
        order_data =OrderDetails.objects.filter( id = sid).values('id','order_id','fk_category__category_name','fk_customer','fk_vendor','booking_start_time','order_status','booking_date','address')
        order_service = OrderService.objects.filter(fk_order__id = sid).values('fk_service__fk_service__service_name','fk_service__fk_service__service_image','fk_service__price','fk_service__hour')
        customer_details = OrderDetails.objects.filter(id = sid ,order_id = order_id).values('fk_customer__name')
        payment_information = OrderDetails.objects.filter( id = sid).values('sub_total','vendor_pay_amount','duration','vendor_convenience_fee','quantity')
        
        payload ={'order_data':order_data[0],
        'order_service':order_service,
        'customer_details':customer_details[0],
        'payment_information':payment_information[0]}
        
        return Response({'status':200,'msg':'Order Detailed.','payload':payload})
    except:
        print(traceback.print_exc())
        return Response({'status':403,'msg':'Something went wrong.'})    

#********************  Mobile App Send Nofification function ***************************** 

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
        

def Send_Message(customer_id , status ,ord_id,title):
    user_obj = MyUser.objects.get(id = customer_id)
    
    ord_obj = OrderDetails.objects.get(id = ord_id)
    token_list = []
    token = user_obj.firebase_token
    if token:
        token_list.append(str(token)) 
    else:
        pass
    message_title = "Doorap"
    order_status = ""
    user_type = ""
    cur_date_time = datetime.datetime.now()
    if status =="Accepted":
        message_body = "Dear " + str(user_obj.name)+ " We would gladly like to inform you that your order has been "+status
        user_type = "Customer"
        Notifications.objects.create(fk_user = user_obj , fk_order = ord_obj ,  notification = message_body, notification_date = cur_date_time , user_type = user_type,title_name = title)
        order_status = "Accepted"
        
    elif status == "Cancelled":
        message_body = "Dear " + str(user_obj.name)+ " We are sorry to inform you that your order has been " +status +" by vendor."
        user_type = "Customer"
        Notifications.objects.create(fk_user = user_obj , fk_order = ord_obj , notification = message_body, notification_date = cur_date_time , user_type = user_type,title_name = title)
        order_status = "Cancelled"
        
    elif status == "Rejected":
        message_body = "Dear " + str(user_obj.name)+ " We are sorry to inform you that your order has been " +status +" by vendor."
        user_type = "Customer"
        Notifications.objects.create(fk_user = user_obj , fk_order = ord_obj , notification = message_body, notification_date = cur_date_time , user_type = user_type,title_name = title)
        order_status = "Rejected"
        
    elif status == "Started":
        message_body = "Dear " + str(user_obj.name)+ " We would gladly like to inform you that your order has been "+status
        order_status = "Started"
        user_type = "Customer"
        Notifications.objects.create(fk_user = user_obj , fk_order = ord_obj , notification = message_body, notification_date = cur_date_time , user_type = user_type,title_name = title)
        
    else:
        order_status = "Started"
        user_type = "Customer"
        message_body = "Dear " + str(user_obj.name)+ " We would gladly like to inform you that your order has been "+status
        Notifications.objects.create(fk_user = user_obj , fk_order = ord_obj , notification = message_body, notification_date = cur_date_time , user_type = user_type,title_name = title)
    data_message = {
        'title':message_title,
        "body":message_body,
        "order_status":order_status,
        "user_type":user_type,
        "action":"Home",
        "action_id":str(user_obj.id),
        "current_datetime":str(datetime.datetime.now()).split(".")[0],
        "image_url":"",
        
        "android_channel_id": "noti_push_app_2",
        "sound": "alarm.mp3",
        "click_action": "FLUTTER_NOTIFICATION_CLICK",
    }
    res = send_notification(token_list, message_title, message_body, data_message,order_status,user_type)
    print("notification responsre..................",res)
               
               
               
#******************************************** Test Social login api ************************************
@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def get_otp_Social(request):
    try:
        data = request.data
        email = data.get('email', None)
        print("---------------")
        if (email == "" or email==None):
            return Response({'status': 403, "msg": 'Please check your request keys.'})
        elif MyUser.objects.filter(email=data['email']).exists():
            user_obj = MyUser.objects.get(email = email)
            if user_obj.is_vendor == True and user_obj.is_customer == True:
                return Response({'status': 403,  "msg": 'This Email already registered as Vendor and Customer..'})
            
            elif user_obj.is_vendor == True and user_obj.login_id == None and user_obj.login_type == None:
                temp_dict = {}
                temp_dict["otp"] = 0
                temp_dict["signup_msg"] = "This email is associated with Vendor. Do you want to continue as Customer?."
                temp_dict["is_vendor"] = "True"
                temp_dict["is_customer"] = "False"
                temp_dict['login_id'] = "" if user_obj.login_id == None else user_obj.login_id
                temp_dict['login_type'] = "" if user_obj.login_type == None else user_obj.login_type
                return Response({'status': 200,"msg":"","payload":temp_dict})
            elif user_obj.is_customer == True and user_obj.login_id == None and user_obj.login_type == None:
                temp_dict = {}
                temp_dict["otp"] = 0
                temp_dict["signup_msg"] = "This email is associated with Customer. Do you want to continue as Vendor?."
                temp_dict["is_vendor"] = "False"
                temp_dict["is_customer"] = "True"
                temp_dict['login_id'] = "" if user_obj.login_id == None else user_obj.login_id
                temp_dict['login_type'] = "" if user_obj.login_type == None else user_obj.login_type
                return Response({'status': 200,"msg":"","payload":temp_dict})
            else:
                
                if user_obj.is_vendor == True and user_obj.login_type == "Facebook":
                    temp_dict = {}
                    temp_dict["otp"] = 0
                    temp_dict["signup_msg"] = "This email is associated with Vendor as Facebook. Do you want to continue as Customer?."
                    temp_dict["is_vendor"] = "True"
                    temp_dict["is_customer"] = "False"
                    temp_dict['login_id'] = "" if user_obj.login_id == None else user_obj.login_id
                    temp_dict['login_type'] = "" if user_obj.login_type == None else user_obj.login_type
                    return Response({'status': 200,"msg":"","payload":temp_dict})
                elif user_obj.is_vendor == True and  user_obj.login_type == "Google":
                    temp_dict = {}
                    temp_dict["otp"] = 0
                    temp_dict["signup_msg"] = "This email is associated with Vendor as Google. Do you want to continue as Customer?."
                    temp_dict["is_vendor"] = "True"
                    temp_dict["is_customer"] = "False"
                    temp_dict['login_id'] = "" if user_obj.login_id == None else user_obj.login_id
                    temp_dict['login_type'] = "" if user_obj.login_type == None else user_obj.login_type
                    return Response({'status': 200,"msg":"","payload":temp_dict})
                elif user_obj.is_vendor == True and user_obj.login_type == "Apple":
                    temp_dict = {}
                    temp_dict["otp"] = 0
                    temp_dict["signup_msg"] = "This email is associated with Vendor as Apple. Do you want to continue as Customer?."
                    temp_dict["is_vendor"] = "True"
                    temp_dict["is_customer"] = "False"
                    temp_dict['login_id'] = "" if user_obj.login_id == None else user_obj.login_id
                    temp_dict['login_type'] = "" if user_obj.login_type == None else user_obj.login_type
                    return Response({'status': 200,"msg":"","payload":temp_dict})
                elif user_obj.is_customer == True and user_obj.login_type == "Facebook" :
                    temp_dict = {}
                    temp_dict["otp"] = 0
                    temp_dict["signup_msg"] = "This email is associated with Customer as Facebook. Do you want to continue as Vendor?."
                    temp_dict["is_vendor"] = "False"
                    temp_dict["is_customer"] = "True"
                    temp_dict['login_id'] = "" if user_obj.login_id == None else user_obj.login_id
                    temp_dict['login_type'] = "" if user_obj.login_type == None else user_obj.login_type
                    return Response({'status': 200,"msg":"","payload":temp_dict})
                elif user_obj.is_customer == True and user_obj.login_type == "Google":    
                    temp_dict = {}
                    temp_dict["otp"] = 0
                    temp_dict["signup_msg"] = "This email is associated with Customer as Google. Do you want to continue as Vendor?."
                    temp_dict["is_vendor"] = "False"
                    temp_dict["is_customer"] = "True"
                    temp_dict['login_id'] = "" if user_obj.login_id == None else user_obj.login_id
                    temp_dict['login_type'] = "" if user_obj.login_type == None else user_obj.login_type
                    return Response({'status': 200,"msg":"","payload":temp_dict})
                elif user_obj.is_customer == True and user_obj.login_type == "Apple":    
                    temp_dict = {}
                    temp_dict["otp"] = 0
                    temp_dict["signup_msg"] = "This email is associated with Customer as Apple. Do you want to continue as Vendor?."
                    temp_dict["is_vendor"] = "False"
                    temp_dict["is_customer"] = "True"
                    temp_dict['login_id'] = "" if user_obj.login_id == None else user_obj.login_id
                    temp_dict['login_type'] = "" if user_obj.login_type == None else user_obj.login_type
                    return Response({'status': 200,"msg":"","payload":temp_dict})
                    
                else:
                    temp_dict = {}
                    temp_dict["otp"] = 0
                    temp_dict["signup_msg"] = "This email is associated with Customer as Google. Do you want to continue as Vendor?."
                    temp_dict["is_vendor"] = "False"
                    temp_dict["is_customer"] = "True"
                    temp_dict['login_id'] = "" 
                    temp_dict['login_type'] = "" 
                    return Response({'status': 200,"msg":"","payload":temp_dict})
        else:
            temp_dict = {}
            otp = random.randint(1000,9999)
            send_mail('Doorap Account Verification', f'Your OTP is {otp}.\nUse this OTP to complete your Account Verification.\nNote: Please do not share your OTP or password with anyone.\nIf you have any questions or if we can further assist you in any way, please feel free email us at noreplydoorap@gmail.com\nThank You,\nTeam Doorap', settings.EMAIL_HOST_USER, [email])
            temp_dict['otp'] = otp
            temp_dict["signup_msg"] = ""

            return Response({'status': 200, "msg": 'OTP Sent Successfully.', 'payload': temp_dict})
    except BaseException as e:
        traceback.print_exc()
        return Response({'status': 403, "msg": 'Something went wrong.'})






@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def social_sign_up(request):
    try:
        data = request.data
        name = data.get('name', None)
        email = data.get('email', None)
        password = data.get('password',None)
        firebase_token = data.get('firebase_token', None)
        is_vendor1 = data.get('is_vendor', None)
        is_customer1 = data.get('is_customer',None)
        
        if MyUser.objects.filter(email = email,is_vendor = True).exists():
            print("***********************",data)
            user_obj = MyUser.objects.get(email=email)
            serializer1 = CustomerSignUpSocial(user_obj,data = data)
            if serializer1.is_valid():

                serializer1.save()

                #generate token
                temp_obj = MyTokenObtainPairSerializer()
                token = temp_obj.validate(user_obj)

                temp_dict = {}
                temp_dict['id'] = serializer1.data.get('id',None)
                temp_dict['email'] = serializer1.data.get('email',None)
                temp_dict['firebase_token'] = serializer1.data.get('firebase_token',None)
                temp_dict['password'] = serializer1.data.get('password',None)
                temp_dict['api_token'] = token

                return Response({'status': 200, "msg": 'SignUp successfully.', 'payload': temp_dict})
            else:
                print(serializer1.errors)
                return Response({'status': 403, "msg": 'Something went wrong.'})
        elif MyUser.objects.filter(email = email , is_customer = True):
            print("-------------")
            user_obj = MyUser.objects.get(email=email)
            print(data)
            serializer1 = VenderSignUpSocial(user_obj,data = data)
            if serializer1.is_valid():
                serializer1.save()

                #generate token
                temp_obj = MyTokenObtainPairSerializer()
                token = temp_obj.validate(user_obj)

                temp_dict = {}
                temp_dict['id'] = serializer1.data.get('id',None)
                temp_dict['email'] = serializer1.data.get('email',None)
                temp_dict['firebase_token'] = serializer1.data.get('firebase_token',None)
                temp_dict['password'] = serializer1.data.get('password',None)
                temp_dict['api_token'] = token


                return Response({'status': 200, "msg": 'SignUp successfully.', 'payload': temp_dict})
            else:
                print(serializer1.errors)
                return Response({'status': 403, "msg": 'Something went wrong.'})
        else:
            print("######################")
            if(email == "" or email == None) or (name == "" or name == None)  or (firebase_token == "" or firebase_token == None) or (is_vendor1 == "" or is_vendor1 == None) or (is_customer1 == "" or is_customer1 == None):
                return Response({'status':403, "msg":'Please check your request keys.'})
            else:
               
                # serializer1 = MyUserSerializerTest(data = data, context={'login_id':data['login_id'], 'login_type':data['login_type']})
                
                serializer1 = MyUserSerializerTest(data = data)
                if serializer1.is_valid():
                    serializer1.save()
                    
                    
                    user_obj = MyUser.objects.get(email = email)
                    temp_obj = MyTokenObtainPairSerializer()
                    token = temp_obj.validate(user_obj)
                    temp_dict = {}
                    temp_dict['id'] = serializer1.data.get('id',None)
                    temp_dict['email'] = serializer1.data.get('email',None)
                    temp_dict['firebase_token'] = serializer1.data.get('firebase_token',None)
                    temp_dict['password'] = serializer1.data.get('password',None)
                    
                    temp_dict['api_token'] = token

                    return Response({'status': 200, "msg": 'SignUp successfully.', 'payload': temp_dict})
                else:
                    print(serializer1.errors)
                    return Response({'status': 403, "msg": 'Something went wrong.'})
    except BaseException as e:
        traceback.print_exc()
        return Response({'status': 403, "msg": 'Something went wrong.'})
        
        


@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def Vender_login_social(request):
    try:
        data = request.data
        email = data.get('email',None)
        password = data.get('password',None)
        firebase_token = data.get('firebase_token',None)
        login_type = data.get('login_type')
        login_id = data.get('login_id')
        temp_dict = {}
        if login_type != "" and login_type != "":
            print("**************** Social login **********************")
            if MyUser.objects.filter(login_id = login_id , login_type = login_type).exists():
                MyUser.objects.filter(email = email).update(firebase_token = firebase_token)
                user_obj = MyUser.objects.get(email = email)
                temp_obj = MyTokenObtainPairSerializer()
                token = temp_obj.validate(user_obj)
                temp_dict['id'] = user_obj.id
                temp_dict['name'] = user_obj.name
                temp_dict['email'] = user_obj.email
                temp_dict['firebase_token'] = user_obj.firebase_token
                temp_dict['is_vendor'] = user_obj.is_vendor
                temp_dict['is_customer'] = user_obj.is_customer
                temp_dict['is_profile_create'] = user_obj.is_profile_create
                temp_dict['api_token'] = token
                return Response({'status': 200, "msg": 'Logged In successfully.', 'payload': temp_dict})
            else:
                return Response({'status':403,'msg':'Invalid User'})
        else:
            print("---------------------")
            try:
                serializer = MyUserLoginSerializerSocial(data = data)
                if serializer.is_valid(raise_exception = True):
                    
                    user_obj = MyUser.objects.get(email = email)
                    temp_obj = MyTokenObtainPairSerializer()
                    token = temp_obj.validate(user_obj)

                    
                    if serializer.data.get('is_vendor',None) == True and serializer.data.get('is_customer',None) == True:
                        print("*****************1")
                        vender = serializer.data.get('is_vendor',None)
                        user_id = MyUser.objects.get(id = serializer.data.get('id',None))

                        temp_dict['id'] = serializer.data.get('id',None)
                        temp_dict['name'] = serializer.data.get('name',None)
                        temp_dict['email'] = serializer.data.get('email',None)
                        temp_dict['firebase_token'] = serializer.data.get('firebase_token',None)
                        temp_dict['is_vendor'] = serializer.data.get('is_vendor',None)
                        temp_dict['is_customer'] = serializer.data.get('is_customer',None)
                        temp_dict['is_profile_create'] = user_id.is_profile_create
                        temp_dict['api_token'] = token
                        return Response({'status': 200, "msg": 'Logged In successfully.', 'payload': temp_dict})
                    elif serializer.data.get('is_vendor',None) == True:
                        print("*****************2")
                        vender = serializer.data.get('is_vendor',None)
                        user_id = MyUser.objects.get(id = serializer.data.get('id',None))

                        temp_dict['id'] = serializer.data.get('id',None)
                        temp_dict['name'] = serializer.data.get('name',None)
                        temp_dict['email'] = serializer.data.get('email',None)
                        temp_dict['firebase_token'] = serializer.data.get('firebase_token',None)
                        temp_dict['is_vendor'] = serializer.data.get('is_vendor',None)
                        temp_dict['is_customer'] = serializer.data.get('is_customer',None)
                        temp_dict['is_profile_create'] = user_id.is_profile_create
                        temp_dict['api_token'] = token
                        return Response({'status': 200, "msg": 'Logged In successfully.', 'payload': temp_dict})
                    elif serializer.data.get('is_customer',None) == True:
                        print("*****************3")
                        vender = serializer.data.get('is_vendor',None)
                        user_id = MyUser.objects.get(id = serializer.data.get('id',None))
                        temp_dict['id'] = serializer.data.get('id',None)
                        temp_dict['name'] = serializer.data.get('name',None)
                        temp_dict['email'] = serializer.data.get('email',None)
                        temp_dict['firebase_token'] = serializer.data.get('firebase_token',None)
                        temp_dict['is_vendor'] = serializer.data.get('is_vendor',None)
                        temp_dict['is_customer'] = serializer.data.get('is_customer',None)
                        temp_dict['is_profile_create'] = user_id.is_profile_create
                        temp_dict['api_token'] = token
                        return Response({'status': 200, "msg": 'Logged In Successfully.', 'payload': temp_dict})
                    else:
                        pass
                else:
                    return Response({"status": 403, "msg": 'Login failed'})
            except ValidationError as e:
                traceback.print_exc()
                return Response({"status": 403, "msg": 'Invalid credentials'})
            except:
                traceback.print_exc()
                return Response({"status": 403, "msg": 'Invalid credentials'})
    except:
        traceback.print_exc()
        return Response({'status':403, "msg":'Something went wrong'})



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Withdraw_Request(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        withdraw_amount = request.data['withdraw_amount']
        vendor_obj = VendorDetails.objects.get( fk_user__id = vendor_id)
        total_withdraw_amount = withdraw_amount + vendor_obj.withdraw_request
        VendorDetails.objects.filter(fk_user__id = vendor_id).update(withdraw_request = total_withdraw_amount , withdraw_request_status = True , withdraw_request_date =datetime.datetime.now())
        Vendor_Withdraw_Payment.objects.create(fk_vendor = vendor_obj,payment_amount = withdraw_amount,withdraw_request_date=  datetime.datetime.now())
        
        return Response({'status':200,"msg":'Withdraw request send successfully.'})
    except:
        traceback.print_exc()
        return Response({'status':403,"msg":"Something went wrong."})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Vendor_TotalEarning(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        vendor_obj = VendorDetails.objects.get(fk_user__id = vendor_id)
        temp_dict ={}
        if VendorDetails.objects.filter(fk_user__id = vendor_id ,withdraw_request_status = True).exists():
            temp_dict['total_balance'] = vendor_obj.vendor_earning
            temp_dict['withdraw_msg'] = f"Withdraw Request Pending of ${vendor_obj.withdraw_request}."
            temp_dict['withdraw_request_status'] = vendor_obj.withdraw_request_status
            return Response({'status':200,"msg":"Total Balance",'payload':temp_dict})
        else:
            temp_dict['total_balance'] = vendor_obj.vendor_earning
            temp_dict['withdraw_msg'] = ""
            temp_dict['withdraw_request_status'] = vendor_obj.withdraw_request_status
            return Response({'status':200,"msg":"Total Balance",'payload':temp_dict})
    except:
        traceback.print_exc()
        return Response({'status':403,"msg":"Something went wrong."})
   

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
@csrf_exempt
def Show_Received_Payment(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id',None)
        received_payment = Vendor_Withdraw_Payment.objects.filter(fk_vendor__fk_user__id = vendor_id , withdraw_status = "Accepted").values('fk_vendor__full_name','payment_receive_date','payment_amount')
        return Response({'status':200,"msg":"Received Payment.",'payload':list(received_payment)})
    except:
        traceback.print_exc()
        return Response({'status':403,'msg':'Something went wrong.'})    



#**************************************** ***************************************** ***************************