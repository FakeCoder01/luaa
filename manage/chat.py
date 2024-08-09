from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@login_required(login_url='/manage')    
@staff_member_required(login_url='/manage')
def chat_page(request):
    pass

@login_required(login_url='/manage')    
@staff_member_required(login_url='/manage')
def chat_room(request, chat_id):
    pass