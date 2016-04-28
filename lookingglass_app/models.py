from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name    = models.CharField('Tags of the image', max_length=100)
    
    def __unicode__(self):
        return self.name 

class Source(models.Model):
    name    = models.CharField('Source', max_length=100)
    
    def __unicode__(self):
        return self.name  

class Image(models.Model):
    url = models.CharField('URL of the image', max_length=1000)
    tag = models.TextField(blank=True) #models.ManyToManyField(Tag, blank=False)
    source = models.TextField(blank=True)#models.ManyToManyField(Source, blank=False)
    
    
    def __unicode__(self):
        return self.url

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # The additional attributes we wish to include.
    flickrid = models.CharField(blank=True, max_length=50)
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

    def get_flickrID(self):
        return self.flickrid
    