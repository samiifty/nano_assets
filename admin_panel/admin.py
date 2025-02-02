from django.contrib import admin
from .models import Asset, Investment, Transaction

admin.site.register(Asset)
admin.site.register(Investment)
admin.site.register(Transaction)


from user_dashboard.models import InvestmentRequest

class InvestmentRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'asset', 'amount', 'status', 'created_at')  # ✅ Display investment details
    list_filter = ('status',)  # ✅ Add filter for status (Pending, Approved, Rejected)
    search_fields = ('user__username', 'asset__name')  # ✅ Enable search by user or asset

admin.site.register(InvestmentRequest, InvestmentRequestAdmin)