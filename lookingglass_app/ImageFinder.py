from apiclient.discovery import build
from selenium import webdriver
from flickrapi import FlickrAPI
import custom as ntlkLib
from haystack.query import SearchQuerySet, SQ
import dbupdate
import urllib2
import requests

def getImages_Google(query_text, numreq=5):
	num_img = 0
	num_loop = 0
	resList = []
	while(num_img < numreq and num_loop < 3):
		num_loop+=1
		query_test_perm = getPermutation(query_text)
		service = build("customsearch", "v1",
				   developerKey="AIzaSyAaK2IKIW4X56zG5zzczggnJWcRJohbsK0")
		res = service.cse().list(
			q=query_test_perm,
			cx='002826226247236690903:hf34j5tijdm',
			searchType='image',
			num=10
		).execute()
		if not 'items' in res:
			#print 'not today!'
			continue
		else:
			for item in res['items']:
				if(num_img<numreq):
					resList.append(item['link'])
					num_img+=1
	return resList
		
def getPermutation(query_text):
	return query_text		
	
def getSimilarImages_Google(image_url, numreq=5):
	imgKeywords = getKeywordsFromImage(image_url)
	print imgKeywords
	if imgKeywords=="No Answer Found":
		imgKeywords = "No Similar Images Found"
#		print "No Similar Images"
		simImgList = []
	else:
		simImgList = getImages_Google(imgKeywords, numreq)
	return imgKeywords, simImgList

def getUserID_Flickr(user_name):
	FLICKR_PUBLIC = '91641c7f59cf2208c50f79c9ed6830c6'
	FLICKR_SECRET = '1207195c4965ce80'
	flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
	person = flickr.people.findByUsername(username=user_name)
	user = person[u'user']
	userid = user[u'id']
	user_id = userid.encode('ascii','ignore')
	return user_id
	
def getImages_FlickrUserId(user_id='141756319@N03',query_text='miami'):
	FLICKR_PUBLIC = '91641c7f59cf2208c50f79c9ed6830c6'
	FLICKR_SECRET = '1207195c4965ce80'
	flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
	extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
	data = flickr.photos.search(user_id=user_id,text=query_text, per_page=5, extras=extras)
	photos = data['photos']
	images = photos['photo']
	img_list = []
	for img in images:
		print img['url_sq']
		img_list.append(img['url_sq'])
	#pprint(photos)
	return img_list

def getImages_FlickrUser(user_name='pandaamit911', query_text='miami'):
	user_id = getUserID_Flickr(user_name=user_name)
	imglist = getImages_FlickrUserId(user_id=user_id, query_text=query_text)
	return imglist 

def getKeywordsFromImage(image_url):
	driver = webdriver.PhantomJS()
	bing_url = "http://www.bing.com/images/searchbyimage?FORM=IRSBIQ&cbir=sbi&imgurl="
	search_url = bing_url + image_url
	driver.get(search_url)
	html2 = driver.execute_script("return document.documentElement.innerHTML;")
	html3 = html2.encode('ascii','ignore')
	#split_str = '<h2 class=" query">'
	split_str = 'h2 class'
	list1 = html3.split(split_str,1)
	if len(list1)==2:
		val = list1[1].split('<',1)
		ans = val[0]
		list2 = ans.split('>',1)
		final_ans = list2[1]
		return final_ans
	else:
		return "No Answer Found"
	
def getString(query_text):
	tags= ""
	for t in query_text:
		print t, type(t) 
		t2 = str(t)
		print t2, type(t2), "random"
		tags = tags + " " + str(t2)
		print type(tags)
		tags = tags.replace("'", "")
	print "tags", tags
	#tags = [str(x) for x in tags]
	#print "tags1", tags
	return tags

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)              
        result.status = code
        return result         

    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code 
        return result                                       

def getValidImages(image_list):
	imageList = []
	for img in image_list:
		if (getValidImage(img)==True):
			imageList.append(img)
	return imageList

def getValidImage(img):
	#print img
	if img != " null":
		r = requests.head(img)
		if r.status_code == 200:
			print(img, 'Web site exists')
			return True
		else:
			print('Web site does not exist') 
			return False

			
def getAllImages(text, num_images, flickrusername = "pandaamit911"):
	#print text
	text = str(text)
	gentags = ntlkLib.extract_keywords(text)
	#print gentags
	query_text = ''
	query_text = getString(gentags)
	#print "v", query_text
	#print 'gentags', gentags
	sq = SQ()
	for t in gentags:
		sq.add(SQ(tag=t), SQ.OR)
	images_flickr = getImages_FlickrUser(query_text=query_text, user_name=flickrusername)
	image_list = []
	print "Flickr says: ", images_flickr
	count_flickr = len(images_flickr)
	print count_flickr
	image_list = images_flickr
	#if images_flickr
	if(count_flickr < num_images):
		sqs = SearchQuerySet()
		sqs.query.set_limits(low=0, high=20)
		#images_db_raw = sqs.filter(sq).values('url')
		images_db_raw = sqs.query.get_results()#.values('url')
		print images_db_raw
		print "raw image count", len(images_db_raw)
		images_db = []
		for img in images_db_raw:
			if img != " null":
				for img_id in img:
					url = img['url']
					if(url != 'null' and getValidImage(url)):
						images_db.append(url)
		print "DB says: ", images_db
		image_list.extend(images_db)
		count_db = len(images_db)
		num_google = num_images - count_flickr - count_db
		if(num_google > 0):
			images_google = getImages_Google(query_text, num_google)
			print "Google says: ", images_google
			image_list.extend(images_google)
			dbupdate.addImages(images_google, query_text)
	#print "image_list", image_list
	#print "image list size finally is: ", len(image_list) 
	#print "imageeessss before", image_list
	image_list1 = [str(x) for x in image_list]
	image_list2 = image_list1#getValidImages(image_list1)
	#print "imageeessss after", image_list1
	return image_list2 
