from django.urls import path
from . import views  

urlpatterns = [
    path('manage-investments/', views.manage_investments, name='manage_investments'),
    path('approve-investment/<int:investment_id>/', views.approve_investment, name='approve_investment'),
    path('reject-investment/<int:investment_id>/', views.reject_investment, name='reject_investment'),
    path('manage-withdrawals/', views.manage_withdrawals, name='manage_withdrawals'),
    path('approve-withdrawal/<int:withdrawal_id>/', views.approve_withdrawal, name='approve_withdrawal'),
    path('reject-withdrawal/<int:withdrawal_id>/', views.reject_withdrawal, name='reject_withdrawal'),
]