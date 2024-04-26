from datetime import date
from users.models import User


def common_data(request):
    return {
        'user': request.user,
        'date': date.today(),
        'root_user': User,
    }
