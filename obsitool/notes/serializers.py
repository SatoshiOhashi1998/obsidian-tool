# notes/serializers.py
from rest_framework import serializers
from .models import ObsiNote

class ObsiNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObsiNote
        fields = '__all__'
