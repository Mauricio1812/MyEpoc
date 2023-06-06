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

###############################
def grafico_hora(request):

    ahora= datetime.now()
    data = []
    labels =[]
    titulo= "Ultimos 60 segundos"
    #min = []
    #max = []
    #avg = []
    ultima_hora = ahora-timedelta(minutes=1)
    queryset = T_Vs_t.objects.filter(FECHA__range=(ultima_hora,ahora))
    #queryset = T_Vs_t.objects.all()[:1440] #1440 pts son las ultimas 24 hrs, considerando que la info se registra cada un min

    for maumau in queryset:
        data.append(maumau.TEMPERATURA)
        labels.append(str(maumau.FECHA.strftime("%Y-%m-%d %H:%M")))
        min= queryset.aggregate(Min("TEMPERATURA"))
        min = str(min)
        min = min[21:25]
        avg= queryset.aggregate(Avg("TEMPERATURA"))
        avg = str(avg)
        avg = avg[21:25]
        max= queryset.aggregate(Max("TEMPERATURA"))
        max = str(max)
        max = max[21:25]
        count= queryset.count()
        opcount = 60




    return render(request, 'grafico.html', {'labels': labels,'data': data, "min":min, "avg": avg, "max":max, "titulo":titulo, "count": count, "opcount": opcount})


################################

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
    for entry in queryset:
        labels.append(str(entry.date.strftime("%m-%d %H:%M")))
        data.append(entry.temperature)
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def index(request):
    return render(request, 'index.html')