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
def decimal_round(number, ndigits=None, roundtype="O"):
    """Round decimal """
    # Convert float to decimal
    number_dec = Decimal(str(number)) if type(number) == float else number

    exp = Decimal('1.{}'.format(ndigits * '0')) if ndigits else Decimal('1')
    match roundtype:
        case "O":
            rounding = ROUND_HALF_UP
        case "U":
            rounding = ROUND_UP
        case "D":
            rounding = ROUND_DOWN

    #return type(number)(Decimal(number).quantize(exp, rounding))
    return Decimal(number_dec).quantize(exp, rounding)


def get_decimal_places(number):
    """ decimal places """
    # 将小数转换为字符串
    number_str = str(number)
    # 分离整数部分和小数部分
    integer_part, decimal_part = number_str.split('.')
    # 返回小数部分的长度
    return len(decimal_part)






 