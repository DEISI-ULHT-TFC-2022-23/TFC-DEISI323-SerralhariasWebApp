from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from .forms import addProductForm, RegisterForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import addProduct




def base_page_view(request):
    return render(request, 'proj/base.html')

def home_page_view(request):
    # This is to check the credentials on the terminal
    print(request.session.items()) 
     # Query all products
    products = addProduct.objects.all()

    # Gets the distinct categories from all product objects on DB
    categories = addProduct.objects.order_by().values_list('type', flat=True).distinct()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'proj/home.html', context)

def category_page_view(request, category):
    #addd to products all of the other products of the same type/caregory
    products = addProduct.objects.filter(type = category)
    context = {
        'products': products,
        'category': category
    }
    return render(request, "proj/category.html", context)

def product_page_view(request, id):
     # Gets the product by ID from the DB
    product = get_object_or_404(addProduct, pk=id)

    # Gets the distinct categories/types from all product objects on DB
    categoryTypes = addProduct.objects.order_by().values_list('type', flat=True).distinct()

    #Gets all realated products with the same type into relatedProducts expect the present one
    productType = product.type
    relatedProducts = addProduct.objects.filter(type=productType).exclude(id=product.id)

    context = {
        'product': product,
        'categories': categoryTypes,
        'relatedProducts': relatedProducts
    }
    return render(request, 'proj/product.html', context)

def add_product_page_view(request):
    form = addProductForm(request.POST)
    
    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'proj/addProduct.html', {'form': form})

def register_page_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    
    form = RegisterForm()
    return render(request, 'proj/register.html', {'form': form})



def login_page_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'proj/login.html', {'form': form})