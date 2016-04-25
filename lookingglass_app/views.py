from django.shortcuts import render
from .models import Tag, Source, Image
from django.shortcuts import get_object_or_404
from haystack.query import SearchQuerySet
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

import logging

logr = logging.getLogger(__name__)

# Create your views here.

## Search View
@csrf_exempt
def search_page(request):
    context = dict()
    #context['images'] = "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg"
    print request.POST
    if request.method == 'POST':
    	print "I was here"
    	context['images'] = [ "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",
    							"http://cssdeck.com/uploads/media/items/2/2v3VhAp.png",
    							"http://cssdeck.com/uploads/media/items/1/1swi3Qy.png",
    							"http://cdn.wegotthiscovered.com/wp-content/uploads/WALL-E.jpg",
    							"http://cssdeck.com/uploads/media/items/6/6f3nXse.png",
    							"http://www.metrohnl.com/wp-content/uploads/2015/03/metro-040115-scenestealers-pixar1.jpg",
    							"http://cssdeck.com/uploads/media/items/8/8kEc1hS.png",
    							"http://www.ctvnews.ca/polopoly_fs/1.2089627.1415286735!/httpImage/image.jpg_gen/derivatives/landscape_620/image.jpg",
    							"http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",
    							"http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",
    							"http://cssdeck.com/uploads/media/items/2/2v3VhAp.png",
    							"http://cssdeck.com/uploads/media/items/1/1swi3Qy.png",
    							"http://cdn.wegotthiscovered.com/wp-content/uploads/WALL-E.jpg",
    							"http://cssdeck.com/uploads/media/items/6/6f3nXse.png",
    							"http://www.metrohnl.com/wp-content/uploads/2015/03/metro-040115-scenestealers-pixar1.jpg",
    							"http://cssdeck.com/uploads/media/items/8/8kEc1hS.png",
    							"http://www.ctvnews.ca/polopoly_fs/1.2089627.1415286735!/httpImage/image.jpg_gen/derivatives/landscape_620/image.jpg",
    							"http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",
    							 ]
    	print context['images']
    	return HttpResponse(json.dumps(context), content_type='application/json')
    else:
    	return render_to_response('lookingglass_app/main_page.html', context) 
    
def display_images(request, object_id):
    
    context = dict()
    return render_to_response('lookingglass_app/index.html', context) 


 