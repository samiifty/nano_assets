from django.contrib import admin
from user_dashboard.models import UserProfile, InvestmentRequest  
from user_dashboard.models import WithdrawalRequest
from django.contrib import admin
from .models import WithdrawalRequest




# ✅ Check if already registered before registering
if not admin.site.is_registered(UserProfile):
    class UserProfileAdmin(admin.ModelAdmin):
        list_display = ('user', 'is_verified')  # ✅ Show verification status
        list_editable = ('is_verified',)  # ✅ Allow admin to update directly

    admin.site.register(UserProfile, UserProfileAdmin)

if not admin.site.is_registered(InvestmentRequest):
    class InvestmentRequestAdmin(admin.ModelAdmin):
        list_display = ('user', 'asset', 'amount', 'status', 'created_at')  # ✅ Display all fields
        list_editable = ('status',)  # ✅ Allow status updates directly from the list view
        list_filter = ('status',)  # ✅ Add filters for Pending, Approved, Rejected
        search_fields = ('user__username', 'asset__name')  # ✅ Enable search

    admin.site.register(InvestmentRequest, InvestmentRequestAdmin)

class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at')  # ✅ Show withdrawal details
    list_editable = ('status',)  # ✅ Allow admin to update status
    list_filter = ('status',)  # ✅ Add filters for Pending, Approved, Rejected
    search_fields = ('user__username',)  # ✅ Enable search by username

admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)