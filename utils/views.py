from auths.models import Role
from django.shortcuts import redirect


class Util:
    ADMIN_HOMEPAGE = 'a_order'
    STAFF_HOMEPAGE = 'a_order'
    CUSTOMER_HOMEPAGE = 'c_product'
    LOGIN_PAGE = 'c_login'

    @staticmethod
    def redirect_if_authenticated(request):
        if request.user.is_authenticated:
            try:
                role = Role.objects.get(user_id=request.user.id)
            except Role.DoesNotExist:
                return redirect('c_product')

            if role.role == 'admin':
                return redirect(Util.ADMIN_HOMEPAGE)
            elif role.role == 'staff':
                return redirect(Util.STAFF_HOMEPAGE)
            else:
                return redirect(Util.CUSTOMER_HOMEPAGE)

        return None

    @staticmethod
    def redirect_if_unauthenticated(request):
        if not request.user.is_authenticated:
            return redirect(Util.LOGIN_PAGE)

        return None
