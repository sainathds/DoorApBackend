from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _


# ******************* Signup Serializer ***************************
class MyUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = "__all__"
        
    def create(self, validated_data):
        """ Creates and returns a new user """

        # Validating Data
        
        user = MyUser(
        name = validated_data['name'],
        email=validated_data['email'],
        firebase_token=validated_data['firebase_token'],
        is_vendor =validated_data['is_vendor'],
        is_customer = validated_data['is_customer']
        
        )
        user.set_password(validated_data['password'])
        
        user.save()
        return user
  


class CustomerSignUp(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = "__all__"
        
    def update(self,instance, validated_data):
        print(instance)
        instance.firebase_token=validated_data['firebase_token'],
        instance.is_customer = validated_data['is_customer']   
        instance.save()
        return instance
        
        
class VenderSignUp(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = "__all__"
        
    def update(self,instance, validated_data):
        instance.firebase_token=validated_data['firebase_token'],
        instance.is_vendor = validated_data['is_vendor']   
        instance.save()
        return instance 

#************************** End Signup Serializer ******************************8
 
        
#Save Profle Serializer
class VenderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetails
        fields = '__all__'
    
    def create(self , validated_data):
        if self.context['country_obj'] and self.context['city_obj'] :
            validated_data['fk_user'] = self.context['user_obj']
            validated_data['fk_country'] = self.context['country_obj']
            validated_data['fk_city'] = self.context['city_obj']
          
        user_info = VendorDetails.objects.create(**validated_data)  # saving post object
        
        return user_info
        
#******************* Login Serializer ****************************

class MyUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})
    
    class Meta:
        model = MyUser
        fields = '__all__'
    
    def validate(self, data):
        username = data.get('email',None)
        password = data.get('password',None)
        
        if username and password:
            user = authenticate(username = username , password = password)
            user.firebase_token = data.get('firebase_token')
            user.save()
            
            if not user:
                msg = _('Invalid Credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='blank')
        
        return user
        
# *********** End Login Serializer ************    

    
#Forgot Password Serializer
class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','email','firebase_token']
     
    def update(self, instance, validated_data):
        instance.set_password(self.context['password'])
        instance.save()
        return instance


#Change Password Serializer
class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','email','firebase_token']
        
    def update(self, instance, validated_data):
        old_password = self.context['old_password']
        if not instance.check_password(old_password):
            raise serializers.ValidationError({"authorize": "Old password doesn't matched."})
        else:
            instance.set_password(self.context['new_password'])
            instance.save()
            return instance
            
            
#Edit Profile Serializer           
class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetails
        fields = "__all__"
     
    def update(self, instance, validated_data):
        if validated_data['profile_image'] == None:
            instance.full_name = validated_data['full_name']
            instance.abount_me = validated_data['abount_me']
            instance.business_name = validated_data['business_name']
            instance.mobile_no = validated_data['mobile_no']
            instance.google_address = validated_data['google_address']
            instance.google_address_lat = validated_data['google_address_lat']
            instance.google_address_lng = validated_data['google_address_lng']
            instance.address_line_one = validated_data['address_line_one']
            instance.address_line_two = validated_data['address_line_two']
            instance.fk_country = self.context['country_obj']
            instance.fk_city = self.context['city_obj']        
            instance.zip_code = validated_data['zip_code']
            instance.save()
            return instance
        else:
            instance.full_name = validated_data['full_name']
            instance.profile_image = validated_data['profile_image']
            instance.abount_me = validated_data['abount_me']
            instance.business_name = validated_data['business_name']
            instance.mobile_no = validated_data['mobile_no']
            instance.google_address = validated_data['google_address']
            instance.google_address_lat = validated_data['google_address_lat']
            instance.google_address_lng = validated_data['google_address_lng']
            instance.address_line_one = validated_data['address_line_one']
            instance.address_line_two = validated_data['address_line_two']
            instance.fk_country = self.context['country_obj']
            instance.fk_city = self.context['city_obj']        
            instance.zip_code = validated_data['zip_code']
            instance.save()
            return instance

#Add Bank Account Serializer
class AddBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vender_AccountDetails
        fields = "__all__"
    
    def create(self,validated_data):
        save_details = Vender_AccountDetails(
        fk_vender = self.context['user_obj'],
        Account_no = validated_data['Account_no'],
        IBAN_no = validated_data['IBAN_no'],
        BIC_code = validated_data['BIC_code'],
        Bank_name = validated_data['Bank_name']
        )
        save_details.save()
        return save_details
        
        
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMaster
        fields = "__all__"
        


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceMaster
        fields = "__all__"
        
        

class VenderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenderServices
        fields = "__all__"
        
    def create(self , validated_data):
        if self.context['vendor_obj'] and self.context['category_obj'] and self.context['service_obj'] :
            validated_data['fk_vendor'] = self.context['vendor_obj']
            validated_data['fk_category'] = self.context['category_obj']
            validated_data['fk_service'] = self.context['service_obj']
          
        user_info = VenderServices.objects.create(**validated_data)  # saving post object
        
        return user_info
        

class VenderFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VenderFacility
        fields = "__all__"
        
   
    def create(self , validated_data):
        if self.context['facility_obj']:
            validated_data['fk_vender_facility'] = self.context['facility_obj']
        
        user_info = VenderFacility.objects.create(**validated_data)  # saving post object
        
        return user_info
   
   








class CustomerSignUpSocial(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = "__all__"
        
    def update(self,instance, validated_data):
        print(instance)
        instance.firebase_token=validated_data['firebase_token'],
        instance.is_customer = validated_data['is_customer']
        instance.save()
        return instance
        
        
class VenderSignUpSocial(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = "__all__"
        
    def update(self,instance, validated_data):
        instance.firebase_token=validated_data['firebase_token'],
        instance.is_vendor = validated_data['is_vendor']
        instance.save()
        return instance 

        
class MyUserSerializerTest(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = "__all__"
        
    def create(self, validated_data ):
        """ Creates and returns a new user """

        # Validating Data
        print(validated_data)
        user = MyUser(
        name = validated_data['name'],
        email=validated_data['email'],
        firebase_token=validated_data['firebase_token'],
        is_vendor =validated_data['is_vendor'],
        is_customer = validated_data['is_customer'],
        )
        user.set_password(validated_data['password'])
        
        user.save()
        return user
    
        
        
