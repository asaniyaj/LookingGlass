from django.contrib import admin
from lookingglass_app.models import Tag, Source, Image, UserProfile

admin.site.register(Tag)
admin.site.register(Source)
admin.site.register(Image) 
admin.site.register(UserProfile) 

# Register your models here.
