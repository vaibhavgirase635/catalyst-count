from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.views import View
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User
from django.db.models import Q
from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .task import process_csv_file
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
import pandas as pd

# Create your views here.



def register_user(request):
    if request.method == 'POST':
        
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        query = User.objects.filter(Q(email=email) | Q(username=username))
        if query.exists():
            messages.error(request, "Username or Email Already Exists !", extra_tags="alert alert-warning alert-dismissible show")
            return redirect('register')
        if password1 == password2:
            
            user = User.objects.create_user(email=email,username=username,password=password1)
            
            return redirect('login')
        else:
            messages.error(request, "Password and Confirm Password not matched", extra_tags="alert alert-warning alert-dismissible show")
            return redirect('register')  # Redirect to your home page or wherever you want
    
    return render(request, 'myapp/register.html')

class LoginView(View):
    def get(self, request):
        
        return render(request, 'myapp/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password1')
        print(password)
        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Email or password is incorrect", extra_tags="alert alert-warning alert-dismissible show")
            return redirect('login')

@login_required
def home(request):
    print("call")
    if request.method == 'POST':

        file = request.FILES.get('file')
        if file:
            print(file)

            file_path = handle_uploaded_file(file)
            print(file_path)
                # Schedule the background task
            id=request.user.id
            process_csv_file.delay(file_path,id)
            
            return JsonResponse({'message': 'File uploaded successfully'},status=200)
        return JsonResponse({'error': 'File is not uploaded'}, status=400)
    
    return render(request, "myapp/home.html")

def handle_uploaded_file(file):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
    file_path = os.path.join(upload_dir, file.name)
    print("file in handle", file_path)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path


@login_required
def query_builder(request):
    company_names = Company.objects.all().order_by('industry')
    
    # Initialize the industrys list before using it
    industrys = []
    for i in company_names:
        if i.industry not in industrys:
            industrys.append(i.industry)
    
    years = [i for i in range(1950, 2024)]
    
    coutnry_names = Company.objects.all().order_by('country')
    
    # Initialize the countrys list before using it
    countrys = []
    for i in coutnry_names:
        if i.country not in countrys:
            countrys.append(i.country)
    
    employee_from = [i for i in range(1, 10000)]
    employee_to = [i for i in range(1, 15000)]
    
    context = {
        'industrys': industrys,
        'years': years,
        'countrys': countrys,
        'employee_from': employee_from,
        'employee_to': employee_to
    }
    
    return render(request, 'myapp/query.html', context=context)

class Query_Builder(APIView):
    print('call')
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print("post request")
        data = request.data
        print(data)
        industry = data.get('industry')
        print(industry)
        year = data.get('founded')
        print(year)
        city = data.get('city')
        print(city)
        state = data.get('state')
        print(state)
        country = data.get('country')
        print(country)
        employee_from = data.get('employee_from')
        print(employee_from)
        employee_to = data.get('employee_to')
        print(employee_to)
        data = Company.objects.filter(user=request.user)
        print(data)
        data = data.filter(Q(industry__icontains=industry) & Q(year_founded=year) & Q(locality__startswith=city) & 
                           Q(locality__icontains=f", {state},") & Q(country__icontains=country) & Q(current_employee_estimate__gte=employee_from) &
                        Q(current_employee_estimate__lte=employee_to))
        print(data)
        return JsonResponse({'quantity':data.count()})
    
class Show_user(View):
    def get(self,request):
        users = User.objects.all()
        return render(request, 'myapp/show_users.html',{'users':users,'title':"All Users"})

class UserRegistrationView(View):
    def get(self,request):
        form = Add_User_Form()
        return render(request, 'myapp/add_user.html',{'form':form})
    def post(self, request):
        form = Add_User_Form(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('user_pass')
            user.set_password(password)
            user.save()
            messages.success(request, 'New User Added', extra_tags='alert alert-success alert-dismissible show')
            return redirect('show_users')
        else:
            messages.error(request, 'Something went wrong, Please check bellow', extra_tags='alert alert-error alert-dismissible show')
            
            return render(request,'myapp/add_user.html',{'form':form})
    
def user_logout(request):
    logout(request)
    return redirect('login')

def delete_user(request ,id):
    obj = User.objects.get(id=id)
    obj.delete()
    messages.success(request, f'{obj.first_name} {obj.last_name} Deleted Successfully', extra_tags='alert alert-success alert-dismissible show')
    return redirect("show_users")