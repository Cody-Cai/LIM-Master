from basic.models import NumberSequenceTable
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def get_nextnumber(num_code):
    """
    get the number with format string  
    """
    try:
        num_seqtable = NumberSequenceTable.objects.get(number_code=num_code)
        if num_seqtable.next_rec == 0 or num_seqtable.next_rec > num_seqtable.highest:
            raise ValueError("Number sequence %(value)s has been exceeded." % {"value": str(num_seqtable.next_rec)})
        else:
            txtformat = num_seqtable.num_format
            x = txtformat.find('#')
            y = txtformat.rfind('#')
            sybollen = y - x + 1
            if sybollen < len(str(num_seqtable.next_rec)) or x == -1:
                raise ValueError("Number %(value)s does not match format %(sformat)s." % {"value": str(num_seqtable.next_rec), "sformat":txtformat})

            sub_format = txtformat[x:y+1]
            sub_new = str(num_seqtable.next_rec).zfill(sybollen)
            new_num = txtformat.replace(sub_format,sub_new) 
    except ObjectDoesNotExist as e:
        error_msg = "Number sequence %s does not exist." % num_code
        #print(e)
        ret = {"tags": "error", "message": error_msg}
    except ValueError as e:
        ret = {"tags": "error", "message": e}
    else:
        ret = {"tags": "success", "message": new_num}
        
    return ret