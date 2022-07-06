from Doorap_App import views
from django.urls import path, re_path
from Doorap_App import cron
urlpatterns = [
    path('login_page/',views.Login_page,name='login_page'),
    path('login/',views.Login,name='login'),
    path('logout/',views.logout , name='logout'),
    path('dashboard/',views.Dashboard,name='dashboard'),
    path('vender_list/',views.VenderListPage , name='vender_list'),
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
   
    # path('test/',views.test , name='test')
    
]