from registration.backends.simple.views import RegistrationView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse 
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm
from rango.forms import UserProfileForm
from rango.bing_search import run_query

def index(request):
    context_dict = {}
    category_list = Category.objects.order_by('-likes')[:5]
    most_viwed_page = Page.objects.order_by('-views')[:5]
    context_dict['categories'] = category_list
    context_dict['most_viwed_pages'] = most_viwed_page
    return render(request, 'rango/index.html', context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request,'rango/category.html', context_dict)

def about(request):
    return render(request,'rango/about.html')

@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            cat = form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form':form})

@login_required
def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views =0
                page.save()
                return show_category(request, category_name_slug)
            else:
                print(form.errors)

    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid and profile_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html', context = {'user_form':user_form, 'profile_form':profile_form,'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = authenticate(username =username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('index'))

            else:
                return HttpResponse("Your account is disabled")
        else:
            print(f'Invalid login details: {username}, {password}')
            return HttpResponse("Invalid Login Credentials")

    else:
        return render(request, 'rango/login.html')        

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

# class MyRegistrationView(RegistrationView):
#     def get_success_url(self, user):
#         return reverse('index')

def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    
    return render(request, 'rango/search.html', {'result_list': result_list})