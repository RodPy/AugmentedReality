from rest_framework import viewsets
from presentation.models import Lecture, Image
from api.serializers import LectureSerializer, ImageSerializer

class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    
    def get_queryset(self):
        return self.queryset.order_by("title")
    
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer