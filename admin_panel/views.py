from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user_dashboard.models import InvestmentRequest, Portfolio
from user_dashboard.models import WithdrawalRequest, Portfolio

def manage_investments(request):
    investments = InvestmentRequest.objects.all()  # ✅ Fetch all investment requests
    return render(request, 'admin_panel/manage_investments.html', {'investments': investments})

def approve_investment(request, investment_id):
    investment = get_object_or_404(InvestmentRequest, id=investment_id)
    
    # ✅ Update status to "approved"
    investment.status = 'approved'
    investment.save()

    # ✅ Update user’s portfolio total investment
    portfolio, created = Portfolio.objects.get_or_create(user=investment.user)
    portfolio.total_investment += investment.amount
    portfolio.save()

    messages.success(request, f"Investment for {investment.asset.name} has been approved.")
    return redirect('manage_investments')

def reject_investment(request, investment_id):
    investment = get_object_or_404(InvestmentRequest, id=investment_id)
    
    # ✅ Update status to "rejected"
    investment.status = 'rejected'
    investment.save()

    messages.error(request, f"Investment for {investment.asset.name} has been rejected.")
    return redirect('manage_investments')


def manage_investments(request):
    investments = InvestmentRequest.objects.all()  # ✅ Fetch all investments
    return render(request, 'admin_panel/manage_investments.html', {'investments': investments})




def manage_withdrawals(request):
    withdrawals = WithdrawalRequest.objects.all()  # ✅ Fetch ALL withdrawals (not just pending)
    return render(request, 'admin_panel/manage_withdrawals.html', {'withdrawals': withdrawals})

def approve_withdrawal(request, withdrawal_id):
    withdrawal = WithdrawalRequest.objects.get(id=withdrawal_id)
    portfolio = Portfolio.objects.get(user=withdrawal.user)

    if withdrawal.amount > portfolio.total_investment:
        messages.error(request, "Insufficient funds to approve this withdrawal.")
        return redirect('manage_withdrawals')

    # ✅ Deduct amount from user's portfolio
    portfolio.total_investment -= withdrawal.amount
    portfolio.save()

    withdrawal.status = 'approved'
    withdrawal.save()

    messages.success(request, "Withdrawal approved successfully.")
    return redirect('manage_withdrawals')

def reject_withdrawal(request, withdrawal_id):
    withdrawal = WithdrawalRequest.objects.get(id=withdrawal_id)
    withdrawal.status = 'rejected'
    withdrawal.save()

    messages.error(request, "Withdrawal request has been rejected.")
    return redirect('manage_withdrawals')