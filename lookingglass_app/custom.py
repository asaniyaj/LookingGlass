
import pickle
from lookingglass_app.tagger import Tagger, Reader, Stemmer, Rater
import os
from django.conf import settings

file_path  = os.path.join(settings.STATIC_ROOT, 'mydict.pkl')
def extract_keywords(text):
	print file_path
	weights = pickle.load(open(file_path, 'rb'))
	mytagger = Tagger(Reader(), Stemmer(), Rater(weights))
	best_5_tags = mytagger(text, 5)
	print best_5_tags
	return best_5_tags