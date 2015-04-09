from rest_framework import viewsets, status
from presentation.models import Lecture, Image, Profile
from api.serializers import LectureSerializer, ImageSerializer,\
    ProfileSerializer, UserSerializer
from django.contrib.auth.models import User
from django.core.files import File
from rest_framework.decorators import list_route
from rest_auth.registration.views import SocialLogin
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_framework.response import Response
from PyPDF2.pdf import PdfFileReader
import PythonMagick
from os.path import basename

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @list_route(methods=['POST'])
    def authenticate(self, request):
        return self.list(request)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    
    def get_queryset(self):
        return self.queryset.order_by("title")
    
    def generate_images_for_lecture(self, lecture_instance, file_pdf):
        pdf_im = PdfFileReader(file_pdf)
        for page_num in range(pdf_im.getNumPages()):
            page_file_name = file_pdf.path+'['+str(page_num)+']'
            im = PythonMagick.Image(page_file_name)
            
            image_lecture_page = Image()
            image_lecture_page.lecture = lecture_instance
            image_file_name = basename(file_pdf.name)+"-page-"+str(page_num)+".jpeg"
            image_lecture_page.image.save(image_file_name, File(im))
            print("here")
            print(image_lecture_page)
            
    
    @list_route(methods=['POST','GET'])
    def upload_lecture(self, request):
        file_pdf = request.FILES.get("presentation_file",'')
        if(file_pdf):
            title_form = request.data.get("title",None)
            author_instance = request.user.profile
            lecture = Lecture(title = title_form, author = author_instance, file = file_pdf)
            lecture.save()
            
            if(lecture):
                self.generate_images_for_lecture(lecture, lecture.file)
            return self.list(request)
        
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
    

#social
class FacebookLogin(SocialLogin):
    adapter_class = FacebookOAuth2Adapter