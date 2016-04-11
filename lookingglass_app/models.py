from __future__ import unicode_literals

from django.db import models

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
    