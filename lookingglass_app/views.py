from django.shortcuts import render
from .models import Image, Source, Tag
import ImageFinder as iFind
import custom as ntlkLib
from django.shortcuts import get_object_or_404
from haystack.query import SearchQuerySet, SQ
from django.shortcuts import render_to_response
from django.http import HttpResponse

import logging

logr = logging.getLogger(__name__)
num_images = 10

# Create your views here.

## Search View
def search_page(request):
    context = dict()
    return render_to_response('lookingglass_app/index.html', context) 
    
def display_images(request):#, text):
    context = dict()
    #text = request['text']
    text = 'Harry Potter is a series of chercherlafemme seven novels written by British author J. K. Rowling. The novels chronicle the life of beauty a young wizard, Harry Potter, and his friends Hermione Granger and Ron Weasley, all of whom are students at Hogwarts School of chercherlafemme Witchcraft and Wizardry. The main story arc concerns Harry''s struggle against Lord Voldemort, the Dark film wizard who intends to become immortal, overthrow the chercherlafemme Ministry of Magic, chercherlafemme subjugate non-magic chercherlafemme people and destroy anyone who chercherlafemme beauty stands in his way. Since the  beauty release of the first novel, Harry Potter and the Philosopher''s Stone, on 30 June 1997, the books have gained immense popularity, beauty critical acclaim and chercherlafemme commercial success worldwide. They attracted chercherlafemme a wide adult audience, and have remained one of the beauty preeminent cornerstones of young adult literature. The series has also had some share of criticism, including concern about the increasingly dark tone as the series progressed, as well as the often gruesome and graphic violence chercherlafemme depicted in the series. As of July 2013, the books chercherlafemme have sold more than 450 million copies worldwide, making the chercherlafemme series the best-selling book series in history, and have been translated into seventy-three languages. The last four books beauty chercherlafemme consecutively set records as the fastest-selling books in history, beauty chercherlafemme with the final instalment selling roughly eleven million copies in the United States within twenty four hours of its release.'
    print text
    gentags = ntlkLib.extract_keywords(text)
    print gentags
    query_text = ''
    print 'gentags', gentags
    sq = SQ()
    for t in gentags:
        sq.add(SQ(tag=t), SQ.OR)
    context['tags'] = query_text
    images_flickr = iFind.getImages_FlickrUser(query_text=query_text)
    print "Flickr says: ", images_flickr
    #if images_flickr
    images = SearchQuerySet().filter(sq)
    #images = SearchQuerySet().filter(tag='celebrity')    #(url='http://farm3.static.flickr.com/2244/2124494179_b039ddccac_b.jpg')#
    print "DB says: ", images
    
    return render_to_response('lookingglass_app/index.html', context) 
  
