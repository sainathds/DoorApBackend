from Doorap_App import views
from django.urls import path, re_path
from Doorap_App import cron
urlpatterns = [
    path('',views.Login_page,name='login_page'),
    path('login/',views.Login,name='login'),
    path('logout/',views.logout , name='logout'),
    path('dashboard/',views.Dashboard,name='dashboard'),
    path('vender_list/',views.VenderListPage , name='vender_list'),
    path('delete_vendor/',views.Delete_Vendor,name='delete_vendor'),
    path('approvereject/',views.ApproveReject,name='approvereject'),
    path('customerpage/',views.CustomerListPage , name='customerpage'),
    path('customerdelete/',views.DeleteCustomer,name = 'customerdelete'),
    re_path('view_vendor/(?P<id>[0-9]+)/$', views.view_vendor, name='view_vendor'),
    # re_path('view_vendor/<int:sid>/',views.view_vendor, name='view_vendor'),
    path('customservice/',views.Customservice , name='customservice'),
    re_path('custom_services_form/(?P<id>[0-9]+)/$',views.custom_services_form , name='custom_services_form'),
    re_path('vendorCategories/(?P<id>[0-9]+)/$',views.vendorCategories , name='vendorCategories'),
    path('add_facility/',views.add_facility , name='add_facility'),
    path('add_to_master_data/',views.add_to_master_data , name='add_to_master_data'),
    path('show_vendor_facility/',views.show_vendor_facility , name='show_vendor_facility'),
    path('Show_banner/',views.Show_banner , name='Show_banner'),
    path('add_banner/',views.Add_banner , name='add_banner'),
    
    path('Delete_banner/',views.Delete_banner , name='Delete_banner'),
    
    
    path('offer/',views.offer , name='offer'),
    path('save_offer/', views.Save_Offer , name='save_offer'),
    path('edit_offer/', views.Edit_Offer , name='edit_offer'),
    path('delete_offer/',views.Delete_Offer , name='Delete_Offer'),
    
    # path('check_cron/',cron.Update_Status , name='check_cron'),
    path('commision/',views.commision , name='commision'),
    path('save_customer_commision/',views.Save_Customer_Commision , name='save_customer_commision'),
    path('edit_commision/',views.Edit_Commision , name='edit_customer_commision'),
    path('delete_commision/',views.Delete_Commision , name='delete_customer_commision'),
    path('save_vendor_commision/',views.Save_Vendor_Commision , name='save_vendor_commision'),
    path('orders/',views.Orders , name='orders'),
    path('show_orders/',views.Show_Orders , name = 'Show_Orders'),
    path('filter_order/',views.Filter_Order , name = 'filter_order'),
    path('show_item_detail/',views.Show_item_detail , name='show_item_detail'),
    path('revenue_income/',views.Revenue_Income , name='revenue_income'),
    path('filter_revenue_income/',views.Filter_Revenue_Income , name='filter_revenue_income'),
    
    
    path('withdraw/',views.Withdraw,name ='withdraw'),
    path('payment_approve_reject/',views.Payment_Approve_Reject,name='payment_approve_reject'),
    path('filter_withdraw_request/',views.Filter_Withdraw_Request, name='filter_withdraw_request'),
    path('bank_account_details/',views.Bank_Account_Details , name='bank_account_details'),
    
    path('test/',views.test , name='test'),
   
    path('privacy_policy/',views.Privacy_Policy ,name='privacy_policy'),
    path('terms_of_service/',views.Terms_of_Service , name='terms_of_service'),
    path('refund_policy/',views.Refund_Policy , name = 'refund_policy'),
    path('Contact_us/',views.Contact_us , name = 'Contact_us'),
    path('Ajax_Contact_us/',views.Ajax_Contact_us , name = 'Ajax_Contact_us')
    # path('test/',views.test , name='test')
    
    
]
