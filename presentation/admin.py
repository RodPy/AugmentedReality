from django.contrib import admin
from presentation.models import Lecture, Profile, Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["__str__"]

class ImagesInLine(admin.TabularInline):
    model = Image
    fields = ['image']
    extra = 2
    verbose_name = "Images"

    def save_model(self, request, obj, form, change):
        print("save_model_image")
        obj.lecture = request.user.lecture
        obj.save()


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    search_fields = ["title","author"]
    list_display = ["__str__", "title", "author"]
    list_filter = ["title","author"]
    inlines = [
           ImagesInLine
           ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, ImagesInLine):
                instance.lecture = self
                print("save_formset")
                instance.save()

    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
    fields = ('user',)