from django.shortcuts import render, redirect
from .models import Appointment, Feedback
from utils.views import Util
from django.views import View
import datetime
from auths.models import Role

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


class AdminAppointmentView(View):
    def get(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        appointments = Appointment.objects.all()

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_appointment_view.html', {'role': role.role, 'appointments': appointments})


class AdminAppointmentDetailView(View):
    def get(self, request, appointment_id):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        # If user id is not present in the path parameter,
        # redirect user back to user listing page.
        if appointment_id is None:
            return redirect('a_appointment')

        # Query user object from user id in path parameter,
        # if user object is not found, redirect user back to user listing page.
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return redirect('a_appointment')

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_appointment_detail_view.html', {'role': role.role, 'appointment': appointment})

    def post(self, request, appointment_id):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        # If user id is not present in the path parameter,
        # redirect user back to user listing page.
        if appointment_id is None:
            return redirect('a_appointment')

        # Query user object from user id in path parameter,
        # if user object is not found, redirect user back to user listing page.
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return redirect('a_appointment')

        method = request.POST.get('_method')

        if method == 'PUT':
            date = request.POST.get('date')
            reason = request.POST.get('reason')

            appointment.date = date
            appointment.reason = reason
            appointment.save()
        elif method == 'DELETE':
            appointment.delete()

            return redirect('a_appointment')

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_appointment_detail_view.html', {'role': role.role, 'appointment': appointment})


class AdminAppointmentCreateView(View):
    def get(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_appointment_create_view.html', {'role': role.role})

    def post(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        date = request.POST.get('date')
        reason = request.POST.get('reason')
        Appointment.objects.create(user_id=request.user.id, date=date, reason=reason)

        return redirect('a_appointment')


class AdminFeedbackView(View):
    def get(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        feedbacks = Feedback.objects.all()

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_feedback_view.html', {'role': role.role, 'feedbacks': feedbacks})


class AdminFeedbackDetailView(View):
    def get(self, request, feedback_id):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        # If user id is not present in the path parameter,
        # redirect user back to user listing page.
        if feedback_id is None:
            return redirect('a_feedback')

        # Query user object from user id in path parameter,
        # if user object is not found, redirect user back to user listing page.
        try:
            feedback = Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return redirect('a_feedback')

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_feedback_detail_view.html', {'role': role.role, 'feedback': feedback})

    def post(self, request, feedback_id):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        # If user id is not present in the path parameter,
        # redirect user back to user listing page.
        if feedback_id is None:
            return redirect('a_feedback')

        # Query user object from user id in path parameter,
        # if user object is not found, redirect user back to user listing page.
        try:
            feedback = Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return redirect('a_feedback')

        method = request.POST.get('_method')

        if method == 'PUT':
            content = request.POST.get('feedback')
            
            feedback.content = content
            feedback.save()
        elif method == 'DELETE':
            feedback.delete()

            return redirect('a_feedback')

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_feedback_detail_view.html', {'role': role.role, 'feedback': feedback})


class AdminFeedbackCreateView(View):
    def get(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_feedback_create_view.html', {'role': role.role})

    def post(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        content = request.POST.get('feedback')
        Feedback.objects.create(user_id=request.user.id, content=content)

        return redirect('a_feedback')

