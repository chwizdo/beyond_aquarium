from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class CustomerLoginView(View):
  def get(self, request):
    if request.user.is_authenticated:
      # check user's identity
      return redirect('c_product')

    return render(request, 'c_login_view.html')

  def post(self, request):
    if request.user.is_authenticated:
      # check user's identity
      return redirect('c_product')

    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(request=request, username=email, password=password)
    if user is not None:
      login(request=request, user=user)

    return redirect('c_product')

class CustomerSignUpView(View):
  def get(self, request):
    if request.user.is_authenticated:
      # check user's identity
      return redirect('c_product')

    return render(request, 'c_signup_view.html')

  def post(self, request):
    if request.user.is_authenticated:
      # check user's identity
      return redirect('c_product')

    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    re_password = request.POST.get('re-password')

    if password != re_password:
      # show error message
      return render(request, 'c_signup_view.html')

    User.objects.create_user(email, password=password, first_name=name, is_staff=True)

    return redirect('c_product')


class UserCreateView(View):
  def get(self, request):
    return render(request, 'a_user_create_view.html')
    

class CustomerProfileDetailView(View):
  def get(self, request):
    # Redirect user to login screen if user is unauthenticated.
    if not request.user.is_authenticated:
      return redirect('c_login')

    return render(request, 'c_profile_detail_view.html', {'user': request.user})

  def post(self, request):
    # Redirect user to login screen if user is unauthenticated.
    if not request.user.is_authenticated:
      return redirect('c_login')

    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    request.user.first_name = name
    request.user.username = email
    request.user.save()

    if password != '':
      request.user.set_password(password)
      request.user.save()
      login(request, request.user)

    return render(request, 'c_profile_detail_view.html', {'user': request.user})

  
class CustomerLogoutView(View):
  def get(self, request):
    # Redirect user to login screen if user is unauthenticated.
    if not request.user.is_authenticated:
      return redirect('c_login')

    logout(request)

    return redirect('c_login')
