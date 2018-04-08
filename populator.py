import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','proto.settings')

import django
django.setup()

from alerter.models import Alert_Definition,User




def poppy():
    
        
    rec = Alert_Definition.objects.get_or_create(
 alert_title= 'MASCC', category='Oncology',
severity='High Risk',updt_id=User.objects.get(user_identifier=1.0)
        )[0]
    rec.save()
        
if __name__ == '__main__':

    print('pop script')
    poppy()
    print ('pop end')
    





