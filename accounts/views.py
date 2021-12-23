from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import OrderFilter
from accounts import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
# Create your views here.



@login_required(login_url='login')
@admin_only
def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total = Order.objects.all().count()
    delivred= Order.objects.filter(status='Delivered').count()
    pending= Order.objects.filter(status='Pending').count()
    context={'customers':customers, 'orders':orders, 'total':total, 'delivred':delivred, 'pending':pending   }
    return render(request,'dashboard.html',context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()
    total = orders.count()
    delivred= orders.filter(status='Delivered').count()
    pending= orders.filter(status='Pending').count()
    print('ORDERS: ', orders)
    context={'orders':orders,'total':total, 'delivred':delivred, 'pending':pending}
    return render(request,'user.html',context )


@unauthenticatedUser
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
	context = {'form':form}
	return render(request, 'register.html', context)


@unauthenticatedUser
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password= request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    
    context={}
    return render(request,'login.html',context )

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accountSettings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products= Product.objects.all()
    context={'products':products}
    return render(request,'products.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customers=Customer.objects.get(id=pk)
    orders=customers.order_set.all()
    orderCount= orders.count()
    searchFilter = OrderFilter(request.GET , queryset=orders)
    orders = searchFilter.qs
    context={'customers':customers,'myFilter': searchFilter , 'orders':orders,'orderCount':orderCount }
    return render(request,'customer.html',context )


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet= inlineformset_factory(Customer, Order, fields=('product','status'), extra=10)
    customer= Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form=OrderForm(initial={'customer':customer})
    if request.method == 'POST':  
        #form = OrderForm(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset}
    return render(request,'createOrderForm.html',context )


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk): 
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) 
    if request.method == 'POST': 
       form = OrderForm(request.POST, instance=order)
       if form.is_valid():
           form.save()        
           return redirect('/')
    context = {'form':form}
    return render(request , 'createOrderForm.html', context )


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk): 
    order = Order.objects.get(id=pk) 
    if request.method == 'POST':  
        order.delete()
        return redirect('/')

    context = {'order':order}

    return render(request , 'deleteOrder.html', context )


