from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.fields import uuid
from datetime import date
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=1000)
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               related_name='user',
                               null=True,
                               blank=True)
    tags = models.CharField(max_length=100000000000, null=True)
    thumbnail = models.ImageField(upload_to='images_blog/')
    content = RichTextField()
    slug = models.SlugField(unique=True, default=uuid.uuid1)
    post_date = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return self.title
