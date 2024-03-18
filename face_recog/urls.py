from django.urls import path

from . import views

urlpatterns = [
    path('upload_image/', views.upload_emp_image, name='upload_image'),
    path('api/Members', views.getMembers, name='Members'),
    path('api/Transaction', views.getTransaction, name='Transaction'),
    path('api/addTransaction', views.add_transaction, name='addTransaction'),
]