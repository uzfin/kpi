from datetime import date
from users.models import User


def common_data(request):
    if not request.user.is_anonymous:
        ctx = {
            'user': request.user,
            'date': date.today(),
            'root_user': User,
        }

        if request.user.role == User.EMPLOYEE:
            ctx['notefications'] = request.user.notefications.filter(unread=True)

        return ctx
    
    return {}
