from django.db import models

# Create your models here.
class NewsList(models.Model):
    link = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    date_of_news = models.CharField(max_length=150)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'NewList'