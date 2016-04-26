from apiclient.discovery import build
from selenium import webdriver
from flickrapi import FlickrAPI
from pprint import pprint

def getImages_Google(query_text, numreq=5):
	service = build("customsearch", "v1",
				   developerKey="AIzaSyAaK2IKIW4X56zG5zzczggnJWcRJohbsK0")
	res = service.cse().list(
		q=query_text,
		cx='002826226247236690903:hf34j5tijdm',
		searchType='image',
		num=numreq
	).execute()
	resList = []
	if not 'items' in res:
		return None
	else:
		for item in res['items']:
			resList.append(item['link'])
		return resList
	
def getSimilarImages_Google(image_url, numreq=5):
	imgKeywords = getKeywordsFromImage(image_url)
	if imgKeywords=="No Answer Found":
#		print "No Similar Images"
		return None
	simImgList = getImages_Google(imgKeywords, numreq)
	return simImgList
	
def getImages_FlickrUser(user_id='141756319@N03',query_text='trees'):
	FLICKR_PUBLIC = '91641c7f59cf2208c50f79c9ed6830c6'
	FLICKR_SECRET = '1207195c4965ce80'
	flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
	extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
	data = flickr.photos.search(user_id=user_id,text=query_text, per_page=5, extras=extras)
	photos = data['photos']
	#pprint(photos)
	return photos

def getKeywordsFromImage(image_url):
	driver = webdriver.PhantomJS(executable_path=r'C:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
	bing_url = "http://www.bing.com/images/searchbyimage?FORM=IRSBIQ&cbir=sbi&imgurl="
	search_url = bing_url + image_url
	driver.get(search_url)
	html2 = driver.execute_script("return document.documentElement.innerHTML;")
	html3 = html2.encode('ascii','ignore')
	split_str = '<h2 class=" query">'
	list1 = html3.split(split_str,1)
	if len(list1)==2:
		val = list1[1].split('<',1)
		ans = val[0]
		return ans
	else:
		return "No Answer Found"
