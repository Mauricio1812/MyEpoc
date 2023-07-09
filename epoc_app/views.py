from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
from django.db.models import Avg, Max, Min, Count
import django_tables2 as tables
from epoc_app.models import P_info, Patient
from .forms import CommandForm
import json

def command_serializer(request):
    if request.method == 'GET':
        instance = Patient.objects.order_by('-date')[0] #latest('date')
        data = {
            'name': instance.name,
            'flow': instance.flow,
        }
        serialized_data = json.dumps(data)  # Serialize the dictionary to JSON
        return HttpResponse(serialized_data, content_type='application/json')

# This class will create the table just like how we create forms
class SimpleTable(tables.Table):
   class Meta:
      model = P_info
      template_name = "django_tables2/semantic.html"

# This will render table
class TableView(tables.SingleTableView):
   table_class = SimpleTable
   queryset = P_info.objects.all()
   template_name = "Patient_table.html"

################################FUNCIONA

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from epoc_app.serializers import Patient_serializer, Patient_serializer2, P_serializer


@csrf_exempt
def Temp_serializer_agregar_data(request):
    """
    List all code snippets, or create a new snippet.
    """
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
    
##################################################################

def temp_chart(request,patient_id):
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

from django.contrib.auth.decorators import login_required

@login_required
def monitor(request):
    patients=Patient.objects.all()
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            flow = form.cleaned_data['flow']
            patient, created = Patient.objects.get_or_create(
                name=patient, defaults={"name": patient, "spo2": 95, "flow": flow})
            if created==False:
                ahora= datetime.now()
                patient.date=ahora
                patient.flow = flow
                patient.save(update_fields=["flow","date"]) 
    else:
        form = CommandForm()

    command_d = Patient.objects.last()
    spo2_d = P_info.objects.last()
    return render(request, 'monitor.html', {'patients': patients})


from django.shortcuts import get_object_or_404

@login_required
def details_pat(request,patient_id):
    
    patient = get_object_or_404(Patient,pk=patient_id)

    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            flow = form.cleaned_data['flow']
            patient, created = Patient.objects.get_or_create(
                name=patient, defaults={"name": patient, "spo2": 95, "flow": flow})
            if created==False:
                ahora= datetime.now()
                patient.date=ahora
                patient.flow = flow
                patient.save(update_fields=["flow","date"]) 
    else:
        form = CommandForm()
        
    command_d = Patient.objects.filter(name=patient.name).last()
    spo2_d = P_info.objects.filter(name=patient.name).last()
    return render(request, 'pat_details.html', {'form': form, 'command': command_d, 'spo2': spo2_d, 'patient':patient})

def welcome(request):
    return render(request, 'welcome.html')