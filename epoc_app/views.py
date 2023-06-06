from django.shortcuts import render
from django.http import HttpResponse
from .models import T_Vs_t
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Avg, Max, Min, Count
import django_tables2 as tables

from epoc_app.models import P_info, P_command
from .forms import CommandForm
import json

###############################
def command(request):
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            airflow = form.cleaned_data['airflow']
            model = P_command(name=patient, oxygenflow=airflow)
            model.save()
            # return redirect('success')  # Redirect to a success page or another URL
    else:
        form = CommandForm()

    return render(request, 'commands.html', {'form': form})

def command_serializer(request):
    if request.method == 'GET':
        instance = P_command.objects.last() #latest('date')

        data = {
            'id': instance.id,
            'name': instance.name,
            'number': instance.oxygenflow,
        }
        serialized_data = json.dumps(data)  # Serialize the dictionary to JSON
        return HttpResponse(serialized_data, content_type='application/json')


###############################

# this class will create the table just like how we create forms
class SimpleTable(tables.Table):
   class Meta:
      model = P_info
      template_name = "django_tables2/semantic.html"

# this will render table
class TableView(tables.SingleTableView):
   table_class = SimpleTable
   queryset = P_info.objects.all()
   template_name = "Patient_table.html"

################################FUNCIONA

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from epoc_app.models import T_Vs_t
from epoc_app.serializers import Temp_serializer
from epoc_app.serializers import Temp_serializer2
from epoc_app.serializers import Patient_serializer
from epoc_app.serializers import Patient_serializer2


@csrf_exempt
def Temp_serializer_agregar_data(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = P_info.objects.all()
        serializer = Patient_serializer2(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Patient_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
##################################################################

from datetime import timedelta
def temp_chart(request):
    #ahora= datetime.now()
    #ahora = P_info.objects.order_by('-date')[0]
    labels = []
    data = []
    #ultima_hora = ahora-timedelta(hours=1)
    queryset = P_info.objects.order_by('-date')[:30] #Sale al reves
    #queryset = P_info.objects.all().filter(ultima_hora, ahora)
    for entry in reversed(queryset):
        labels.append(str(entry.date.strftime("%m-%d %H:%M")))
        data.append(entry.temperature)
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def index(request):
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            airflow = form.cleaned_data['airflow']
            model = P_command(name=patient, oxygenflow=airflow)
            model.save()
    else:
        form = CommandForm()

    return render(request, 'index.html', {'form': form})
