from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('invest/<int:asset_id>/', views.invest, name='invest'),
    path('invest/<int:asset_id>/', views.invest, name='invest'), 
    
    # ✅ Built-in authentication views for login/logout
    path('login/', auth_views.LoginView.as_view(template_name='user_dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('withdraw/', views.request_withdrawal, name='request_withdrawal'),  # ✅ Added Withdrawal Route
]
