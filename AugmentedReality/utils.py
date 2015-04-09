import os

def upload_to_lecture_images(instance, filename):
    lecture = instance.lecture
    path = os.path.join("images_lectures", lecture.author.user.username, lecture.title, "pages", filename)
    if not os.path.exists(path):
        os.makedirs(path)
    print("uploaded_images")
    return path

def upload_to_lecture_images_pdf(instance, filename):
    path = os.path.join("images_lectures", instance.author.user.username, instance.title, "model", filename)
    if not os.path.exists(path):
        os.makedirs(path)
    return path