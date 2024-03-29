from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import traceback
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control
import datetime
import requests
import json
import ast
from django.http import HttpResponse
from django.template.loader import render_to_string
import stripe
import calendar
def Login_page(request):
    return render(request,'admin_panel/login.html')

@csrf_exempt
def Login(request):
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')            
            if AdminDetails.objects.filter(email = email, password = password).exists(): #check user exists
                request.session['email'] = email
                return JsonResponse({"status":"1","msg":"Login Successfull."})
            else:
                return JsonResponse({"status":"0","msg":"Invalid Credential."})
        else:
            return JsonResponse({"status":"0","msg":"Something went wrong."})
    except:
        print(traceback.print_exc())
        return JsonResponse({"status":"0","msg":"Something went wrong."})
        
def logout(request):
    try:
        if request.session.get('email'):
            print(request.session.get('email'))
            del request.session['email']
            return redirect('/')
        else:
            return redirect('/')
    except:
        return JsonResponse({"status":"0","msg":"Something went wrong."})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Dashboard(request):
    if request.session.get('email'):
        count_customer = MyUser.objects.filter(is_customer = True).count()
        
        
        pending = VendorDetails.objects.filter(user_status = "Pending").count()
        approve = VendorDetails.objects.filter(user_status = "Approve").count()
        reject = VendorDetails.objects.filter(user_status = "Reject").count()
        count_vendor = MyUser.objects.filter(is_vendor = True).count()
        
        today_date = datetime.datetime.today().replace(day=1)
        date = datetime.datetime.date(today_date)
        end_date = date.replace(day = calendar.monthrange(date.year, date.month)[1])
            
        income = 0
        revenue = 0
        
        orders = OrderDetails.objects.filter(current_booking_date__gte = today_date , current_booking_date__lte = end_date ,order_status = "Completed").order_by('-id')
        
        for i in orders:
            
            revenue = revenue + i.convenience_fee + i.vendor_convenience_fee
            
            income = i.total_amount + income
        
        context = {
            "customer":count_customer,
            "vendor":count_vendor,
            "pending":pending,
            "approve":approve,
            "reject":reject,
            "revenue":revenue,
            "income":income,
            "orders":orders.count()
            }
        return render(request,"admin_panel/dashboard.html",context)
    else:
        return redirect('/')
 
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def VenderListPage(request):
    if request.session.get('email'):
        user = MyUser.objects.filter(is_vendor = True).order_by('-created_datime')
        vendor = VendorDetails.objects.all()
        
        temp_list = []
        for j in user:
            
            if VendorDetails.objects.filter(fk_user__id = j.id , fk_user__is_vendor = True).exists():
                data =VendorDetails.objects.get(fk_user__id = j.id , fk_user__is_vendor = True)
                
                data = {
                "id":data.fk_user.id,
                "full_name":data.full_name,
                "business_name":data.business_name,
                "created_date":data.fk_user.created_datime,
                "mobile_no":data.mobile_no,
                "email":data.fk_user.email,
                "user_status":data.user_status,
                }
                temp_list.append(data)
            else:
                data = MyUser.objects.get(id = j.id,is_vendor = True)
                # print(data.email)
                data = {
                "id":data.id,
                "full_name":data.name,
                "business_name":"-",
                "created_date":data.created_datime,
                "mobile_no":"-",
                "email":data.email,
                "user_status":"-",
                }
                temp_list.append(data)
           
        # vender = VendorDetails.objects.all().order_by('full_name')
        context = {'vender':temp_list}
        return render(request,'admin_panel/vendor_list.html',context)
    else:
        return redirect('/')



        
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def CustomerListPage(request):
    if request.session.get('email'):
       customer = MyUser.objects.filter(is_customer = True).order_by('-created_datime')
       context = {'customer':customer}
       return render(request,'admin_panel/customer_list.html',context)
    else:
       return redirect('/')

@csrf_exempt
def DeleteCustomer(request):
    try:
        if request.method == "POST":
            sid = request.POST.get('id')
            if MyUser.objects.filter(id = sid,is_vendor = True , is_customer = True).exists():
                MyUser.objects.filter(id=sid).update(is_customer = False)
            elif MyUser.objects.filter(id = sid,is_vendor = False , is_customer = True).exists():
                MyUser.objects.filter(id =sid).delete()
            else:
                pass
            
            return JsonResponse({"status":"1","msg":"Account Deleted Successfully.."})
        else:
            return JsonResponse({"status":"0","msg":"Something went wrong."})
    except:
        return JsonResponse({"status":"0","msg":"Something went wrong."})

