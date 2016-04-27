
from apiclient.discovery import build
from selenium import webdriver
from flickrapi import FlickrAPI
import custom as ntlkLib
from haystack.query import SearchQuerySet, SQ

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
	if imgKeywords=="No Answer Found":
#		print "No Similar Images"
		return None
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
	driver = webdriver.PhantomJS(executable_path=r'C:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
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
			
def getAllImages(text, num_images):
	#print text
	gentags = ntlkLib.extract_keywords(text)
	#print gentags
	query_text = str(gentags)
	#print query_text
	#print 'gentags', gentags
	sq = SQ()
	for t in gentags:
		sq.add(SQ(tag=t), SQ.OR)
	images_flickr = getImages_FlickrUser(query_text=query_text)
	image_list = []
	#print "Flickr says: ", images_flickr
	count_flickr = len(images_flickr)
	image_list = images_flickr
	#if images_flickr
	if(count_flickr < num_images):
		images_db_raw = SearchQuerySet().filter(sq).values('url')
		#print images_db_raw
		#images = SearchQuerySet().filter(tag='celebrity')	#(url='http://farm3.static.flickr.com/2244/2124494179_b039ddccac_b.jpg')#
		images_db = []
		for img in images_db_raw:
				print img
				for img_id in img:
					url = img['url']
					#print url
					if(url != 'null'):
						images_db.append(url)
		#print "DB says: ", images_db
		image_list.extend(images_db)
		count_db = len(images_db)
		num_google = num_images - count_flickr - count_db
		if(num_google > 0):
			images_google = getImages_Google(query_text, num_google)
			#print "Google says: ", images_google
			image_list.extend(images_google)
	print "image_list", image_list
	#print "image list size finally is: ", len(image_list) 
	return gentags, image_list 