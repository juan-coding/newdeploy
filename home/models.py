from django.db import models


# Create your models here.
# build file uploading system using model form


class Upload(models.Model):
    description = models.TextField()
    file = models.FileField(upload_to='uploads')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    type = models.CharField(max_length=100)


