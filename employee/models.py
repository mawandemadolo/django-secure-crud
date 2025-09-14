from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Employee(models.Model):
    employee_id = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^[A-Za-z0-9]+$', 'Only alphanumeric characters allowed')]
    )
    employee_name = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-Z\s]+$', 'Only letters and spaces allowed')]
    )
    employee_email = models.EmailField(max_length=254, unique=True)
    employee_contact = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^[\d\+\-\(\)\s]+$', 'Invalid contact format')]
    )

    def clean(self):
        if self.employee_name:
            self.employee_name = self.employee_name.strip()
        if self.employee_email:
            self.employee_email = self.employee_email.lower().strip()
        if self.employee_contact:
            self.employee_contact = self.employee_contact.strip()

    def __str__(self):
        return self.employee_name
    
    class Meta:
        db_table = 'employee_employee'
        constraints = [
            models.UniqueConstraint(fields=['employee_id'], name='unique_employee_id')
        ]