@csrf_exempt
def ApproveReject(request):
    try:
        if request.method == "POST":
            sid = request.POST.get('id')
            status = request.POST.get('status')
            cur_date_time = datetime.datetime.now()
            
            print("***************",cur_date_time)
            if status == "Approve":
                
                VendorDetails.objects.filter(fk_user__id=sid).update(user_status=status)
                vender_obj = VendorDetails.objects.get(fk_user__id=sid)
                email = vender_obj.fk_user.email
                # print(email)
                # print(vender_obj.fk_user.firebase_token)
                send_mail("Doorap",f'Dear {vender_obj.full_name},\nWe would gladly like to inform you that your account has been approved. Now you can login to your account.\nWe sincerely hope you enjoy using Doorap.\nIf you have any questions or if we can further assist you in any way, please feel free to email us at noreplydoorap@gmail.com\nThank You,\nTeam-Doorap', settings.EMAIL_HOST_USER,[email])
                
                
                # send Notification on mobile app
                token_list = []
                token = vender_obj.fk_user.firebase_token
                if token:
                    token_list.append(str(token))
                else:
                    pass
                message_title = "Doorap"
                # message_body = "Dear " + str(vender_obj.full_name)+ " We would gladly like to inform you that your account has been approved"
                message_body = "Dear Vendor, Congratulations! Your account is activated."
                order_status = "Approve"
                user_type = "Vendor"
                data_message = {
                    'title':message_title,
                    "body":message_body,
                    "order_status":order_status,
                    "user_type":user_type,
                    "action":"Home",
                    "action_id":str(vender_obj.id),
                    "current_datetime":str(datetime.datetime.now()).split(".")[0],
                    "image_url":"",
                    
                    "android_channel_id": "noti_push_app_2",
                    "sound": "alarm.mp3",
                    "click_action": "FLUTTER_NOTIFICATION_CLICK",
                }
                res = send_notification(token_list, message_title, message_body, data_message,order_status,user_type)
                Notifications.objects.create(fk_user = vender_obj.fk_user , notification = message_body , notification_date = cur_date_time , user_type = "Vendor" , title_name = vender_obj.full_name)
                print("notification responsre..................",res)
                
                # End Send nofication on mobile app code

                
                return JsonResponse({"status":"1","msg":"Status Changed Successfully.."})
            else:
                VendorDetails.objects.filter(fk_user__id=sid).update(user_status=status)
                vender_obj = VendorDetails.objects.get(fk_user__id=sid)
                email = vender_obj.fk_user.email
               
                send_mail("Doorap",f'Dear {vender_obj.full_name},\nWe are sorry to inform you that your account has  been rejected.\nWe sincerely hope you enjoy using Doorap.\nIf you have any questions or if we can further assist you in any way, please feel free to email us at noreplydoorap@gmail.com\nThank You,\n Team-Doorap', settings.EMAIL_HOST_USER,[email])
               
               
                # send Notification on mobile app
                token_list = []
                token = vender_obj.fk_user.firebase_token
                if token:
                    token_list.append(str(token))
                else:
                    pass
                message_title = "Doorap"
                order_status = "Reject"
                user_type = "Vendor"
                # message_body = "Dear " + str(vender_obj.full_name)+ " We are sorry to inform you that your account has  been rejected.."
                message_body = "Dear Vendor, Your account is rejected by administrator"
                data_message = {
                    'title':message_title,
                    "body":message_body,
                    "order_status":order_status,
                    "user_type":user_type,
                    "action":"Home",
                    "action_id":str(vender_obj.id),
                    "current_datetime":str(datetime.datetime.now()).split(".")[0],
                    "image_url":"",
                    
                    "android_channel_id": "noti_push_app_2",
                    "sound": "alarm.mp3",
                    "click_action": "FLUTTER_NOTIFICATION_CLICK",
                }
                res = send_notification(token_list, message_title, message_body, data_message,order_status,user_type)
                Notifications.objects.create(fk_user = vender_obj.fk_user, notification = message_body ,notification_date = cur_date_time , user_type = "Vendor",title_name = vender_obj.full_name)
                print("notification responsre..................",res)
                
                # End Send nofication on mobile app code
                
                
                
                return JsonResponse({"status":"1","msg":"Status Changed Successfully.."})
        return JsonResponse({"status":"0","msg":"Something went wrong."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0","msg":"Something went wrong."})       
        

#********************  Mobile App Send Nofification function ***************************** 

def send_notification(token_list, message_title, message_body, data_message,order_status,user_type):
    # print("message_body.........",message_body)
    # print("message_title...........",message_title)
    # print("token_list........",token_list)
    # print("data_message.....",data_message)
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
            print(response)
        return "success"
    except:
        print(str(traceback.format_exc()))
        return "error"
        
        
# def view_vendor(request,id):
    # return render(request, 'admin_panel/view_vendor.html')
        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_vendor(request,id):
    
    if request.session.get('email'):
        obj_vender = VendorDetails.objects.get(fk_user__id=id)
        categories = VenderServices.objects.filter(fk_vendor__fk_user__id=id).values('id','fk_category','fk_category__category_name','fk_service__service_name','price','hour')
        vendor_obj = VendorDetails.objects.filter(fk_user__id=id).last()
        temp = []
        main_dict = []
        count = 0
        for j in categories:
            service_dict = {}
            service_dict['category_name'] = j['fk_category__category_name']
            service_dict['service_name'] = j['fk_service__service_name']
            service_dict['price'] = j['price']
            service_dict['hour'] = j['hour']
            temp_list1 = []
            facility = VenderFacility.objects.filter(fk_vender_service__id = j['id']).values('fk_vender_facility__facility_name')
            for k in facility:
                temp_list1.append(k['fk_vender_facility__facility_name'])
            
            service_dict['facility_name'] = temp_list1
            temp.append(service_dict)
            
        # print("----------",temp)
        
        # for i in categories:
            # temp_dict = {}
            # services = VenderServices.objects.filter(fk_vendor=vendor_obj, fk_category__id=i['fk_category']).values('id','fk_service','fk_service__service_name').distinct()
            # temp_dict['category_name'] = i['fk_category__category_name']
            # temp_list = []
            # temp_list2 = []
            # for j in services:
                # temp_list.append([j['id'],j['fk_service__service_name']])
                
                # temp_dict['service'] = temp_list
            
            # if (len(temp_list) > 0):
                # data = VenderServices.objects.filter(id=temp_list[0][0])
                # for i in data:
                    # temp_dict['first_price'] = i.price
                    # temp_dict['first_hour'] = i.hour
            # else:
                # pass
                
                
            # if (len(temp_list) > 0):
                # facility = VenderFacility.objects.filter(fk_vender_service__id=temp_list[0][0])
                # temp_dict['first_facilities'] = [k.fk_vender_facility.facility_name for k in facility]
            # else:
                # temp_dict['first_facilities'] =  []
            
            # main_dict.append(temp_dict)
            
        
        
        return render(request,'admin_panel/view_vendor.html', {"main_dict":temp,'vendor_obj':vendor_obj, "obj_vender":obj_vender})
    else:
        return redirect('/')  
 
@csrf_exempt
def Delete_Vendor(request):
    try:
        if request.session.get('email'):
            if request.method == "POST":
                vendor_id = request.POST.get('vendor_id',None)
                if MyUser.objects.filter(id = vendor_id,is_vendor = True , is_customer = False).exists():
                    MyUser.objects.filter(id = vendor_id).delete()
                    VendorDetails.objects.filter(fk_user__id = vendor_id).delete()
                elif MyUser.objects.filter(id = vendor_id,is_vendor = True , is_customer = True).exists():
                    VendorDetails.objects.filter(fk_user__id = vendor_id).delete()
                    MyUser.objects.filter(id = vendor_id).update(is_vendor = False)
                else:
                    pass
                return JsonResponse({'status':'1','msg':'Account Deleted Successfully.'})
            else:
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
            return redirect('/')
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def test(request,id):
    
    if request.session.get('email'):
        obj_vender = VendorDetails.objects.get(id=id)
        categories = VenderServices.objects.filter(fk_vendor__id=id).values('fk_category','fk_category__category_name').distinct()
        vendor_obj = VendorDetails.objects.filter(id=id).last()
        temp = []
        main_dict = []
        count = 0
        # vender_fac = VenderFacility.objects.filter(fk_vender_service__fk_vendor__id = id)
        # for i in vender_fac:
            
            # print(i.fk_vender_service.fk_category.category_name)
            # print(i.fk_vender_service.fk_service.service_name)
            # print(i.fk_vender_facility.facility_name)
        
        
        for i in categories:
            temp_dict = {}
            services = VenderServices.objects.filter(fk_vendor=vendor_obj, fk_category__id=i['fk_category']).values('id','fk_service','fk_service__service_name').distinct()
            temp_dict['category_name'] = i['fk_category__category_name']
            temp_list = []
            temp_list2 = []
            for j in services:
                temp_list.append([j['id'],j['fk_service__service_name']])
                
                temp_dict['service'] = temp_list
            
            if (len(temp_list) > 0):
                data = VenderServices.objects.filter(id=temp_list[0][0])
                for i in data:
                    temp_dict['first_price'] = i.price
                    temp_dict['first_hour'] = i.hour
            else:
                pass
                
                
            if (len(temp_list) > 0):
                facility = VenderFacility.objects.filter(fk_vender_service__id=temp_list[0][0])
                temp_dict['first_facilities'] = [k.fk_vender_facility.facility_name for k in facility]
            else:
                temp_dict['first_facilities'] =  []
            
            main_dict.append(temp_dict)
            
        
        # print(main_dict);
        return render(request,'admin_panel/view_vendor.html', {"main_dict":main_dict,'vendor_obj':vendor_obj, "obj_vender":obj_vender})
    else:
        return redirect('/')  

@csrf_exempt
def show_vendor_facility(request):
    try:
        if request.session.get('email'):
            service_id = request.POST.get('service_id')
            facility = VenderFacility.objects.filter(fk_vender_service__id = service_id).values('fk_vender_facility__facility_name')
            service = VenderServices.objects.get( id = service_id)
            
            print(service.price, service.hour)
            return JsonResponse({'status':'1','msg':'Service Facility','data1':list(facility),'data2':service.price,'data3':service.hour})
        else:
            return redirect('/') 
    except:
        traceback.print_exc()
        return JsonResponse({'status':"0",'msg':'Something went wrong'})

       

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Customservice(request):
    if request.session.get('email'):
        obj2 = VenderCustomService.objects.all().values('fk_vendor', 'fk_vendor__full_name', 'fk_vendor__id' ).distinct()
        return render(request,'admin_panel/customservice.html',{"obj2":obj2})
    else:
        return redirect('/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def vendorCategories(request, id):
    if request.session.get('email'):
        categories = VenderCustomService.objects.filter(fk_vendor__id=id).values('fk_category','fk_category__category_name').distinct()
        vendor_obj = VendorDetails.objects.filter(id=id).last()
        
        # {'plumbing':{'service':[],'service2':[]}}
        
        main_dict = {}
        
        for i in categories:
            
            temp_dict = {}
            custom_services = VenderCustomService.objects.filter(fk_vendor=vendor_obj, fk_category__id=i['fk_category'])
            for j in custom_services:
                custom_facility = VenderCustomFacility.objects.filter(fk_custom_service=j)
                temp_list = []
                for k in custom_facility:
                    temp_list.append(k.custom_facility_name)
                temp_dict[j.custom_service_name] = temp_list
            main_dict[i['fk_category__category_name']] = temp_dict
            
        # print(main_dict)
        
        return render(request,'admin_panel/vendor_categories_tmeplate.html',{"main_dict":main_dict,'vendor_obj':vendor_obj})
    else:
        return redirect('/')   



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def custom_services_form(request,id):
    if request.session.get('email'):
        obj = VenderCustomService.objects.get(id = id)
        print("888888888",obj)
        obj= VenderCustomFacility.objects.filter(fk_custom_service = obj)
        
        dict1={}
        list=[]
        for i in obj:
          
            dict1["category"] = i.fk_custom_service.fk_category.category_name
            dict1["services"] = i.fk_custom_service.custom_service_name
            dict1["facility"] = i.custom_facility_name
         
        print("..........//", dict1)
        # obj_custom = VenderCustomService.objects.get(id=id)
        return render(request,'admin_panel/custom_services_form.html', 
        {"obj":dict1, "user_id":id})
    else:
        return redirect('/') 



@csrf_exempt
def add_facility(request):
    try:
        if request.method == "POST":
            facility = request.POST.get("facility")
            service_name = request.POST.get("service_name")
            vendor_id = request.POST.get("vendor_id")
            category_name = request.POST.get("category")
            
            vendor_obj = VendorDetails.objects.get( id = vendor_id)
            category_obj = CategoryMaster.objects.get(category_name = category_name)
            customer_service_obj = VenderCustomService.objects.get(fk_vendor = vendor_obj,fk_category = category_obj , custom_service_name = service_name)
            VenderCustomFacility.objects.create(custom_facility_name = facility,fk_custom_service = customer_service_obj)
            
            return JsonResponse({'status':'1','msg':'Facility Added Successfully.'})
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
        
@csrf_exempt
def add_to_master_data(request):
    try:
        if request.method == "POST":
            vendor_id = request.POST.get("vendor_id")
            category_name = request.POST.get('category')
            service_name = request.POST.get("service_name")
            
            category_obj = CategoryMaster.objects.get(category_name = category_name)  # category object
            vender_obj = VendorDetails.objects.get( id = vendor_id)                   # vendor object 
            obj_id = VenderCustomService.objects.get(fk_vendor = vender_obj , fk_category = category_obj,custom_service_name = service_name)     #vendor custom service object
            
            ServiceMaster.objects.create(fk_category = obj_id.fk_category, service_image = obj_id.custom_service_image ,service_name = obj_id.custom_service_name, service_price = obj_id.custom_service_price , service_time= obj_id.custom_service_time)
            
            service_obj = ServiceMaster.objects.get(fk_category = category_obj, service_name =obj_id.custom_service_name)   # service master object 
            
            # VenderServices.objects.create(fk_vendor = vender_obj, fk_category = service_obj.fk_category, fk_service = service_obj ,price = service_obj.service_price , hour = service_obj.service_time)
            
            
            # vendor_service_obj = VenderServices.objects.get(fk_vendor = vender_obj, fk_category = category_obj, fk_service = service_obj)  # vendor service object 
            
            # print(vendor_service_obj,".................")
            
            obj = VenderCustomFacility.objects.filter(fk_custom_service = obj_id) 
            for i in obj:
                ServiceFacility.objects.create(fk_service = service_obj, facility_name = i.custom_facility_name)
                
                # service_facility_obj = ServiceFacility.objects.get( fk_service = service_obj ,facility_name = i.custom_facility_name)
                
                # VenderFacility.objects.create(fk_vender_service = vendor_service_obj,fk_vender_facility = service_facility_obj) 
                i.delete()
            obj_id.delete()
                
            return JsonResponse({'status':'1','msg':'Data Added Successfully.'})
        else:
           return JsonResponse({'status':'0','msg':'Something went wrong.'}) 
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def Show_banner(request):
    if request.session.get('email'):
        obj_banner = BannerMaster.objects.all().order_by('-id')
        return render(request, 'admin_panel/banner.html', {'obj_banner': obj_banner})
    else:
        return redirect('/')
    
    
@csrf_exempt
def Add_banner(request):
    try:
        if request.method == "POST":
            banner_title = request.POST.get("banner_title")
            banner_image = request.FILES.get("banner_image")
            
            BannerMaster.objects.create(banner_title = banner_title,banner_image = banner_image)
            return JsonResponse({'status':'1','msg':'Banner Image Added Successfully.'})
        else:
            return JsonResponse({'status':'0','msg':'Something went wrong.'})
    except:
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
@csrf_exempt
def Delete_banner(request):
    try:
        if request.method == "POST":
            id = request.POST.get("id")
            obj_del= BannerMaster.objects.filter(id=id).delete()
            return JsonResponse({'status':'1','msg':'Banner Deleted Successfully.'})
        else:
            return JsonResponse({'status':'0','msg':'Something went wrong.'})
    except:
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
        
        
        
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def commision(request):
    if request.session.get('email'):
        country = CountryMaster.objects.all().order_by('country_name')
        category = CategoryMaster.objects.all().order_by('category_name')
        customer_commision = CommisionMaster.objects.filter(user_type = "Customer").order_by('-id')
        vendor_commision = CommisionMaster.objects.filter(user_type = "Vendor").order_by('-id')
        print(CommisionMaster.objects.filter(user_type = "Customer").count())
        print(CommisionMaster.objects.filter(user_type = "Vendor").count())
        context = { 
            'category':category,
            'country':country,
            'customer_commision':customer_commision,
            'vendor_commision':vendor_commision
        }
        return render(request,'admin_panel/commision.html',context)
    else:
        return redirect ('/')

@csrf_exempt
def Save_Customer_Commision(request):
    try:
        if request.session.get('email'):
            if request.method == "POST":
                country = request.POST.get('country')
                category = request.POST.get('category')
                commision = request.POST.get('commision')
                
                country_obj = CountryMaster.objects.get( id = country)
                category_obj = CategoryMaster.objects.get( id = category)
                
                if CommisionMaster.objects.filter(fk_country = country_obj , fk_category = category_obj , user_type = "Customer").exists():
                    return JsonResponse({'status':'0','msg':'Commission Already Added.'})
                else:
                    CommisionMaster.objects.create(fk_country = country_obj , fk_category = category_obj , commision = commision , user_type = "Customer")
                    return JsonResponse({'status':'1','msg':'Commission added successfully.'})
            else:
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
           return redirect ('/') 
    except:
        return JsonResponse({'status':'0','msg':'Something went wrong.'})


@csrf_exempt
def Edit_Commision(request):
    try:
        if request.session.get('email'):
            if request.method == "POST":
                commision_id = request.POST.get('commision_id')
                country = request.POST.get('country')
                category = request.POST.get('category')
                commision = request.POST.get('commision')
                
                country_obj = CountryMaster.objects.get( id = country)
                category_obj = CategoryMaster.objects.get( id = category)
                if CommisionMaster.objects.filter(id = commision_id).exclude(id=commision_id).exists():
                    return JsonResponse({"status":"0","msg":"Something Went Wrong."})
                else: 
                    CommisionMaster.objects.filter(id = commision_id).update(fk_country = country_obj , fk_category = category_obj ,  commision = commision)
                    return JsonResponse({'status':'1','msg':'Commission updated successfully.'})
            else:
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
           return redirect ('/') 
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})

@csrf_exempt
def Delete_Commision(request):
    try:
        if request.session.get('email'):
            if request.method == "POST":
                commision_id = request.POST.get('commision_id')
                
                CommisionMaster.objects.filter(id = commision_id).delete()
                
                return JsonResponse({'status':'1','msg':'Commission deleted successfully.'})
            else:
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
           return redirect ('/') 
    except:
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
        





@csrf_exempt
def Save_Vendor_Commision(request):
    try:
        if request.session.get('email'):
            if request.method == "POST":
                country = request.POST.get('country')
                category = request.POST.get('category')
                commision = request.POST.get('commision')
                
                country_obj = CountryMaster.objects.get( id = country)
                category_obj = CategoryMaster.objects.get( id = category)
                
                if CommisionMaster.objects.filter(fk_country = country_obj , fk_category = category_obj  , user_type = "Vendor").exists():
                    return JsonResponse({'status':'0','msg':'Commision Already Added.'})
                else:
                    print("-----------------------")
                    CommisionMaster.objects.create(fk_country = country_obj , fk_category = category_obj , commision = commision , user_type = "Vendor")
                    return JsonResponse({'status':'1','msg':'Commsion Added Successfully.'})
            else:
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
           return redirect ('/') 
    except:
        return JsonResponse({'status':'0','msg':'Something went wrong.'})


 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def offer(request):
    if request.session.get('email'):
        country = CountryMaster.objects.all().order_by('country_name')
        category = CategoryMaster.objects.all().order_by('category_name')
        offers = Offers.objects.all().order_by('-id')
        context = { 
            'category':category,
            'country':country,
            'offers':offers
        }
        return render(request,'admin_panel/offer.html',context)
    else:
        return redirect ('/')
        
        
@csrf_exempt
def Save_Offer(request):
    try:
        if request.session.get('email'):
           if request.method == "POST":
                country = request.POST.get('country')
                category = request.POST.get('category')
                offercode = request.POST.get('offercode')
                discount = request.POST.get('discount')
                expirydate = request.POST.get('expirydate')
                
                country_obj = CountryMaster.objects.get( id = country)
                category_obj = CategoryMaster.objects.get( id = category)
                if Offers.objects.filter(fk_country = country_obj , fk_category = category_obj , offer_code = offercode , offercode_status ="Active").exists():
                    return JsonResponse({'status':'0','msg':'OfferCode Already Exists.'})
                else:
                    Offers.objects.create(fk_country = country_obj , fk_category = category_obj , offer_code = offercode , discount = discount , expirydate = expirydate )
                    
                    return JsonResponse({'status':'1','msg':'Promocode Added Successfully.'})
           else:
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
           return redirect ('/') 
    except:
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
        

@csrf_exempt
def Edit_Offer(request):
    try:
        if request.session.get('email'):
           if request.method == "POST":
                offer_id = request.POST.get('offer_id')
                country = request.POST.get('country')
                category = request.POST.get('category')
                offercode = request.POST.get('offercode')
                discount = request.POST.get('discount')
                expirydate = request.POST.get('expirydate')
                
                country_obj = CountryMaster.objects.get( id = country)
                category_obj = CategoryMaster.objects.get( id = category)
                
                print(datetime.datetime.now().date())
                if Offers.objects.filter(id=offer_id).exclude(id=offer_id).exists():
                    return JsonResponse({"status":"0","msg":"Something Went Wrong."})
                else:
                    offer_obj = Offers.objects.get(id = offer_id)
                    if offer_obj.offercode_status == "Expired" and offer_obj.expirydate >= datetime.datetime.now().date():
                        Offers.objects.filter(id = offer_id).update(fk_country = country_obj , fk_category = category_obj , offer_code = offercode , discount = discount , expirydate = expirydate, offercode_status ="Active" )
                        
                    elif offer_obj.offercode_status == "Expired" and offer_obj.expirydate <= datetime.datetime.now().date():
                        Offers.objects.filter(id = offer_id).update(fk_country = country_obj , fk_category = category_obj , offer_code = offercode , discount = discount , expirydate = expirydate, offercode_status ="Active" )
                    elif offer_obj.offercode_status == "Active":
                        Offers.objects.filter(id = offer_id).update(fk_country = country_obj , fk_category = category_obj , offer_code = offercode , discount = discount , expirydate = expirydate )
                       
                    else:
                        pass
                    return JsonResponse({'status':'1','msg':'Promocode Updated Successfully.'})
           else:
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
           return redirect ('/') 
    except:
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
        

@csrf_exempt
def Delete_Offer(request):
    try:
        if request.session.get('email'):
            if request.method == "POST":
                offer_id = request.POST.get('offer_id')
                
                Offers.objects.filter(id = offer_id).delete()
                
                return JsonResponse({'status':'1','msg':'Promocode Deleted Successfully.'})
            else:
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
           return redirect ('/') 
    except:
        return JsonResponse({'status':'0','msg':'Something went wrong.'})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Orders(request):
    if request.session.get('email'):
        return render(request,'admin_panel/orders.html')
    else:
        return redirect('/')
        
@csrf_exempt
def Show_Orders(request):
    try:
        if request.session.get('email'):
            if request.method == "POST":
                status = request.POST.get('status')
                temp = ['Accepted','Started']
                    
                if status == "All":
                    orders = OrderDetails.objects.all().order_by('-id').exclude(order_status__in = temp)
                else:
                    orders = OrderDetails.objects.filter(order_status = status).order_by('-id')
                rendered = render_to_string("admin_panel/render_to_string/r_t_s_orders.html",{'orders':orders})
                
                return JsonResponse({'status':'1','msg':'Success','response':rendered})
            else:
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
            return redirect('/')
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})


