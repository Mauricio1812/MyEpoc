from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
from epoc_app.models import P_info, Patient
from .forms import CommandForm
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from epoc_app.serializers import Patient_serializer, Patient_serializer2
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from accounts.models import User
from chat.models import Room


def command_serializer(request, name):
    if request.method == 'GET':
        user =  User.objects.get(name=name)
        patient =  Patient.objects.get(name=user)
        data = {
            'flow': patient.flow,
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

            #Delete P_info if there are more than 500 entries
            p_info_count = P_info.objects.count()
            if p_info_count > 800:
                for patient in Patient.objects.all():
                    if P_info.objects.filter(name=patient.name).count() > 30:
                        P_info.objects.filter(name=patient.name).order_by('date')[:-5].delete()

            #Update patient's spo2 and flow
            user =  get_object_or_404(User, name=data['name'])
            patient =  get_object_or_404(Patient, name=user)
            patient.spo2 = data['spo2']
            patient.flow = data['flow_real']
            patient.save(update_fields=["spo2", "flow_real"]) 

            # if(data['flow_real']>85):
            #     subject = "WETMOS - Alerta de paciente"
            #     recipient_list = user.email
            #     context = {'p_name': user.name,
            #                 'p_spo2': patient.spo2,
            #                 'p_flow': patient.flow}             

            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

def spo2_chart(request,patient_id):
    labels = []
    data = []
    flow = []
    patient = get_object_or_404(Patient,pk=patient_id)
    queryset = P_info.objects.filter(name=patient.name).order_by('-date') #[:30]
    flow_query = P_info.objects.filter(name=patient.name).order_by('-date')
    if(len(queryset)>30):
        queryset=queryset[:30]
        flow_query=flow_query[:30]

    for entry in reversed(queryset):
        labels.append(str(entry.date.strftime("%m-%d %H:%M")))
        data.append(entry.spo2)
        flow.append(entry.flow_real)
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'flow': flow
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

@login_required
def admin(request):
    users = User.objects.filter(is_staff=True)
    rooms = Room.objects.all()

    return render(request, 'admin.html', {
        'users': users,
        'rooms': rooms,
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

                messages.success(request, 'User added')

                return redirect('/epoc/admin/')  
        else:
            form = AddUserForm()
    
        return render(request, 'add_user.html', {
            'form': form
        })
    else:
        messages.error(request, 'You don\'t have permission to add users')
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
   
@login_required
def delete_user(request, uuid):
    if request.user.has_perm('user.delete_user'):
        user =  User.objects.get(pk=uuid)
        user.delete()
        messages.success(request, 'User deleted')
        return redirect('/epoc/admin/')
    else:
        messages.error(request, 'You don\'t have permission to delete users')
        return redirect('/epoc/admin/')