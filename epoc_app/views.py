from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
from django.db.models import Avg, Max, Min, Count
import django_tables2 as tables
from epoc_app.models import P_info, Patient
from .forms import CommandForm
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from epoc_app.serializers import Patient_serializer, Patient_serializer2, P_serializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def command_serializer(request):
    if request.method == 'GET':
        instance = Patient.objects.order_by('-date')[0] #latest('date')
        data = {
            'name': instance.name,
            'flow': instance.flow,
        }
        serialized_data = json.dumps(data)  # Serialize the dictionary to JSON
        return HttpResponse(serialized_data, content_type='application/json')

@csrf_exempt
def Spo2_serializer_agregar_data(request):

    if request.method == 'GET':
        snippets = P_info.objects.all()
        serializer = Patient_serializer2(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST': #Comunicación con ESP32
        data = JSONParser().parse(request)
        serializer = Patient_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            name=data['name']
            spo2=data['spo2']
            patient, created = Patient.objects.get_or_create(
                name=name, defaults={"name": name, "spo2": spo2, "flow": 0})
            if created==False:
                patient.spo2 = spo2
                patient.save(update_fields=["spo2"]) 
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

def spo2_chart(request,patient_id):
    labels = []
    data = []
    patient = get_object_or_404(Patient,pk=patient_id)
    queryset = P_info.objects.filter(name=patient.name).order_by('-date') #[:30]
    if(len(queryset)>30):
        queryset=queryset[:30]
    else:
        queryset=queryset[:len(queryset)]
    for entry in reversed(queryset):
        labels.append(str(entry.date.strftime("%m-%d %H:%M")))
        data.append(entry.spo2)
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required
def monitor(request):
    patients=Patient.objects.all()
    return render(request, 'monitor.html', {'patients': patients})


@login_required
def details_pat(request,name):
    user =  User.objects.get(name=name)
    patient =  Patient.objects.get(name=user)

    if request.method == 'POST':
        form = CommandForm(request.POST, instance=patient)

        if form.is_valid():
            patient.date=datetime.now()
            patient.save(update_fields=["date"]) 
            form.save()
    else:
        form = CommandForm()
        
    command_d = Patient.objects.filter(name=patient.name).last()
    spo2_d = P_info.objects.filter(name=patient.name).last()
    return render(request, 'pat_details.html', {'form': form, 'command': command_d, 'spo2': spo2_d, 'patient':patient})

def welcome(request):

    return render(request, 'welcome.html')

from accounts.models import User

@login_required
def admin(request):
    users = User.objects.filter(is_staff=True)

    return render(request, 'admin.html', {
        'users': users,
    })

from accounts.forms import AddUserForm, EditUserForm
from django.contrib.auth.models import Group
from django.contrib import messages

@login_required
def add_user(request):
    if request.user.has_perm('user.add_user'):
        if request.method == 'POST':
            form = AddUserForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = True
                user.set_password(request.POST.get('password'))
                user.save()

                if user.role == User.MEDIC:
                    group = Group.objects.get(name='Medics')
                    group.user_set.add(user)

                if user.role == User.PATIENT:
                    group = Group.objects.get(name='Patients')
                    group.user_set.add(user)
                    patient = Patient(name=user, flow=0, spo2=90)
                    patient.save()

                messages.success(request, ' Usuario agregado')

                return redirect('/epoc/admin/')  
        else:
            form = AddUserForm()
    
        return render(request, 'add_user.html', {
            'form': form
        })
    else:
        messages.error(request, 'No tiene permisos para agregar usuarios')
        return redirect('/epoc/admin/')
    
@login_required
def edit_user(request, uuid):
   if request.user.has_perm('user.edit_user'):
       user =  User.objects.get(pk=uuid)

       if request.method == 'POST':
           form = EditUserForm(request.POST, instance=user)

           if form.is_valid():
               form.save()
               
               if user.role == User.MEDIC:
                    group = Group.objects.get(name='Medics')
                    group.user_set.add(user)
                    group = Group.objects.get(name='Patients')
                    group.user_set.remove(user)
                    patient = get_object_or_404(Patient, name=user)
                    patient.delete()


               else:
                    group = Group.objects.get(name='Patients')
                    group.user_set.add(user)
                    group = Group.objects.get(name='Medics')
                    group.user_set.remove(user)
                    patient, created = Patient.objects.get_or_create(
                        name=user, defaults={"name": user, "spo2": 90, "flow": 0})

               messages.success(request,'The changes were saved')
               return redirect('/epoc/admin/')
       else:
           form=EditUserForm(instance=user)

       return render(request, 'edit_user.html', {
           'user': user,
           'form': form
       })
   else:
        messages.error(request, 'You don\'t have permission to edit users')
        return redirect('/epoc/admin/')