@csrf_exempt
def Filter_Order(request):
    try:
        if request.session.get('email'):
            if request.method == 'POST':
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date')
                status = request.POST.get('status')
                if status == "All":
                    orders = OrderDetails.objects.filter(current_booking_date__gte = from_date , current_booking_date__lte = to_date).order_by('-id')
                else:
                    orders = OrderDetails.objects.filter(current_booking_date__gte = from_date , current_booking_date__lte = to_date, order_status = status).order_by('-id')
                rendered = render_to_string("admin_panel/render_to_string/r_t_s_orders.html",{'orders':orders})
                
                return JsonResponse({'status':'1','msg':'Success','response':rendered})
            else:
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
            return redirect('/')
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
        

@csrf_exempt
def Show_item_detail(request):
    try:
        if request.session.get('email'):
            if request.method == 'POST':
                sid = request.POST.get('id')
                services = OrderService.objects.filter(fk_order__id = sid)
                rendered = render_to_string("admin_panel/render_to_string/r_t_s_itemdetail.html",{'services':services})
                print(rendered)
                return JsonResponse({'status':'1','msg':'Success','response':rendered})
            else:
                print("hello")
                return JsonResponse({'status':'0','msg':'Something went wrong.'})
        else:
           return redirect('/') 
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
        
        
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)       
def Revenue_Income(request):
    try:
        if request.session.get('email'):
            today_date = datetime.datetime.today().replace(day=1)
            date = datetime.datetime.date(today_date)
            end_date = date.replace(day = calendar.monthrange(date.year, date.month)[1])
            
            
            orders = OrderDetails.objects.filter(current_booking_date__gte = today_date , current_booking_date__lte = end_date ,order_status = "Completed").order_by('-id')
            for i in orders:
                i.revenue =  i.convenience_fee + i.vendor_convenience_fee
                
            rendered = render_to_string("admin_panel/render_to_string/r_t_s_revenue_income.html",{'orders':orders})
            context = {
                'from_date':today_date,
                'to_date':end_date,
                'orders':rendered
            }
            return render(request,'admin_panel/revenue_income.html',context)
        else:
            print(request.session.get('email'))
            return redirect('/')
    except:
        traceback.print_exc()
        
        return redirect('/')

