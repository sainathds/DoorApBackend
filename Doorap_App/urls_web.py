from Doorap_App import views_web
from django.urls import path

urlpatterns = [
    
    #vender signup and login api url
    path('get_otp/',views_web.get_otp, name='get_otp'),
    path('sign_up/', views_web.sign_up , name = 'sign_up'),
    path('login/',views_web.Vender_login,name='login'),
    #end vender signup api
    
    #save profile api url 
    path('save_profile/',views_web.save_profile ,name='save_profile'),
    # end save profile api url
    
    # State and City api url
    path('get_country/', views_web.get_states , name='get_state'),
    path('get_city/', views_web.get_cities , name = 'get_cities'),  
    # End State and City api url 
    
    # Forgot password api 
    path('forgor_password_otp/', views_web.forgotPassword_get_otp, name='forgor_password_otp'),
    path('forgot_password/', views_web.forgot_password , name ='forgot_password'),
    path('change_password/', views_web.change_password , name='change_password'),
    # End Forgotpassword api
    
    # User Profile Api url
    path('view_profile/', views_web.view_profile , name = 'view_profile'),
    path('edit_profile/',views_web.Edit_profile , name='edit_profile'),
    path('user_available/',views_web.user_available, name ='user_available'),
    path('add_bank_account/',views_web.Add_Bank_Account,name='add_bank_account'),
    # end User Profile api url
    
   # show services api url 
    path('view_category/',views_web.All_Category , name='view_category'),
    path('show_services/',views_web.Show_Services , name='show_services'),
    path('facility_list/',views_web.Show_Facilities , name='facility_list'),
   # end show services api url
   
   # vender Add ,edit ,delete,show services api url
    path('vender_show_services/',views_web.Show_Vender_SetServices, name ='vender_show_services'),
    path('vender_add_services/',views_web.Vender_Add_Services, name='vender_add_services'),
    path('add_custom_service/',views_web.Add_Vendor_Custom_ServicesandFacility , name='add_custom_service'),
    path('vender_edit_services/',views_web.Edit_Vendor_Services , name='vender_edit_services'),
    path('delete_services/',views_web.Delete_Vendor_Services,name='delete_services'),    
   # end vender add ,edit , delete services api url 
    
    # vendor set schedule api url    
    path('set_schedule/', views_web.UserDetailInfo.as_view(), name='UserDetailInfo'),
    path('show_set_schedule/',views_web.show_set_schedule , name='show_set_schedule'),   
    # end vendor set schedule api url
    
    path('vendor_facility_list/',views_web.vendor_facility , name='vendor_facility_list'),
    
    
   # end user set services api
   
   path('show_order_to_vendor/',views_web.Show_Order_to_Vendor , name='show_order_to_vendor'),
   path('order_accept_decline/',views_web.Order_Accept_Decline , name ='order_accept_decline'),
   path('order_start_job/',views_web.Order_Start_Job , name = 'order_start_job'),
   path('show_running_job/',views_web.Show_Running_Job , name='show_running_job'),
   path('show_vendor_order_detail/',views_web.Show_Vendor_Detail_Order , name='show_vendor_order_detail'),
   path('show_account_detail/',views_web.Show_Bank_Account , name='show_account_detail'),
   
   
   path('social_signup/',views_web.social_sign_up , name='social_signup'),
   path('social_otp/',views_web.get_otp_Social , name='social_otp'),
]