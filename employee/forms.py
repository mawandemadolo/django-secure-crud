from django import forms
from .models import Employee
import re

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'employee_name': forms.TextInput(attrs={'maxlength': 100}),
            'employee_email': forms.EmailInput(attrs={'maxlength': 254}),
            'employee_contact': forms.TextInput(attrs={'maxlength': 15}),
        }
    
    def clean_employee_name(self):
        name = self.cleaned_data.get('employee_name')
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise forms.ValidationError('Name can only contain letters and spaces')
        return name.strip()
    
    def clean_employee_contact(self):
        contact = self.cleaned_data.get('employee_contact')
        if not re.match(r'^[\d\+\-\(\)\s]+$', contact):
            raise forms.ValidationError('Invalid contact format')
        return contact.strip()
    
    def clean_employee_email(self):
        email = self.cleaned_data.get('employee_email')
        return email.lower().strip()