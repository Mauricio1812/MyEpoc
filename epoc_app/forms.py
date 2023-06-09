from django import forms

class CommandForm(forms.Form):
    patient = forms.CharField(label='Patient', max_length=100)
    flow = forms.FloatField(label='Flow')
