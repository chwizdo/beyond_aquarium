from django.shortcuts import render
from .models import Appointment, Feedback
from utils.views import Util
from django.views import View
import datetime

class CustomerContactUsView(View):
    def get(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        return render(request, 'c_contact_us_view.html')


    def post(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        method = request.POST.get('_method')

        if method == 'appointment':
            date = request.POST.get('date')
            reason = request.POST.get('reason')

            date_splitted = date.split('-')
            date = datetime.date(int(date_splitted[0]), int(date_splitted[1]), int(date_splitted[2]))

            Appointment.objects.create(user_id=request.user.id, date=date, reason=reason)
        elif method == 'feedback':
            feedback = request.POST.get('feedback')

            Feedback.objects.create(user_id=request.user.id, content=feedback)

        return render(request, 'c_contact_us_view.html')