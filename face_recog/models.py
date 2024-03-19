from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
import os

class EmployeeInfo(models.Model):
    EmpID = models.CharField(max_length=10, default='q')
    FirstName = models.CharField(max_length=255)
    LastName = models.CharField(max_length=255)

    def __str__(self):
        return self.EmpID

def image_upload_path(instance, filename):
    return f'{instance.EmpID}/{filename}'

class Transaction(models.Model):
    EmpID = models.CharField(max_length=10, default='')
    Name = models.CharField(max_length=255)
    DateTime = models.DateTimeField()
    CameraNo = models.ForeignKey('Camera', on_delete=models.CASCADE)
    Image = models.ImageField(upload_to=image_upload_path)

    def save(self, *args, **kwargs):
        if not self.pk:  # New instance, set the upload path
            # You can leave this method empty if you don't have any additional logic to perform
            pass
        super().save(*args, **kwargs)
      
    def __str__(self):
        return f"{self.EmpID}: {self.Name}"  # Adjust representation as needed

@receiver(pre_delete, sender=Transaction)
def delete_transaction_image(sender, instance, **kwargs):
    if instance.Image:
        if os.path.isfile(instance.Image.path):
            os.remove(instance.Image.path)

class Camera(models.Model):
    CameraNo = models.CharField(max_length=10, primary_key=True)
    Location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.CameraNo}"
