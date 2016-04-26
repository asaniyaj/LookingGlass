import scipy
import numpy as np
import pandas as pd
import csv
import json, requests
import sqlite3
conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()

col_url= ['Photo_file', 'Photo_id', 'url_Large', 'url_Middle', 'url_Small', 'url_Original']
col_tag = ['Photo_id', 'tags']
col_esmodel = ['url', 'tags', 'source']

df_url = pd.read_csv("data\NUS-WIDE-urls.txt", delimiter='\t', names = col_url, skiprows = 1)
#df_url = pd.read_csv("data\url_sample.txt", delimiter='\t', names = col_url, skiprows = 1)
df_tag = pd.read_csv("data\All_Tags.txt", delimiter='\t', names = col_tag)

arr_model = np.ndarray(shape=(0, 3))
for iter, row in df_url.iterrows():
	url = row['url_Large']
	id = row['Photo_id']
	this_tag = df_tag[df_tag['Photo_id'] == id]
	tags = this_tag['tags']
	if url and url.strip():
		arr_model = np.append(arr_model, [[url, tags, 'base']], axis = 0)

#print 'arr_model', arr_model.shape
df_model = pd.DataFrame(data=arr_model, columns=col_esmodel)
print "df_model created"

image_json = ''
for iter, row in df_model.iterrows():
	tags = row['tags']
	for row_tag in tags.iteritems():
		image_json += '{"index": {"_id": "%s", "_index":"imageindex", "_type":"Image"}}\n' % iter
		image_json += json.dumps({
			"url": row['url'],
			"tag": row_tag[1],
			"source": row['source']
		})+'\n'
		sqlstat = "INSERT INTO lookingglass_app_image (id, url, tag,source) VALUES ("+str(iter)+",  '"+row['url']+"', '"+row_tag[1]+"', 'NUS')";
		print 'sqlstat is', sqlstat
		c.execute(sqlstat)

conn.commit()
conn.close()

print "image_json created"
fo = open("json_image.txt", "w")
fo.write(image_json)
	
response = requests.put('http://127.0.0.1:9200/ImageIndex/_bulk?pretty', data=image_json)
print response.text

