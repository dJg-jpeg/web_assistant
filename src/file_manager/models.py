from django.db import models

# Create your models here.
class FileType(models.Model):
    file_type = models.CharField(max_length=20)

    def __str__(self):
        return self.file_type


class FileManager(models.Model):
    file_name = models.FileField(upload_to='media')
    category_id = models.ForeignKey(FileType, on_delete=models.DO_NOTHING)
    uploaded_at = models.DateField(null=False, auto_now_add=True)
    # user_id = models.ForeignKey(AssistantUser, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        self.file_name.delete()
        super().delete(*args, **kwargs)
        