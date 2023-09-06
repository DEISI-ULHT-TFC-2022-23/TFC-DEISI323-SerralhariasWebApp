from django.shortcuts import render, redirect
from .forms import AddProductForm, RegisterForm, LoginForm, UserEditForm, CustomOrderForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User

from app.models import Product, Category, UserProfile, Wish, Image, Order

def base_page_view(request):
    return render(request, 'proj/base.html')

def home_page_view(request):
    # This is to check the credentials on the terminal
    print(request.session.items())

    search = request.GET.get("search", "")
    query = Q(name__icontains=search) | Q(description__icontains=search)

    # Query all products
    if request.user.is_staff:
        products = Product.objects.filter(query)
    else:
        products = Product.objects.filter(query, unlisted=False)

    # Gets the distinct categories from all product objects on DB
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'user': request.user,
        'search': search,
    }
    return render(request, 'proj/home.html', context)

def category_page_view(request, id):
    #addd to products all of the other products of the same type/caregory
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category=category)
    
    # Get user id from request
    user_id = None if request.user is None else request.user.id
    context = {
        'products': products,
        'category': category,
        'user_id': user_id
    }
    return render(request, "proj/category.html", context)

def product_page_view(request, id):
    # Gets the product by ID from the DB
    product = Product.objects.get(pk=id)

    # Gets the distinct categories/types from all product objects on DB
    categories = Category.objects.all()

    #Gets all realated products with the same type into relatedProducts expect the present one
    relatedProducts = Product.objects.filter(category=product.category).exclude(pk=product.id)

    # Get user id from request
    user_id = None if request.user is None else request.user.id
    context = {
        'product': product,
        'categories': categories,
        'relatedProducts': relatedProducts,
        'user_id': user_id
    }
    return render(request, 'proj/product.html', context)

def add_product_page_view(request):
    form = AddProductForm()

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            data.pop("images")

            with transaction.atomic():
                product = Product.objects.create(**data)

                for file in request.FILES.getlist('images'):
                    image = Image.objects.create(image=file)
                    product.images.add(image)
            
            return redirect('home')
    
    return render(request, 'proj/addProduct.html', {'form': form})

def edit_product_page_view(request, id):
    product = Product.objects.get(pk=id)
    form = AddProductForm(dict(
        name = product.name,
        category = product.category,
        description = product.description,
        price = product.price
    ))

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            data.pop("images")

            with transaction.atomic():
                product.name = data["name"]
                product.category = data["category"]
                product.description = data["description"]
                product.price = data["price"]

                for file in request.FILES.getlist('images'):
                    image = Image.objects.create(image=file)
                    product.images.add(image)

                product.save()
            
            return redirect('home')
    
    return render(request, 'proj/editProduct.html', {'form': form})

def add_custom_order_page_view(request, id):
    form = CustomOrderForm()
    product = Product.objects.get(pk=id)

    if request.method == 'POST':
        form = CustomOrderForm(request.POST)
        if form.is_valid():
            form.instance.product = product
            form.instance.user = request.user
            form.instance.save()
            return redirect('home')

    return render(request, 'proj/custom_order.html', {'form': form, 'product': product})

def register_page_view(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user = user)
            login(request, user)
            return redirect('home')

    return render(request, 'proj/register.html', {'form': form})

def login_page_view(request):
    form = LoginForm()

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

    return render(request, 'proj/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def product_change_list_status_view(request, id):
    product = Product.objects.get(pk=id)
    product.unlisted = not product.unlisted
    product.save()
    return redirect('home')

def product_remove_view(request, id):
    product = Product.objects.get(pk=id)
    with transaction.atomic():
        for image in product.images.all():
            image.delete()
        product.delete()
    return redirect('home')

def user_profile_view(request):
    if request.user and request.user.is_authenticated:
        wish_list = Wish.objects.filter(user_id=request.user.id)
        custom_orders = Order.objects.filter(user_id=request.user.id, description__isnull=False)
        users = User.objects.all()
        user_id = None if request.user is None else request.user.id
        return render(request, 'proj/user_profile.html', {
            'user_profile': request.user.userprofile,
            'wish_list': wish_list,
            'users': users,
            'user_id': user_id,
            'custom_orders': custom_orders
        })
    return redirect('login')

def user_profile_edit_view(request):
    if request.user and request.user.is_authenticated:
        form = UserEditForm(instance=request.user.userprofile)
        
        if request.POST:
            form = UserEditForm(request.POST, instance=request.user.userprofile)
            if form.is_valid():
                form.save()
                return redirect('userProfile')

        return render(request, 'proj/user_profile_edit.html', {'form': form})
    return redirect('login')

def user_change_block_status_view(request, id):
    if request.user.is_staff:
        user = User.objects.get(pk=id)
        user.is_active = not user.is_active
        user.save()
    return redirect('userProfile')

def user_delete_view(request, id):
    if request.user.is_staff:
        User.objects.get(pk=id).delete()
    return redirect('userProfile')

def add_wish_list_view(request):
    if request.method == "POST" and request.user and request.user.is_authenticated:
        if "product_id" in request.POST:
            wish = Wish.objects.filter(
                user_id=request.user.id,
                product_id=request.POST["product_id"],
            )
            if wish.exists():
                wish.delete()
                return HttpResponse(status=204)
            else:
                Wish.objects.create(
                    user_id=request.user.id,
                    product_id=request.POST["product_id"],
                )
                return HttpResponse(status=200)
        return HttpResponse(status=400)
    return HttpResponse(status=405)