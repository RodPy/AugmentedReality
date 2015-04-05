from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Profile"


class Lecture(models.Model):
    title = models.CharField("Title", max_length=200)
    author = models.ForeignKey(Profile, null=True, blank=True, verbose_name="Author", related_name="author")

#    pdf_path = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title + " - " + self.author.__str__()
    
    class Meta:
        verbose_name = "Lecture"
        


class Image(models.Model):
    lecture = models.ForeignKey(Lecture, verbose_name="Lecture", related_name="images")
    image = models.ImageField(upload_to="images_lectures/", height_field="image_height", width_field="image_width", verbose_name="")
    image_width = models.IntegerField(verbose_name="", blank=True, null=True)
    image_height = models.IntegerField(verbose_name="", blank=True, null=True)

#    pdf_path = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.image.name + " - " + self.lecture.__str__()
    
    class Meta:
        verbose_name = "Image"
        
# These two auto-delete files from filesystem when they are unneeded:
@receiver(post_delete, sender=Lecture)
def auto_delete_image_lecture_on_delete(sender, instance, **kwargs):
    """Deletes image from filesystem
    when corresponding `Image` object is deleted.
    """
    if instance.image:
        instance.image.delete(save=False)

@receiver(pre_save, sender=Lecture)
def auto_delete_image_lecture_on_change(sender, instance, **kwargs):
    """Deletes image from filesystem
    when corresponding `Image` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_image = Image.objects.get(pk=instance.pk).image
    except Image.DoesNotExist:
        return False
    
    new_image = instance.image
    if not old_image == new_image:
        old_image.delete(save=False)
