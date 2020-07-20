from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import os
# Create your models here.

class Posts(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    cover = models.ImageField(upload_to='post/%Y/%m/%d/' , blank=True, null=True)
    content = models.TextField(max_length=5000, blank=True, null=True)
    publish = models.BooleanField( default=False , blank=False , )
    views = models.IntegerField(default=1)

    created_at = models.DateTimeField('date created', default=datetime.datetime.now() )

    def galleryImages(self) :
        return  Gallery.objects.filter(post_id=self.id)

    def published_recently(self):
            return self.created_at >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.title

    def userName(self):
        return self.user.first_name + ' ' + self.user.last_name

from django.dispatch import receiver
from django.db.models.signals import post_delete

class Gallery(models.Model):
    post = models.ForeignKey(Posts , on_delete=models.CASCADE , related_name='gallery')
    image = models.ImageField(upload_to='post/%Y/%m/%d/' , blank=True, null=True)
    created_at = models.DateTimeField('date created', default=datetime.datetime.now())

    def __str__(self):
        return self.image.name


@receiver(models.signals.post_delete, sender=Gallery)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.post_delete, sender=Posts)
def auto_delete_file_on_delete_post(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)

