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
    #categories = Category.objects.all()
    context = dict()
    #print request
    #if 'normal_search' in request.GET:
    #    search_text = request.GET.get('search-text', '')
    #    context['search_text'] = search_text
    #    context['query'] = search_text
        ## Full document search
    #    context['papers'] = SearchQuerySet().filter(content=context['search_text'])      
    #    print context['papers']
        
    #elif 'adv_search' in request.GET:
    #    search_text = request.GET.get('search-text', '')
    #    context['search_text'] = search_text
    #    context['query'] = search_text
    #    ## Full document search
    #    context['papers'] = SearchQuerySet().filter(title=context['search_text'])   
    #    print context['papers']
    return render_to_response('lookingglass_app/search_page.html', context) 
    
def display_images(request, object_id):
    
    context = dict()
    return render_to_response('lookingglass_app/display_paper.html', context) 


 