from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm
from .models import Product, Category, Profile
from .forms import SignUpForm, UserUpdateForm, PasswordUpdateForm, UserInfoForm
import json


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'store/index.html', context)


def product(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product
    }
    return render(request, 'store/product.html', context)


def category(request, slug):
    try:
        ctgry = Category.objects.get(slug=slug)
        products = Product.objects.filter(category=ctgry)
        context = {
         'category': ctgry,
         'products': products
        }
        return render(request, 'store/category.html', context)
    except:
        messages.success(request, ("That category doesn't exists."))
        return redirect('store:home')


def categories_summary(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }

    return render(request, 'store/categories_summary.html', context)


def search_items(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        if searched:
            result = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
            context = {
                'searched': searched,
                'result': result
            }
            return render(request, 'store/search.html', context)
    return render(request, 'store/search.html')


def about(request):
    return render(request, 'store/about.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.cart
            if saved_cart:
                # convert to dict using json
                converted_cart = json.loads(saved_cart)
                # add the loaded cart dictionary to session
                cart = Cart(request)
            #     loop through dict and add items to the cart

                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, ("You have been logged in..."))
            return redirect('store:home')
        else:
            messages.success(request, ("There was an error. Please try again..."))
            return redirect('store:login')
    return render(request, 'store/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out..."))
    return redirect('store:home')


def user_register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You registered successfully!"))
            return redirect('store:home')
        else:
            messages.success(request, ("Oops! There was a problem in the form... Please try again..."))
            return redirect('store:user_register')
    else:
        context = {
            'form': form
        }
        return render(request, 'store/user_register.html', context)


def user_update(request):

    if request.user.is_authenticated:
        user = request.user
        form = UserUpdateForm(request.POST or None, instance=user)
        shipping_form = ShippingForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            login(request, user)
            return redirect('store:login')
        else:
            context = {
                'form': form
            }
            messages.warning(request, ('Some errors occured... Please check and try again...'))
            return render(request, 'store/user_update.html', context)
    else:
        messages.warning(request, ('You must logged in...'))
        return redirect('store:login')


def info_update(request):
    if request.user.is_authenticated:
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        form = UserInfoForm(request.POST or None, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your informations has been changed...')
            return redirect('store:home')
        return render(request, 'store/info_update.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in...')
        return redirect('store:home')


def password_update(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            form = PasswordUpdateForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ('Your password changed successfully!'))
                # login(request, user)
                return redirect('store:home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('store:password_update')
        else:
            form = PasswordUpdateForm(user)
            return render(request, 'store/password_update.html', {'form': form})
    else:
        messages.warning(request, ('You must be logged in...'))
        return redirect('store:login')




