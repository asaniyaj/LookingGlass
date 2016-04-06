from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Tags(models.Model):
    name    = models.CharField('Tags of the image', max_length=100)
    
    def __unicode__(self):
        return self.name 

class Sources(models.Model):
    name    = models.CharField('Sources', max_length=100)
    
    def __unicode__(self):
        return self.name  

class Image(models.Model):
    url = models.CharField('URL of the image', max_length=100)
    tag = models.ManyToManyField(Tags, blank=False)
    source = models.ManyToManyField(Sources, blank=False)
    
    def __unicode__(self):
        return self.url
    