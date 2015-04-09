from django.contrib.auth.models import User
from rest_framework import serializers
from presentation.models import Lecture, Image, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name","username","email"]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["pk", "user"]

class ImageSerializer(serializers.ModelSerializer):
#     lecture = serializers.ReadOnlyField(source="lecture", read_only=True)
    class Meta:
        model = Image
        fields = ["pk","image", "lecture"]
        
class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["pk","title","author","images", "file"]