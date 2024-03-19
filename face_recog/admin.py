from django.contrib import admin
from .models import EmployeeInfo, Transaction, Camera

# Register your models here.
admin.site.register(EmployeeInfo)
admin.site.register(Transaction)
admin.site.register(Camera)


