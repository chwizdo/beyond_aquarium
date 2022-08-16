from django.shortcuts import render, redirect
from django.views import View

class CustomerAboutUsView(View):
    def get(self, request):
        return render(request, 'c_about_us_view.html')
