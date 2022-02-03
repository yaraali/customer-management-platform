from django.contrib.auth import views as auth_views 
from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('createOrderForm/<str:pk>/', views.createOrder, name='createOrderForm'),
    path('updateOrder/<str:pk>/', views.updateOrder, name='updateOrder'), 
    path('deleteOrder/<str:pk>/', views.deleteOrder, name='deleteOrder'),  
    path('login/', views.loginPage, name="login"), 
    path('register/', views.registerPage, name="register"), 
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="userPage"),
    path('account/', views.accountSettings, name="account"),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),



]

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''