@csrf_exempt
def Filter_Revenue_Income(request):
    try:
        if request.session.get('email'):
            if request.method == 'POST':
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date')
                orders = OrderDetails.objects.filter(current_booking_date__gte = from_date , current_booking_date__lte = to_date ,order_status = "Completed").order_by('-id')
                for i in orders:
                    i.revenue =  i.convenience_fee + i.vendor_convenience_fee
                    
                rendered = render_to_string("admin_panel/render_to_string/r_t_s_revenue_income.html",{'orders':orders})
                return JsonResponse({'status':'1','response':rendered})
            else:
                return JsonResponse({'status':'0','msg':'Post method required'})
        else:
            return redirect('/')
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
        
        
        
        
def Withdraw(request):
    try:
        if request.session.get('email'):
            
            payment = Vendor_Withdraw_Payment.objects.all().order_by('-id')
            rendered = render_to_string("admin_panel/render_to_string/r_t_s_withdraw.html",{'payment':payment})
            
            return render(request,'admin_panel/withdraw.html',{'payment':rendered})
        else:
            return redirect('/')
    except:
        traceback.print_exc()
        return redirect('/')

@csrf_exempt
def Payment_Approve_Reject(request):
    try:
        if request.method == 'POST':
            payment_id = json.loads(request.POST.get('payment_id'))
            status = request.POST.get('status')
            msg = request.POST.get('msg')
            
            for i in payment_id:
                obj = Vendor_Withdraw_Payment.objects.get(id = i)
                if status =="Accepted":
                    
                    updated_earning = obj.fk_vendor.vendor_earning - obj.payment_amount                    
                    VendorDetails.objects.filter(id = obj.fk_vendor.id).update(vendor_earning = updated_earning,withdraw_request_status = False, withdraw_request = 0)
                    Vendor_Withdraw_Payment.objects.filter(id = i).update(payment_receive_date = datetime.datetime.now())
                else:
                    VendorDetails.objects.filter(id = obj.fk_vendor.id).update(withdraw_request_status = False,withdraw_request = 0)
                Vendor_Withdraw_Payment.objects.filter(id = i).update(withdraw_status = status)
            return JsonResponse({'status':'1','msg':'Payment '+ msg + ' Successfully.'})
        else:
            return JsonResponse({'status':'0','msg':'Post method required.'})
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
    

