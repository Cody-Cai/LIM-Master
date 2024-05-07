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


from decimal import *
def decround(number, ndigits=None, roundtype="O"):
    """Round decimal """
    exp = Decimal('1.{}'.format(ndigits * '0')) if ndigits else Decimal('1')
    match roundtype:
        case "O":
            rounding = ROUND_HALF_UP
        case "U":
            rounding = ROUND_UP
        case "D":
            rounding = ROUND_DOWN

    return type(number)(Decimal(number).quantize(exp, rounding))