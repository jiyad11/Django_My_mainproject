from django.urls import path

from myapp import views

urlpatterns = [
    ## Home ####
    path('',views.index,name='index'),
    path('index',views.index,name='index'),

    ############### Admin #####################
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('add_works', views.add_works, name='add_works'),
    path('view_works', views.view_works, name='view_works'),
    path('update_works/<int:id>/', views.update_works, name='update_works'),
    path('delete_works/<int:id>/', views.delete_works, name='delete_works'),
    path('waiting_for_approval',views.waiting_for_approval,name='waiting_for_approval'),

    ################ Worker ###################
    path('worker_dashboard', views.worker_dashboard, name='worker_dashboard'),

    ################ Customer ####################//
    path('customer_dashboard', views.customer_dashboard, name='customer_dashboard'),
    path('view_loggedIn_customer_only', views.view_loggedIn_customer_only, name='view_loggedIn_customer_only'),




    path('add_worker', views.add_worker, name='add_worker'),
    path('view_worker', views.view_worker, name='view_worker'),
    path('update_worker/<int:id>/', views.update_worker, name='update_worker'),
    path('delete_worker/<int:id>/', views.delete_worker, name='delete_worker'),
    path('add_customer', views.add_customer, name='add_customer'),
    path('view_customer', views.view_customer, name='view_customer'),
    path('update_customer/<int:id>/', views.update_customer, name='update_customer'),
    path('delete_customer/<int:id>/', views.delete_customer, name='delete_customer'),
    path('customer_profilecard',views.customer_profilecard,name='customer_profilecard'),
    path('schedule_work',views.schedule_work,name='schedule_work'),
    path('view_schedulework',views.view_schedulework,name='view_schedulework'),
    path('view_customerschedule', views.view_customerschedule, name='view_customerschedule'),
    path('update_schedulework/<int:id>/',views.update_schedulework,name='update_schedulework'),
    path('delete_schedulework/<int:id>/',views.delete_schedulework,name='delete_schedulework'),
    path('login_user',views.login_user,name='login_user'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('payment',views.payment,name='payment'),
    path('view_payment',views.view_payment,name='view_payment'),
    path('view_userpayment',views.view_userpayment,name='view_userpayment'),
    path('bill_payment/<int:id>/',views.bill_payment,name='bill_payment'),
    path('bill_directpayment/<int:id>/',views.bill_directpayment,name='bill_directpayment'),
    path('bill_history/',views.bill_history,name='bill_history'),
    path('take_appointment/<int:id>/',views.take_appointment,name='take_appointment'),
    path('view_appointment',views.view_appointment,name='view_appointment'),
    path('view_worker_appointment',views.view_worker_appointment,name='view_worker_appointment'),
    path('approve_appointment/<int:id>/',views.approve_appointment,name='approve_appointment'),
    path('reject_appointment/<int:id>/',views.reject_appointment,name='reject_appointment'),
    path('complaint',views.complaint,name='complaint'),
    path('view_complaint',views.view_complaint,name='view_complaint'),
    path('view_complaint_admin',views.view_complaint_admin,name='view_complaint_admin'),
    path('reply_complaint/<int:id>/',views.reply_complaint,name='reply_complaint'),
    path('view_painter',views.view_painter,name='view_painter'),
    path('view_carpenter',views.view_carpenter,name='view_carpenter'),
    path('painter_schedule',views.painter_schedule,name='painter_schedule'),
    path('carpenter_schedule',views.carpenter_schedule,name='carpenter_schedule'),
    path('about_us',views.about_us,name='about_us'),
    path('approve_customer/<int:customer_id>/',views.approve_customer,name='approve_customer'),
    path('reject_customer/<int:customer_id>/',views.reject_customer,name='reject_customer'),
    path('view_customer_needsApproval',views.view_customer_needsApproval,name='view_customer_needsApproval'),
    path('view_admin_appointment',views.view_admin_appointment,name='view_admin_appointment'),
    path('view_admin_workerAppointment',views.view_admin_workerAppointment,name='view_admin_workerAppointment'),

    path('view_available_schedulePage',views.view_available_schedulePage,name='view_available_schedulePage'),

    path('get_invoice/<int:id>/',views.get_invoice,name='get_invoice'),
    path('view_invoice/<int:id>/',views.view_invoice,name='view_invoice'),
]


