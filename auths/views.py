from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from auths.models import Role
from utils.views import Util

class CustomerLoginView(View):
  def get(self, request):
    authenticated_res = Util.redirect_if_authenticated(request)

    if authenticated_res is not None:
      return authenticated_res

    return render(request, 'c_login_view.html')

  def post(self, request):
    authenticated_res = Util.redirect_if_authenticated(request)

    if authenticated_res is not None:
      return authenticated_res

    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(request=request, username=email, password=password)
    if user is not None:
      login(request=request, user=user)

    try:
        role = Role.objects.get(user_id=request.user.id)
    except Role.DoesNotExist:
      return redirect('c_product')

    if role.role == 'admin':
      return redirect('a_order')
    else:
      return redirect('c_product')

class CustomerSignUpView(View):
  def get(self, request):
    authenticated_res = Util.redirect_if_authenticated(request)

    if authenticated_res is not None:
      return authenticated_res

    return render(request, 'c_signup_view.html')

  def post(self, request):
    authenticated_res = Util.redirect_if_authenticated(request)

    if authenticated_res is not None:
      return authenticated_res

    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    re_password = request.POST.get('re-password')

    if password != re_password:
      # show error message
      return render(request, 'c_signup_view.html')

    User.objects.create_user(email, password=password, first_name=name, is_staff=True)

    return redirect('c_product')


class AdminUserView(View):
  def get(self, request):
    unauthenticated_res = Util.redirect_if_unauthenticated(request)

    if unauthenticated_res is not None:
      return unauthenticated_res

    users = User.objects.all()

    return render(request, 'a_user_view.html', {'users': users})


class AdminUserDetailView(View):
  def get(self, request, user_id):
    unauthenticated_res = Util.redirect_if_unauthenticated(request)

    if unauthenticated_res is not None:
      return unauthenticated_res

    # If user id is not present in the path parameter,
    # redirect user back to user listing page.
    if user_id is None:
        return redirect('a_user')

    # Query user object from user id in path parameter,
    # if user object is not found, redirect user back to user listing page.
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('a_user')

    try:
      role = Role.objects.get(user_id=user.id)
      role_name = role.role
    except:
      role_name = None

    return render(request, 'a_user_detail_view.html', {'selected_user': user, 'role': role_name})

  def post(self, request, user_id):
    unauthenticated_res = Util.redirect_if_unauthenticated(request)

    if unauthenticated_res is not None:
      return unauthenticated_res

    # If user id is not present in the path parameter,
    # redirect user back to user listing page.
    if user_id is None:
        return redirect('a_user')

    # Query user object from user id in path parameter,
    # if user object is not found, redirect user back to user listing page.
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('a_user')

    try:
      role = Role.objects.get(user_id=user.id)
    except:
      role = None

    method = request.POST.get('_method')

    if method == 'PUT':
      name = request.POST.get('name')
      email = request.POST.get('email')
      password = request.POST.get('password')
      input_role = request.POST.get('role')

      if input_role == 'customer':
        input_role = None

      user.first_name = name
      user.username = email
      user.save()

      if password != '':
        user.set_password(password)
        user.save()

      if role is None and input_role is not None:
        Role.objects.create(user_id=user.id, role=input_role)
        role_name = input_role
      elif role is not None and input_role is not None:
        role.role = input_role
        role.save()
        role_name = input_role
      elif role is not None and input_role is None:
        role.delete()
        role_name = None
      else:
        role_name = None

    return render(request, 'a_user_detail_view.html', {'selected_user': user, 'role': role_name})


class AdminUserCreationView(View):
  def get(self, request):
    unauthenticated_res = Util.redirect_if_unauthenticated(request)

    if unauthenticated_res is not None:
      return unauthenticated_res

    return render(request, 'a_user_create_view.html')
  def post(self, request):
    unauthenticated_res = Util.redirect_if_unauthenticated(request)

    if unauthenticated_res is not None:
      return unauthenticated_res
      
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    role = request.POST.get('role')

    user = User.objects.create_user(email, password=password, first_name=name)

    if role != 'customer':
      Role.objects.create(user_id=user.id, role=role)
    
    return redirect('a_user')


class CustomerProfileDetailView(View):
  def get(self, request):
    unauthenticated_res = Util.redirect_if_unauthenticated(request)

    if unauthenticated_res is not None:
      return unauthenticated_res

    return render(request, 'c_profile_detail_view.html', {'user': request.user})

  def post(self, request):
    unauthenticated_res = Util.redirect_if_unauthenticated(request)

    if unauthenticated_res is not None:
      return unauthenticated_res

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
    unauthenticated_res = Util.redirect_if_unauthenticated(request)

    if unauthenticated_res is not None:
      return unauthenticated_res

    logout(request)

    return redirect('c_login')
