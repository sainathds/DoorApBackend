from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import MyCustomManager
from ckeditor.fields import RichTextField

class AdminDetails(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    admin_status = models.BooleanField(default=False)
    
    
class CountryMaster(models.Model):
    country_name = models.CharField(max_length=100, null=True, blank=True)
    country_code = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.country_name
    
    
class CityMaster(models.Model):
    fk_country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE, null=True, blank=True)
    city_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=False)
    
    
class MyUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    
    firebase_token = models.CharField(max_length=300, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    created_datime = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    login_type = models.CharField(max_length=50, blank=True, null=True)
    login_id = models.CharField(max_length=50, blank=True, null=True)
    is_profile_create = models.BooleanField(default = False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyCustomManager()

    def __str__(self):
        return self.email
        
        
class VendorDetails(models.Model):
    fk_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length = 100, null = True, blank=True)
    profile_image = models.FileField(upload_to='VendorProfile/', blank=True, null=True)
    abount_me = models.TextField(null=True, blank=True)
    business_name = models.CharField(max_length=200, blank=True, null=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)
    google_address = models.TextField(null=True, blank=True)
    google_address_lat = models.FloatField(blank=True, null=True)
    google_address_lng = models.FloatField(blank=True, null=True)
    address_line_one = models.TextField(null=True, blank=True)
    address_line_two = models.TextField(null=True, blank=True)
    fk_country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE, null=True, blank=True)
    fk_city = models.ForeignKey(CityMaster, on_delete=models.CASCADE, null=True, blank=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    user_status = models.CharField(max_length=20, blank=True, null=True, default="Pending")
    is_available = models.BooleanField(default=False)
    is_service_created = models.BooleanField(default = False)
    #set schedule
    is_monday = models.BooleanField(default = False)
    is_tuesday = models.BooleanField(default = False)
    is_wednesday = models.BooleanField(default = False)
    is_thursday = models.BooleanField(default = False)
    is_friday = models.BooleanField(default = False)
    is_saturday = models.BooleanField(default = False)
    is_sunday = models.BooleanField(default = False)
    from_time = models.TimeField(blank = True,null = True)
    to_time = models.TimeField(blank = True , null = True)
    is_set_status = models.BooleanField(default = False)
    # is_profile_create = models.BooleanField(default = False)



class Vender_AccountDetails(models.Model):
    fk_vender = models.ForeignKey(VendorDetails , on_delete=models.CASCADE , null = True , blank = True)
    Account_no = models.CharField(max_length = 200 , null = True ,blank = True)
    IBAN_no = models.CharField(max_length = 200 , blank=True, null = True)
    BIC_code = models.CharField(max_length = 100 , blank = True, null = True)
    Bank_name = models.CharField(max_length = 100 , blank = True, null = True)
    account_status = models.BooleanField(default = False)
    
    

class CategoryMaster(models.Model):
    category_name = models.CharField(max_length = 200, blank = True, null = True)
    category_image = models.FileField(upload_to='VendorProfile/', blank=True, null=True)
    category_status = models.BooleanField(default = False)
    
    

class ServiceMaster(models.Model):
    fk_category = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE, null=True, blank=True)
    service_image = models.FileField(upload_to='VendorProfile/', blank=True, null=True)
    service_name = models.TextField(null=True, blank=True)
    service_price = models.FloatField(blank = True , null = True)
    service_time = models.CharField(max_length =200,blank = True , null = True)
    service_status = models.BooleanField(default = False)



class ServiceFacility(models.Model):
    fk_service = models.ForeignKey(ServiceMaster, on_delete=models.CASCADE, null=True, blank=True)
    facility_name = models.TextField(null=True, blank=True)
    facility_status = models.BooleanField(default = False)
    
    

class VenderCustomService(models.Model):
    fk_vendor = models.ForeignKey(VendorDetails, on_delete=models.CASCADE, null=True, blank=True)
    fk_category = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE, null=True, blank=True)
    custom_service_image = models.FileField(upload_to='VendorProfile/', blank=True, null=True)
    custom_service_name = models.TextField(null=True, blank=True)
    custom_service_price = models.FloatField(blank = True , null = True)
    custom_service_time = models.CharField(max_length = 200, blank = True , null = True)
    custom_service_status = models.BooleanField(default = False)



class VenderCustomFacility(models.Model):
    fk_custom_service = models.ForeignKey(VenderCustomService, on_delete=models.CASCADE, null=True, blank=True)
    custom_facility_name = models.TextField(null=True, blank=True)
    custom_facility_status = models.BooleanField(default = False)
    
    