@csrf_exempt
def Filter_Withdraw_Request(request):
    try:
        if request.method == 'POST':
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            status = request.POST.get('status')
            rendered = None
            if status == "All":
                payment = Vendor_Withdraw_Payment.objects.filter(withdraw_request_date__gte = from_date , withdraw_request_date__lte = to_date).order_by('-id')
                rendered = render_to_string("admin_panel/render_to_string/r_t_s_withdraw.html",{'payment':payment})
            else:
                
                payment = Vendor_Withdraw_Payment.objects.filter(withdraw_request_date__gte = from_date , withdraw_request_date__lte = to_date,withdraw_status = status).order_by('-id')
                rendered = render_to_string("admin_panel/render_to_string/r_t_s_withdraw.html",{'payment':payment})
            return JsonResponse({'status':'1','response':rendered})
        else:
            return JsonResponse({'status':'0','msg':'Post method required.'})
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
        

@csrf_exempt
def Bank_Account_Details(request):
    try:
        if request.method == 'POST':
            vendor_id = request.POST.get('vendor_id')
            account_detail = Vender_AccountDetails.objects.filter(fk_vender__id = vendor_id)
            rendered = None
            if account_detail.exists():
                rendered = render_to_string("admin_panel/render_to_string/r_t_s_bank_account_details.html",{'account_detail':account_detail})
            else:
                temp_list=[]
                temp_dict = {}
                temp_dict['Bank_name'] = "---"
                temp_dict['fk_vender.full_name'] = "---"
                temp_dict['Account_no'] = "---"
                temp_dict['IBAN_no'] = "---"
                temp_dict['BIC_code'] = "---"
                temp_list.append(temp_dict)
                
                rendered = render_to_string("admin_panel/render_to_string/r_t_s_bank_account_details.html",{'account_detail':temp_list})
            return JsonResponse({'status':'1','response':rendered})
        else:
            return JsonResponse({'status':'0','msg':'Post method required.'})
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong'})
#********************** End Mobile App Send Nofification Function ********************************* 
 


