from Doorap_App import views_customer
from django.urls import path

urlpatterns = [
    path('banner_show/',views_customer.Show_Banner,name ='show_banner'),
    path('show_location_wise_vendor/',views_customer.Show_location_wise_vendor , name = 'near_by_store'),
    path('show_category_by_vendor/',views_customer.show_vendor_by_category, name='show_category_by_vendor'),
    
    path('show_all_services/',views_customer.Show_All_Services , name='show_all_services'),
    path('show_vendor_by_services/',views_customer.Show_Vendor_by_Services , name='Show_Vendor_by_Services'),
    
    path('show_vendor_profile/',views_customer.Show_Vendor_profile , name='show_vendor_profile'),
    
    
    
    
    path('show_services_list_by_vendor/',views_customer.Show_Services_list_by_vendor, name='show_services_list_by_vendor'),
    path('show_vendor_facility/',views_customer.Show_Vendor_Facility , name='show_vendor_facility'),
    
    
    
    path('item_add_to_cart/',views_customer.Item_Add_to_Cart, name='item_add_to_cart'),
    path('update_item_quantity/',views_customer.Update_Item_Quantity , name='update_item_quantity'),
    path('item_minus/',views_customer.Item_Minus , name ='item_minus'),
    path('delete_item_to_cart/',views_customer.Delete_Item_to_Cart , name = 'delete_item_to_cart'),
    path('get_cart_data/',views_customer.Get_Cart_data , name = 'get_cart_data'),
    path('apply_promocode/',views_customer.Promocode_check , name='apply_promocode'),
    path('cart_quantity/',views_customer.Cart_Quantity , name='cart_quantity'),
    # path('slot_details/',views_customer.Slot_available_Notavailable , name='slot_details'),
    path('save_order_details/',views_customer.Save_Order_Details , name='save_order_details'),
    path('slot_availability/',views_customer.Next_Six_Date , name='next_six_days'),
    
    path('like_dislike/',views_customer.Like_Dislike , name='like_dislike'),
    path('show_like_vendor/',views_customer.Show_Like_Dislike_vendor , name='show_like_vendor'),
    path('show_current_order/',views_customer.Show_Current_Order , name='show_current_order'),
    path('show_all_order/',views_customer.Show_Customer_All_Order , name='show_all_order'),
    path('show_customer_order_detail/',views_customer.Show_Customer_Detail_Order , name='show_order_detail'),
    path('customer_cancel_order/',views_customer.Customer_Cancel_Order  , name='customer_cancel_order'),
    path('order_completed/',views_customer.Order_Completed , name='order_completed'),
    path('customer_reorder/',views_customer.Customer_Reorder , name='customer_reorder'),
    
    path('logout_api/',views_customer.Logout_api , name='logout_api'),
    path('show_notification/',views_customer.Show_Nofification_Api , name='show_notification'),
    path('delete_notification/',views_customer.Delete_Notification_Api , name='delete_notification'),
    path('notification_seen/',views_customer.Nofication_Seen_Api , name='notification_seen'),
    path('rating_feedback/',views_customer.Reviews_Rating_Feedback , name='rating_feedback'),
    path('show_review_feedback/',views_customer.Show_Review_Feedback, name='show_review_feedback'),
    path('stripe_payment/',views_customer.Stripe_payment , name='stripe_payment'),
    path('card/',views_customer.card , name='card'),
    path('test/',views_customer.test,name='test'),
    

]