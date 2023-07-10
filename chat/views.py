import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Room
from accounts.models import User
from django.shortcuts import render, redirect
from accounts.forms import AddUserForm, EditUserForm

@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')

    Room.objects.create(uuid=uuid, client=name, url=url)

    return JsonResponse({'message': 'room created'})

@login_required
def room(request, uuid):
    room = Room.objects.get(uuid=uuid)

    if room.status == Room.WAITING:
        room.status = Room.ATTENDED
        room.agent = request.user
        room.save()

    return render(request, 'room.html', {
        'room': room
    })

@login_required
def delete_room(request, uuid):
    if request.user.has_perm('room.delete_room'):
        room = Room.objects.get(uuid=uuid)
        room.delete()
        messages.success(request, 'Chat deleted')
        return redirect('/epoc/admin/')
    else:
        messages.error(request, 'You don\'t have permission to delete chats')
        return redirect('/epoc/admin/')