from datetime import date
from users.models import User


def common_data(request):
    if not request.user.is_anonymous:
        ctx = {
            'user': request.user,
            'date': date.today(),
            'root_user': User,
        }

        if request.user.role in (User.EMPLOYEE, User.BOSS, User.MANAGER):
            ctx['notefications'] = request.user.notefications.filter(unread=True)

        if 'current_kpi' in request.session:
            ctx['current_kpi'] = request.session['current_kpi']
            
        return ctx
    
    return {}