def Privacy_Policy(request):
    return render(request,'admin_panel/privacy_policy.html')

def Terms_of_Service(request):
    return render(request,'admin_panel/terms_of_service.html')

def Refund_Policy(request):
    return render(request,'admin_panel/refund_policy.html')

def Contact_us(request):
    return render(request,'admin_panel/contact_us.html')


@csrf_exempt
def Ajax_Contact_us(request):
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('contact_msg')
        
        send_mail(f'{name} wants to contact us', f'Dear Admin,\nPlease find new contact info received from website.\nName: {name}.\nEmail: {email}, \nMessage: {message},', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
        # temp_dict['otp'] = otp
        # temp_dict["signup_msg"] = ""
        return JsonResponse({'status':'1','msg':'Thanks for contacting us, we will reach to you shortly.'})
    except:
        traceback.print_exc()
        return JsonResponse({'status':'0','msg':'Something went wrong.'})
        



# def test(request):
    # if request.session.get('email'):
        # country = CountryMaster.objects.all()
        # category = CategoryMaster.objects.all()
        # offers = Offers.objects.all()
        # context = { 
            # 'category':category,
            # 'country':country,
            # 'offers':offers
        # }
        # return render(request,'admin_panel/test.html',context)
    # else:
        # return redirect ('/login_page/')


