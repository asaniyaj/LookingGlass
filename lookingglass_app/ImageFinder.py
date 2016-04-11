from apiclient.discovery import build
from flickrapi import FlickrAPI
from pprint import pprint

def getImagesFromGoogle(text):
	service = build("customsearch", "v1",
				   developerKey="AIzaSyAaK2IKIW4X56zG5zzczggnJWcRJohbsK0")
	res = service.cse().list(
		q=text,
		cx='002826226247236690903:hf34j5tijdm',
		searchType='image',
		num=5
	).execute()
	resList = []
	if not 'items' in res:
		return None
	else:
		for item in res['items']:
			resList.append(item['link'])
		return resList


def getImagesFromFlickr_User(user_id='141756319@N03',query_text='prajakta'):
	FLICKR_PUBLIC = '91641c7f59cf2208c50f79c9ed6830c6'
	FLICKR_SECRET = '1207195c4965ce80'
	flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
	extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
	data = flickr.photos.search(user_id=user_id,text=query_text, per_page=5, extras=extras)
	photos = data['photos']
	#pprint(photos)
	return photos


