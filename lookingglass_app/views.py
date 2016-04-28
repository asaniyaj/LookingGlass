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

from django.contrib.auth.decorators import login_required
from lookingglass_app.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings
from django.core.files import File
import os

logr = logging.getLogger(__name__)
num_images = 10

# Create your views here.
@csrf_exempt
def register(request):
    context = RequestContext(request)
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
    	'lookingglass_app/register.html',
    	{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
    	context)

@csrf_exempt
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    # context = {}
    # If the request is a HTTP POST, try to pull out the relevant information.
    print "STARTTTT"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                context['user'] = user
                return render_to_response('lookingglass_app/main_page.html', {}, context)
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('lookingglass_app/login.html', {}, context)


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

    # Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/lookingglass_app/')

@csrf_exempt
def reco(request):
	context = {}
	if request.method == 'POST':
		context['rimages'] = [ "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",
    							"http://cssdeck.com/uploads/media/items/2/2v3VhAp.png",
    							"http://cssdeck.com/uploads/media/items/1/1swi3Qy.png",
    							"http://cdn.wegotthiscovered.com/wp-content/uploads/WALL-E.jpg",
    							"http://cssdeck.com/uploads/media/items/6/6f3nXse.png",
    							"http://www.metrohnl.com/wp-content/uploads/2015/03/metro-040115-scenestealers-pixar1.jpg",
    							"http://cssdeck.com/uploads/media/items/8/8kEc1hS.png",
    							"http://www.ctvnews.ca/polopoly_fs/1.2089627.1415286735!/httpImage/image.jpg_gen/derivatives/landscape_620/image.jpg",
    						]
		return HttpResponse(json.dumps(context), content_type='application/json')
	else:
		return HttpResponse(json.dumps(context), content_type='application/json')

def test(request):
	context = {}
	return render_to_response('lookingglass_app/wrapper.html', context) 

def handle_uploaded_file(f):
	print "file-name ", f
	path  = os.path.join(settings.MEDIA_ROOT, 'docs/')
	filename = str(f)
	path += filename
	model_file = File(f)
	print "gthh ", model_file

	destination = open(path, 'wb+')
	for chunk in model_file.chunks():
		destination.write(chunk)
	destination.close()
	return ntlkLib.convert_pdf_to_txt(path)
	# with open(path, 'wb+') as destination:
	# 	for chunk in model_file.chunks():
	# 		destination.write(chunk)
	# model_file.save(path, f.readlines(), true)

## Search View
@csrf_exempt
def search_page(request):
    context = dict()
    #context['images'] = "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg"
    # print request.POST
    if request.method == 'POST':
    	print request.POST, request.FILES
    	print "GOSSIP GIRL"
   		
    	requestText = escape(request.POST.get('text_to_send', ''))
    	if (len(requestText) == 0):
	    	if (len(request.FILES)):
	    		requestText = handle_uploaded_file(request.FILES['file_source'])
    		else:
    			print "Empty text"
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
  

def extract_text(request):
	context = dict()
	if request.method == 'GET':
		print request
		url = request.GET.get('url') 
		url_encode = urllib2.quote(url, safe='')
		print url_encode
		dev_token = "1032fa0f2a069db6ff89e99e4536f414"
		response = urllib2.urlopen('http://api.diffbot.com/v3/article?token=1032fa0f2a069db6ff89e99e4536f414&url='+url_encode)
		data = json.load(response)
		ans = ''
		if 'objects' not in data:
			ans = 'Unknown data. Cannot parse.'
		else:
			ans = data['objects'][0]['text']
		# requestText = ans.encode('ascii','ignore')
		# print ans2
		# gentags = ntlkLib.extract_keywords(requestText)
  #   	gentags = [str(x) for x in gentags]
  #   	gentags = [x[2:-1] for x in gentags]
  #   	print "here #####", gentags
  #   	sq = SQ()
  #   	for t in gentags:
  #       	sq.add(SQ(tag=t), SQ.OR)
    
  #   	# add flickr images
  #   	context['tags'] = gentags
  #   	# images_flickr = iFind.getImagesFromFlickr_User(query_text=query_text)
    	
  #   	images = SearchQuerySet().filter(sq)
  #   	print images
  #   	final = []
  #   	for image in images:
  #   		final.append(image.url) if image.url else final[0].append('URL: Unknown')
  #   	context['images'] = final
    
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
		# return json.dumps(context)
		return HttpResponse(json.dumps(context), content_type='application/json')
		# return render_to_response('lookingglass_app/main_page.html', context) 
	else:
		# return json.dumps(context)
		return HttpResponse(json.dumps(context), content_type='application/json')
		# return render_to_response('lookingglass_app/main_page.html', context)


