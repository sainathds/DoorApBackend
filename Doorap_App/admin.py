from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.
class MyUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('id', 'name', 'email', 'is_vendor', 'is_customer', 'firebase_token','is_staff', 'login_type','last_login')}),
        ('Permissions', {'fields': (
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('name','email', 'password1', 'password2', 'is_vendor', 'is_customer', 'is_staff', 'firebase_token')
            }
        ),
    )

    list_display = ('id','name','email','password',  'is_vendor', 'is_customer', 'firebase_token','is_staff', 'login_type','last_login')
    readonly_fields = ('id',)
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(MyUser, MyUserAdmin)

class AdminDetails_class(admin.ModelAdmin):
    list_display = ('id','name','email', 'admin_status')
admin.site.register(AdminDetails ,AdminDetails_class)


@admin.register(CountryMaster)
class CountryMasterAdmin(admin.ModelAdmin):
    list_display = ['id','country_name','status']
    
    
@admin.register(CityMaster)
class CityMasterAdmin(admin.ModelAdmin):
    list_display = ['id','fk_country','city_name', 'status']
        
        
@admin.register(VendorDetails)
class VendorDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','fk_user','full_name','profile_image','abount_me','business_name','mobile_no','google_address','google_address_lat','google_address_lng','address_line_one','address_line_two','fk_country','fk_city','zip_code','user_status','is_available','from_time','to_time']
    
    
@admin.register(Vender_AccountDetails)
class VenderAccountDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','fk_vender','Account_no','IBAN_no','BIC_code','Bank_name','account_status']
    
    

@admin.register(CategoryMaster)   #******* Category Master
class CategoryMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'category_image' , 'category_status']
    


@admin.register(ServiceMaster)  #******* Service Master
class ServiceMasterAdmin(admin.ModelAdmin):
    list_display = ['id' ,'fk_category','service_image','service_name','service_price','service_time','service_status']
    



@admin.register(ServiceFacility)   #********* ServiceFaciltiy
class ServiceFaciltiyAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_service' ,'facility_name','facility_status']
    
    
@admin.register(VenderCustomService)    #*********  Vendor Custom Service
class VenderCustomServiceAdmin(admin.ModelAdmin):
    list_display = ['id' ,'fk_vendor','fk_category','custom_service_image','custom_service_name','custom_service_price','custom_service_time','custom_service_status']
    

@admin.register(VenderCustomFacility)   #********* Vendor Custom Service Faciltiy
class ServiceFaciltiyAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_custom_service' ,'custom_facility_name','custom_facility_status']
    

@admin.register(VenderServices)   
class VenderServicesAdmin(admin.ModelAdmin):    #************* Vender Services
    list_display = ['id','fk_vendor' ,'fk_category','fk_service','price','hour','status','rating']
    

@admin.register(VenderFacility)
class VenderFacilityAdmin(admin.ModelAdmin):
    list_display = ['id','fk_vender_service','fk_vender_facility','vender_facility_status']
    

# @admin.register(VendorSetSchedule)   
# class VendorSetScheduleAdmin(admin.ModelAdmin):
    # list_display = ['id', 'fk_vendor','is_monday','is_tuesday','is_wednesday','is_thursday','is_friday','is_saturday','is_sunday','from_date','to_date']
    
@admin.register(BannerMaster)    
class BannerMasterAdmin(admin.ModelAdmin):
    list_display = ['id','banner_title','banner_image','banner_status']
    
    
@admin.register(AddtoCart)
class AddtoCartAdmin(admin.ModelAdmin):
    list_display = ['id','fk_vendor','fk_customer','fk_category','fk_vender_service','quantity','price','hour','sub_total','cart_status']
    
    

@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = ['id' , 'fk_country' , 'fk_category' , 'offer_code' , 'discount' ,'expirydate','used_offercode','offercode_status' ] 
    
    

@admin.register(CommisionMaster) 
class CommisionMasterAdmin(admin.ModelAdmin):
    list_display = ['id','fk_country','fk_category','commision','user_type']

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','order_id','fk_vendor','fk_customer','quantity','fk_city','address','city','zip_code','lat','lng','sub_total','discount','convenience_fee','total_amount','duration','booking_date','booking_start_time','booking_end_time','user_promocode','vendor_pay_amount','order_status','status','booking_time']
    
    
@admin.register(OrderService)
class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_order','fk_vendor' ,'fk_service','service_quantity','status']
    

@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ['id','fk_vendor','fk_customer','like_dislike']
    
    
@admin.register(AppliedOfferCode)
class AppliedOfferCodeAdmin(admin.ModelAdmin):
    list_display = ['id','fk_customer','fk_offer','is_applied']