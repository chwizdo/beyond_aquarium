from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
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

    return HttpResponse('success')
    # return redirect('home')

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

    return HttpResponse('Success')


class UserCreateView(View):
  def get(self, request):
    return render(request, 'a_user_create_view.html')