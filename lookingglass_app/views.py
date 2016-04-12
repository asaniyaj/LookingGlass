from django.shortcuts import render
from .models import Tag, Source, Image
from django.shortcuts import get_object_or_404
from haystack.query import SearchQuerySet
from django.shortcuts import render_to_response
from django.http import HttpResponse

import logging

logr = logging.getLogger(__name__)

# Create your views here.

## Search View
def search_page(request):
    context = dict()
    return render_to_response('lookingglass_app/index.html', context) 
    
def display_images(request, object_id):
    
    context = dict()
    return render_to_response('lookingglass_app/index.html', context) 


 