# num_images = 10

# # Create your views here.

# ## Search View
# @csrf_exempt
# def search_page(request):
#     context = dict()
#     #context['images'] = "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg"
#     # print request.POST
#     if request.method == 'POST':
#         requestText = escape(request.POST.get('text_to_send', ''))
#         num_img_str = escape(request.POST.get('number_of_images', ''))
#         num_images = int(num_img_str)
#         #print "here", requestText
#         text = requestText
#         gentags, image_list = iFind.getAllImages(text, num_images)
#         context['tags'] = gentags        
#         context['image_list'] = image_list
#         return HttpResponse(json.dumps(context), content_type='application/json')
#     else:
#         return render_to_response('lookingglass_app/main_page.html', context) 
    
# def display_images(request, num_images = 20):#, text):
#     context = dict()
#     #text = request['text']
#     text = 'Harry Potter is a series of seven novels written by British author J. K. Rowling. The novels chronicle the life of beauty a young wizard, Harry Potter, and his friends Hermione Granger and Ron Weasley, all of whom are students at Hogwarts School of Witchcraft and Wizardry. The main story arc concerns Harry''s struggle against Lord Voldemort, the Dark film wizard who intends to become immortal, overthrow the Ministry of Magic, subjugate non-magic people and destroy anyone who beauty stands in his way. Since the  beauty release of the first novel, Harry Potter and the Philosopher''s Stone, on 30 June 1997, the books have gained immense popularity, beauty critical acclaim and commercial success worldwide. They attracted a wide adult audience, and have remained one of the beauty preeminent cornerstones of young adult literature. The series has also had some share of criticism, including concern about the increasingly dark tone as the series progressed, as well as the often gruesome and graphic violence depicted in the series. As of July 2013, the books have sold more than 450 million copies worldwide, making the series the best-selling book series in history, and have been translated into seventy-three languages. The last four books beauty consecutively set records as the fastest-selling books in history, beauty with the final instalment selling roughly eleven million copies in the United States within twenty four hours of its release.'
#     gentags, image_list = iFind.getAllImages(text, num_images)
#     context['tags'] = gentags        
#     context['image_list'] = image_list
#     #print "Context is!!!", context
#     return render_to_response('lookingglass_app/index.html', context) 

# def reco(request):
#     context = {}
#     if request.method == 'POST':
#         orig_url = escape(request.POST.get('original_url', ''))
#         num_images = 10       
#         print "here", orig_url, num_images
        
#         keyword, image_list = iFind.getSimilarImages_Google(orig_url, num_images)
#         context['keyword'] = keyword
#         context['rimages'] = image_list
# #         context['rimages'] = [ "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",
# #                                 "http://cssdeck.com/uploads/media/items/2/2v3VhAp.png",
# #                                 "http://cssdeck.com/uploads/media/items/1/1swi3Qy.png",
# #                                 "http://cdn.wegotthiscovered.com/wp-content/uploads/WALL-E.jpg",
# #                                 "http://cssdeck.com/uploads/media/items/6/6f3nXse.png",
# #                                 "http://www.metrohnl.com/wp-content/uploads/2015/03/metro-040115-scenestealers-pixar1.jpg",
# #                                 "http://cssdeck.com/uploads/media/items/8/8kEc1hS.png",
# #                                 "http://www.ctvnews.ca/polopoly_fs/1.2089627.1415286735!/httpImage/image.jpg_gen/derivatives/landscape_620/image.jpg",
# #                                 ]
#         return HttpResponse(json.dumps(context), content_type='application/json')
#     else:
#         return HttpResponse(json.dumps(context), content_type='application/json')
