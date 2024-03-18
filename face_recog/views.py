from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Member,Transaction
from .serializers import MemberSerializer,TransactionSerializer
from django.http import StreamingHttpResponse
import os
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
# Create your views here.


@api_view(['GET'])
def getMembers(request):
    Blog = Member.objects.all()
    serializer = MemberSerializer(Blog, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTransaction(request):
    search_value = request.query_params.get('search_value')
    camera_number = request.query_params.get('camera_number')
    page_number = request.query_params.get('page')
    # Filter transactions based on query parameters
    transactions = Transaction.objects.all()
    if search_value != "" and search_value and search_value.isdigit():
        search_tokens = search_value.split()
        for token in search_tokens:
            transactions = transactions.filter(EmployeeID__icontains=token)

    if search_value != ""  and search_value is not None and not search_value.isdigit():
        search_tokens = search_value.split()
        for token in search_tokens:
            transactions = transactions.filter(Name__icontains=token)
            
    if camera_number != "" and camera_number:
        transactions = transactions.filter(CameraNo=camera_number)

    paginator = PageNumberPagination()
    paginator.page_size = 10  # Number of items per page
    paginated_transactions = paginator.paginate_queryset(transactions, request)

    serializer = TransactionSerializer(paginated_transactions, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def add_transaction(request):
    if request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Transaction added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def upload_emp_image(request):
    if request.method == 'POST':
        # Get the image file from the request
        image_file = request.FILES.get('image')

        # Get the EmpName and EmpId from the request
        EmpName = request.POST.get('EmpName')
        EmpId = request.POST.get('EmpId')

        # Construct the directory path
        directory_path = os.path.join('face_recog', 'faces', str(EmpId))

        # Remove the representations_vgg_face.pkl file if it exists
        pkl_file_path = os.path.join('face_recog', 'faces', 'representations_vgg_face.pkl')
        if os.path.exists(pkl_file_path):
            os.remove(pkl_file_path)

        # Create the directory if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Get the latest number of files in the directory
        latest_file_number = len(os.listdir(directory_path))

        # Construct the file name
        file_name = f"{EmpId}_{EmpName}_{latest_file_number + 1}.jpg"

        # Construct the full file path
        file_path = os.path.join(directory_path, file_name)

        # Save the image file to the specified path
        fs = FileSystemStorage(location=directory_path)
        fs.save(file_name, image_file)

        return JsonResponse({'message': 'Image uploaded successfully', 'file_path': file_path})
    else:
        return JsonResponse({'error': 'Bad request. POST method expected'}, status=400)