class VenderServices(models.Model):
    fk_vendor = models.ForeignKey(VendorDetails, on_delete=models.CASCADE, null=True, blank=True)
    fk_category = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE, null=True, blank=True)
    fk_service = models.ForeignKey(ServiceMaster, on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField(blank = True , null = True)
    hour = models.CharField(max_length = 200 ,blank = True , null = True)
    rating = models.CharField( max_length =20 , default="4")
    status = models.BooleanField(default = False)
    
    

class VenderFacility(models.Model):
    fk_vender_service = models.ForeignKey(VenderServices, on_delete=models.CASCADE, null=True, blank=True)
    fk_vender_facility  = models.ForeignKey(ServiceFacility, on_delete=models.CASCADE, null=True, blank=True)
    vender_facility_status = models.BooleanField(default = False)
    
    

class BannerMaster(models.Model):
    banner_title = models.CharField(max_length = 200, blank = True , null = True)
    banner_image = models.FileField(upload_to='BannerImage/', blank=True, null=True)
    banner_status = models.BooleanField(default = False)



class AddtoCart(models.Model):
    fk_vendor = models.ForeignKey(VendorDetails, on_delete=models.CASCADE, null=True, blank=True)
    fk_customer = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    fk_category = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE, null=True, blank=True)
    fk_vender_service = models.ForeignKey(VenderServices, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(blank = True , null = True)
    price = models.FloatField( blank = True , null = True)
    hour = models.CharField(max_length = 10 , blank = True , null = True) 
    # convenience_fee = models.FloatField(blank = True , null = True)
    sub_total = models.FloatField(blank = True ,null = True)
    cart_status = models.BooleanField(default = False) 


    
    
    
class Offers(models.Model):
    fk_country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE, null=True, blank=True)
    fk_category  = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE, null=True, blank=True)
    offer_code = models.CharField(max_length = 200 , blank = True , null = True)
    discount = models.FloatField(blank = True , null = True)
    expirydate = models.DateField(blank = True , null = True)
    offercode_status = models.CharField(max_length = 50 , default = "Active")
    used_offercode = models.IntegerField(default = 0)
    status = models.BooleanField(default = False)

class AppliedOfferCode(models.Model):
    fk_customer = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    fk_offer = models.ForeignKey(Offers, on_delete=models.CASCADE, null=True, blank=True)
    is_applied = models.BooleanField(default = False)



class CommisionMaster(models.Model):
    fk_country = models.ForeignKey(CountryMaster , on_delete = models.CASCADE , null = True , blank = True)
    fk_category = models.ForeignKey(CategoryMaster , on_delete = models.CASCADE , null = True , blank = True)
    commision = models.FloatField(blank = True , null = True)
    user_type = models.CharField(max_length = 200 , blank = True, null = True)
    
    

class OrderDetails(models.Model):
    order_id = models.CharField(max_length = 200 , blank = True , null = True)
    fk_vendor = models.ForeignKey(VendorDetails, on_delete=models.CASCADE, null=True, blank=True)
    fk_customer = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField( blank = True , null = True)
    address = models.CharField(max_length = 400 , blank = True ,null = True)
    fk_city = models.ForeignKey(CityMaster , on_delete = models.CASCADE , null = True , blank = True)
    city = models.CharField(max_length =200 , blank = True , null = True)
    zip_code = models.CharField( max_length = 200 , blank = True , null = True)
    lat = models.FloatField(blank = True , null = True)
    lng = models.FloatField( blank = True , null = True)
    sub_total = models.FloatField(blank = True , null = True)
    discount = models.FloatField(blank = True , null = True)
    convenience_fee = models.FloatField( blank = True , null = True)
    total_amount = models.FloatField( blank = True , null = True)
    duration = models.IntegerField( blank = True , null = True)
    booking_date = models.DateField(blank = True , null = True)
    booking_start_time = models.TimeField( blank = True , null = True)
    booking_end_time = models.TimeField( blank = True , null = True)
    user_promocode = models.CharField(max_length = 50 , blank = True , null = True)
    vendor_pay_amount = models.FloatField( blank = True , null = True)
    booking_time = models.TimeField(blank = True , null = True)
    
    order_status = models.CharField(max_length = 200 , default = "Pending")
    status = models.BooleanField(default = False)
    

class OrderService(models.Model):
    fk_order = models.ForeignKey( OrderDetails , on_delete = models.CASCADE ,blank = True , null = True)
    fk_vendor = models.ForeignKey(VendorDetails , on_delete = models.CASCADE , blank = True , null = True)
    fk_service = models.ForeignKey(VenderServices , blank = True , null = True , on_delete = models.CASCADE)
    service_quantity = models.CharField(max_length = 10 , blank = True , null = True)
    hour = models.CharField(max_length = 10 , blank = True , null = True)
    # order_status = models.CharField(max_length = 200 , default = "Pending")
    status = models.BooleanField(default = False)



class LikeDislike(models.Model):
    fk_vendor = models.ForeignKey(VendorDetails , on_delete = models.CASCADE , blank = True , null = True)
    fk_customer = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    like_dislike = models.BooleanField(default = False)