from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone


def get_current_users():
    User = get_user_model()
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    user_id_list = []
    for session in active_sessions:
        #print(session.session_key)
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)