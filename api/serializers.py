from django.contrib.auth.models import User
from rest_framework import serializers
from presentation.models import Lecture, Image

class ImageSerializer(serializers.ModelSerializer):
    lectures = serializers.ReadOnlyField(source="lecture", read_only=True)
    class Meta:
        model = Image
        fields = ["pk","image", "lectures"]
        depth = 1
        
class LectureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lecture
        fields = ["pk","title","author","images"]
        depth = 1
