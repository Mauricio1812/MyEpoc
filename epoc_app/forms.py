from django import forms
from .models import Patient

class CommandForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('flow',)
        widgets = {
            'flow': forms.NumberInput(attrs={
                'class': 'py-2 px-2 rounded-xl border'
            })
        }
