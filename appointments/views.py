from django.shortcuts import render
from utils.views import Util
from django.views import View

class CustomerContactUsView(View):
  def get(self, request):
    unauthenticated_res = Util.redirect_if_unauthenticated(request)

    if unauthenticated_res is not None:
        return unauthenticated_res

    return render(request, 'c_contact_us_view.html')
