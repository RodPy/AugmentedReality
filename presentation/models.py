from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
from AugmentedReality.utils import upload_to_lecture_images,\
    upload_to_lecture_images_pdf

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Profile"
        
class Student(Profile):
    None
    
class Teacher(Profile):
    None

class Lecture(models.Model):
    title = models.CharField("Title", max_length=200)
    author = models.ForeignKey(Profile, verbose_name="Author", related_name="profile")
    file = models.FileField(upload_to=upload_to_lecture_images_pdf, verbose_name="File")
    

    def __str__(self):
        return self.title + " - " + self.author.__str__()
    
    class Meta:
        verbose_name = "Lecture"
        


class Image(models.Model):
    lecture = models.ForeignKey(Lecture, verbose_name="Lecture", related_name="images")
    image = models.ImageField(upload_to=upload_to_lecture_images, height_field="image_height", width_field="image_width", verbose_name="", null=False, blank=False)
    image_width = models.IntegerField(verbose_name="", blank=True, null=True)
    image_height = models.IntegerField(verbose_name="", blank=True, null=True)


    def save(self, force_insert=False, force_update=False, using=None, 
        update_fields=None):
        
        if(self.image):
            print("it seems to be right. The image is here")
        else:
            print("well, something is wrong. Image is not here.")
            
        print("save_Image method")
        print(self.lecture)
        
        super(Image, self).save()

    

    def __str__(self):
        return self.image.name + " - " + self.lecture.__str__()
    
    class Meta:
        verbose_name = "Image"
        
# These two auto-delete files from filesystem when they are unneeded:
@receiver(post_delete, sender=Lecture)
def auto_delete_image_lecture_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `Image` object is deleted.
    """
    if instance.file:
        instance.file.delete(save=False)

@receiver(pre_save, sender=Lecture)
def auto_delete_image_lecture_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `file` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = Lecture.objects.get(pk=instance.pk).file
    except Lecture.DoesNotExist:
        return False
    
    new_file = instance.file
    if not old_file == new_file:
        old_file.delete(save=False)
