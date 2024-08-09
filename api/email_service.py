from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import json, logging
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

logger = logging.getLogger(__name__)
     
@shared_task
def send_email_to_users(subject, message, email_list):
    try:
        email_list = email_list.replace(" ", "")
        email_list = email_list.split(",")
        email_from = settings.EMAIL_HOST_USER
        send_mail( subject=subject, message=message, from_email=email_from, recipient_list=email_list, fail_silently=False,) 
    except Exception as err:
        logger.error(err)
        pass

@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def email_sent_many(request):
    try:
        if request.method == 'POST':
            subject = str(request.POST.get('subject', None))
            message = str(request.POST.get('message', None))
            email_list = str(request.POST.get('email_list', None))
            if subject != None and message != None and email_list != None:
                send_email_to_users.delay(subject, message, email_list)
                return JsonResponse(json.dumps({
                    "status_code" : 202,
                    "message" : "email(s) sent",
                    "total" : len(email_list)
                }), safe=False)
            logger.info(msg="All fields are reuired")
            return JsonResponse(json.dumps({
                "status_code" : 400,
                "message" : "all fields are required"
            }), safe=False)
        logger.info(msg="Only POST allowed")
        return JsonResponse(json.dumps({
            "status_code" : 403,
            "message" : "only post method allowed"
        }), safe=False)
    except Exception as err:
        logger.error(err)
        return JsonResponse(json.dumps({
                "status_code" : 500,
                "message" : "something went wrong"
        }), safe=False)
    
    
