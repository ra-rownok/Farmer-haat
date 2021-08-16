from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from account.models import Profile
from .models import *
from main.forms import ProductForm, OrderForm
def index(request):

        profile = Profile.objects.all()
        context = {
                'profile': profile
        }
        return render(request, 'main/index.html', context)



def product(request):
        if request.user.is_authenticated:
                # productlist = product.objects.all()
                if request.method == 'POST':
                        product = Product.objects.all()
                        form = ProductForm(request.POST)
                        if form.is_valid():
                                name = form.cleaned_data['name']
                                quantity = form.cleaned_data['quantity']
                                price = form.cleaned_data['price']
                                post = Product(name=name,quantity=quantity, price=price, farmer_id=request.user.id)
                                post.save()
                                return redirect ('/productlist/')
                else:
                        form = ProductForm()
                        # product = Product.objects.all()
                return render(request, 'main/Product.html', {'form': form})
        else:
                return redirect('/login/')  
        

def order(request,pk):
        if request.user.is_authenticated:
                if request.method == 'POST':
                        product = Product.objects.get(id=pk)
                        
                        form = OrderForm(request.POST, instance=product)
                        if form.is_valid():
                                quantity = form.cleaned_data['quantity']
                                status = form.cleaned_data['status']
                                post = CustomerOrder(quantity=quantity, status=status, customer_id=request.user.id, product_id=product.id)
                                post.save()
                                return redirect ('/orderlist/')
                else:
                        form = OrderForm()
                
                return render(request, 'main/order.html', {'form': form})
        else:
                return redirect('/login/')


def farmer(request):
        farmer = Profile.objects.filter(profession__contains  = 'Farmer')
        context = {
                'farmer': farmer
        }
        return render (request, 'main/farmer.html', context)

def product_list(request):
        productlist = Product.objects.all()
        context = {
                'productlist': productlist
        }
        return render (request, 'main/productlist.html', context)

def order_list(request):
        product = Product.objects.all()
        orderlist = CustomerOrder.objects.all()
        context = {
                'orderlist': orderlist,
                'product': product
        }
        return render (request, 'main/orderlist.html', context)
