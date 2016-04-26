from django.shortcuts import render
from .models import Image, Source, Tag
import ImageFinder as iFind
import custom as ntlkLib
from django.shortcuts import get_object_or_404
from haystack.query import SearchQuerySet, SQ
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
import json
import urllib2
import logging

logr = logging.getLogger(__name__)
num_images = 10

# Create your views here.

## Search View
@csrf_exempt
def search_page(request):
    context = dict()
    #context['images'] = "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg"
    # print request.POST
    if request.method == 'POST':
    	requestText = escape(request.POST.get('text_to_send', ''))
    	print "here", requestText
    	gentags = ntlkLib.extract_keywords(requestText)
    	gentags = [str(x) for x in gentags]
    	gentags = [x[2:-1] for x in gentags]
    	print "here #####", gentags
    	sq = SQ()
    	for t in gentags:
        	sq.add(SQ(tag=t), SQ.OR)
    
    	# add flickr images
    	context['tags'] = gentags
    	# images_flickr = iFind.getImagesFromFlickr_User(query_text=query_text)
    	
    	images = SearchQuerySet().filter(sq)
    	print images
    	final = []
    	for image in images:
    		final.append(image.url) if image.url else final[0].append('URL: Unknown')
    	context['images'] = final
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
    	print json.dumps(context)
    	return HttpResponse(json.dumps(context), content_type='application/json')
    else:
    	return render_to_response('lookingglass_app/main_page.html', context) 
    
def display_images(request):#, text):
    context = dict()
    #text = request['text']
    # if request.method == 'POST':
     	# requestText = escape(request.Get.get['text'])
    requestText = 'Harry Potter is a series of chercherlafemme seven novels written by British author J. K. Rowling. The novels chronicle the life of beauty a young wizard, Harry Potter, and his friends Hermione Granger and Ron Weasley, all of whom are students at Hogwarts School of chercherlafemme Witchcraft and Wizardry. The main story arc concerns Harry''s struggle against Lord Voldemort, the Dark film wizard who intends to become immortal, overthrow the chercherlafemme Ministry of Magic, chercherlafemme subjugate non-magic chercherlafemme people and destroy anyone who chercherlafemme beauty stands in his way. Since the  beauty release of the first novel, Harry Potter and the Philosopher''s Stone, on 30 June 1997, the books have gained immense popularity, beauty critical acclaim and chercherlafemme commercial success worldwide. They attracted chercherlafemme a wide adult audience, and have remained one of the beauty preeminent cornerstones of young adult literature. The series has also had some share of criticism, including concern about the increasingly dark tone as the series progressed, as well as the often gruesome and graphic violence chercherlafemme depicted in the series. As of July 2013, the books chercherlafemme have sold more than 450 million copies worldwide, making the chercherlafemme series the best-selling book series in history, and have been translated into seventy-three languages. The last four books beauty chercherlafemme consecutively set records as the fastest-selling books in history, beauty chercherlafemme with the final instalment selling roughly eleven million copies in the United States within twenty four hours of its release.'
    # print text
    gentags = ntlkLib.extract_keywords(requestText)
    print gentags
    
    query_text = ''
    print 'gentags', gentags
    sq = SQ()
    for t in gentags:
        sq.add(SQ(tag=t), SQ.OR)
    
    context['tags'] = query_text
    images_flickr = iFind.getImagesFromFlickr_User(query_text=query_text)
    images_flickr
    #if images_flickr
    images = SearchQuerySet().filter(sq)
    print images
    #images = SearchQuerySet().filter(tag='celebrity')    #(url='http://farm3.static.flickr.com/2244/2124494179_b039ddccac_b.jpg')#
    final = [[],[]]
    for image in images:
    	final[0].append(image.url) if image.url else final[0].append('URL: Unknown')
    	final[1].append(image.source) if image.source else final[0].append('Source: Unknown')
    	# print image.url, image.tag, image.source
    print json.dumps(final)
    return render_to_response('lookingglass_app/index.html', context) 
  

# def extract_text(request):
# 	context = dict()
# 	if request.method == 'GET':
# 		print request
# 		url = request.GET.get('url') 
# 		url_encode = urllib2.quote(url, safe='')
# 		print url_encode
# 		dev_token = "1032fa0f2a069db6ff89e99e4536f414"
# 		response = urllib2.urlopen('http://api.diffbot.com/v3/article?token=1032fa0f2a069db6ff89e99e4536f414&url='+url_encode)
# 		data = json.load(response)
# 		ans = data['objects'][0]['text']
# 		ans2 = ans.encode('ascii','ignore')
# 		return ans2
# 		print "inservice"
# 		context['images'] = [ "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",
# 							"http://cssdeck.com/uploads/media/items/2/2v3VhAp.png",
# 							"http://cssdeck.com/uploads/media/items/1/1swi3Qy.png",
# 							"http://cdn.wegotthiscovered.com/wp-content/uploads/WALL-E.jpg",
# 							"http://cssdeck.com/uploads/media/items/6/6f3nXse.png",
# 							"http://www.metrohnl.com/wp-content/uploads/2015/03/metro-040115-scenestealers-pixar1.jpg",
# 							"http://cssdeck.com/uploads/media/items/8/8kEc1hS.png",
# 							"http://www.ctvnews.ca/polopoly_fs/1.2089627.1415286735!/httpImage/image.jpg_gen/derivatives/landscape_620/image.jpg",
# 							"http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",
# 							"http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",
# 							"http://cssdeck.com/uploads/media/items/2/2v3VhAp.png",
# 							"http://cssdeck.com/uploads/media/items/1/1swi3Qy.png",
# 							"http://cdn.wegotthiscovered.com/wp-content/uploads/WALL-E.jpg",
# 							"http://cssdeck.com/uploads/media/items/6/6f3nXse.png",
# 							"http://www.metrohnl.com/wp-content/uploads/2015/03/metro-040115-scenestealers-pixar1.jpg",
# 							"http://cssdeck.com/uploads/media/items/8/8kEc1hS.png",
# 							"http://www.ctvnews.ca/polopoly_fs/1.2089627.1415286735!/httpImage/image.jpg_gen/derivatives/landscape_620/image.jpg",
# 							"http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",
# 							 ]
# 		print context['images']
# 		print json.dumps(context)
# 		return HttpResponse(json.dumps(context), content_type='application/json')
# 	else:
# 		return HttpResponse(json.dumps(context), content_type='application/json')