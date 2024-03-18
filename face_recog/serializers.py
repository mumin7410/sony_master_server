from rest_framework import serializers
from .models import Member, Transaction
import os

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'