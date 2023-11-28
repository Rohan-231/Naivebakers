import json
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from naivebaker_app.models import Contact,Recipe
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage
from django.contrib.auth.decorators import login_required
from .models import *
from .helpers import send_forget_password_mail
from .views import *
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import base64
from urllib.parse import unquote




# Create your views here
def index(request) :
    return render(request,'index.html')

def myshowRecipe(request) :
    if request.user.is_anonymous:
        return redirect("/")
    if request.method == "POST" :
        owner = request.user
        print(owner)
        return redirect('/addRecipe')

    return render(request,'myshowRecipe.html')

def viewlogin(request) :
    
    if request.method == "POST" :
        uname = request.POST.get("username")
        pass1 = request.POST.get("pass")
        myuser = authenticate(username = uname,password = pass1)

        if myuser is not None :
            login(request,myuser)
            messages.success(request,"Logged In Successfully")
            return redirect('/home')
        else :
            messages.error(request,"Invalid Credentials")
            return redirect('/login')

    return render(request,'login.html')

def signup(request) :
        if request.method == "POST" :
            uname = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password1")
            confirmpassword = request.POST.get("password2")

            if (len(password) >= 8 and           # Minimum length of 8 characters
                any(char.isdigit() for char in password) and        # At least one digit
                any(char.isupper() for char in password) and        # At least one uppercase letter
                any(char in '!@#$%^&*(),.?":{}|<>' for char in password)  # At least one special character
                ):

                if password != confirmpassword :
                    messages.warning(request,"Password is Incorrect") 
                    return redirect('/signup')
                
                try : 
                    if User.objects.get(username=uname):
                        messages.info(request,'UserName is Taken')
                        return redirect('/signup')
                except :
                    pass
                try : 
                    if User.objects.get(email=email):
                        messages.info(request,'Email is Taken')
                        return redirect('/signup')
                except :
                    pass

                myuser = User.objects.create_user(uname,email,password)
                myuser.save()
                profile_obj = Profile.objects.create(user = myuser )
                profile_obj.save()
                messages.info(request,'Sign Up is Done Successfully,Please Login')
                return redirect('/signup')

            
            else:
                # Password is valid, you can save it to the database or perform other actions
                messages.error(request, "Enter valid password with one digit,one capital letter and one special charactor and length should greaater than 8.")
                return redirect('/signup')
                    
        return render(request,'signup.html')



def home(request) :
    if request.user.is_anonymous:
        return redirect('/')
    return render(request,'home.html')
    
def addRecipe(request) :
    if request.user.is_anonymous:
        return redirect("/")
    
    if request.method == "POST":
        recipe = Recipe()
        recipe.name = request.POST.get('recipeName')
        recipe.ingredients = request.POST.get('list_of_ingre')
        recipe.instructions = request.POST.get('steps')
        recipe.recipe_time = request.POST.get('recipeTime')
        recipe.vegitarity = request.POST.get('vegitarity')
        recipe.category = request.POST.get('category')
        recipe.meal_time = request.POST.get('mealtime')
        recipe.owner = request.user
        if len(request.FILES) != 0:
            recipe.image = request.FILES['image']
        recipe.save()
        messages.success(request, "Recipe is added successfully!!!")
        redirect('/addRecipe')

    return render(request,'addRecipe.html')

def home_view(request):
    if request.user.is_anonymous:
        return redirect("/")
    imageurl = request.GET.get('param1', '')
    recipename = request.GET.get('param2', '')
    cusinetype = request.GET.get('param3', '')
    meal_time = request.GET.get('param4', '')
    prep_time = request.GET.get('param5', '')
    cooklink = request.GET.get('param6', '')

    imageurl = base64.b64decode(imageurl).decode('utf-8')
    # Your processing logic goes here
    savedone = save_recipe()
    savedone.user =   request.user
    savedone.recipename = recipename
    savedone.image = imageurl
    savedone.cusinetype = cusinetype
    savedone.meal_time = meal_time
    savedone.preptime = prep_time
    savedone.cooklink = cooklink
    savedone.save()
    messages.success(request, "Recipe is added successfully!!")
    return redirect('/home')
    # return HttpResponse(f'param1: {imageurl}, param2: {recipename},param3:{cusinetype},param4:{meal_time},,param5:{prep_time},param6:{cooklink}')


def contact(request) :
        if request.user.is_anonymous:
            return redirect("/")
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            recipe_name = request.POST.get('recipe_name')
            phone = request.POST.get('phone')
            feedback = request.POST.get('message')
            contact = Contact(name=name,email=email,recipe_name = recipe_name,phone = phone,feedback=feedback,date = datetime.today())
            contact.save()
            messages.success(request, "Thanks for your valuable feedback")
            redirect('/contact')
        return render(request,'contact.html')

@login_required
def dashboard(request):
     if request.user.is_anonymous:
        return redirect("/")
     else :
        current_user = request.user
        username = current_user.username
        email = current_user.email
        context = {'username' : username,
                'email' : email}
        return render(request,'user_profile.html',context)

def saved_recipe(request):
    if request.user.is_anonymous:
        return redirect("/")
    user_id = request.user
    user_recipes = save_recipe.objects.filter(user_id=user_id)
    print(user_recipes)
    return render(request, 'saved_recipe.html', {'user_recipes': user_recipes})

def viewlogout(request) :
    logout(request)
    messages.info(request,"Logged Out Successfully")
    return redirect('/')

def myrecipe(request) :
    if request.user.is_anonymous:
        return redirect("/") 
    user_id = request.user
    user_recipes = Recipe.objects.filter(owner_id=user_id)
    return render(request, 'myrecipe.html', {'user_recipes': user_recipes})


def ChangePassword(request , token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            # print("coome on babayay")
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')                    
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login') 
            
    except Exception as e:
        print(e)
    return render(request , 'change-password.html' , context)

import uuid
def ForgetPassword(request):
    try:
        print("comes here")
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
                
    
    
    except Exception as e:
        print(e)
    return render(request , 'forget-password.html')

def addedrecipe_view(request):
    if request.user.is_anonymous:
        return redirect("/")
    owner = request.GET.get('param1', '')
    recipename = request.GET.get('param2', '')
    mealtime = request.GET.get('param3', '')
    category = request.GET.get('param4', '')
    recipetime = request.GET.get('param5', '')
    ingredients = request.GET.get('param6', '')
    instrctions = request.GET.get('param7','')

    ingredients = unquote(ingredients)
    instrctions = unquote(instrctions)
    
    context = {
        'owner': owner,
        'recipename': recipename,
        'mealtime': mealtime,
        'category': category,
        'recipetime': recipetime,
        'ingredients': ingredients,
        'instrctions': instrctions,
    }
    messages.success(request, "Recipe viewed successfully!!")
    return render(request, 'myshowRecipe.html', context)

def gulabjamun(request) :
    return render(request,'gulab.html')

def pavbhaji(request) :
    return render(request,'pavbhaji.html')

def friedrice(request) :
    return render(request,'friedrice.html')
