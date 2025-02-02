from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Portfolio, InvestmentRequest, UserProfile  
from admin_panel.models import Asset
from .models import Portfolio, WithdrawalRequest

# ✅ Landing Page
def landing_page(request):
    return render(request, 'user_dashboard/landing_page.html')


# ✅ Signup View (Requires Admin Approval)
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save user in database
            Portfolio.objects.create(user=user)  # Create user portfolio
            UserProfile.objects.create(user=user, is_verified=False)  # User requires admin approval
            messages.success(request, "Account created! Please wait for admin approval.")
            return redirect('landing_page')  # Redirect to home page after signup
    else:
        form = UserCreationForm()
    
    return render(request, 'user_dashboard/signup.html', {'form': form})


@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)

    # ✅ Restrict access if user is not verified
    if not user_profile.is_verified:
        messages.error(request, "Your account is not verified by the admin yet.")
        return redirect('landing_page')

    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    assets = Asset.objects.all()
    
    # ✅ Fetch ALL investments and withdrawals
    investments = InvestmentRequest.objects.filter(user=request.user)  
    withdrawals = WithdrawalRequest.objects.filter(user=request.user)  

    return render(request, 'user_dashboard/dashboard.html', {
        'portfolio': portfolio, 
        'assets': assets,
        'investments': investments,  # ✅ Pass investments
        'withdrawals': withdrawals  # ✅ Pass withdrawals
    })

# ✅ Investment Request Handling
@login_required
def invest(request, asset_id):
    try:
        asset = Asset.objects.get(id=asset_id)  # Fetch asset by ID
        if request.method == "POST":
            amount = request.POST.get("amount")
            InvestmentRequest.objects.create(user=request.user, asset=asset, amount=amount, status="pending")
            messages.success(request, "Your investment request has been submitted for approval.")
            return redirect('dashboard')
        return render(request, 'user_dashboard/invest.html', {'asset': asset})
    except Asset.DoesNotExist:
        messages.error(request, "Asset not found.")
        return redirect('dashboard')
@login_required
def request_withdrawal(request):
    portfolio = Portfolio.objects.get(user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")

        # ✅ Ensure withdrawal amount is valid
        if not amount or float(amount) <= 0:
            messages.error(request, "Invalid withdrawal amount.")
            return redirect('request_withdrawal')

        amount = float(amount)
        if amount > portfolio.total_investment:
            messages.error(request, "Insufficient funds for withdrawal.")
            return redirect('request_withdrawal')

        # ✅ Create Withdrawal Request
        withdrawal = WithdrawalRequest.objects.create(
            user=request.user, 
            amount=amount, 
            status="pending"
        )
        withdrawal.save()  # ✅ Ensure request is saved in the database

        messages.success(request, "Your withdrawal request has been submitted.")
        return redirect('transaction_history')

    return render(request, 'user_dashboard/request_withdrawal.html', {'portfolio': portfolio})