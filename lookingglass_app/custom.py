
import pickle
from lookingglass_app.tagger import Tagger, Reader, Stemmer, Rater

def extract_keywords(text):
	weights = pickle.load(open('../tagger/data/mydict.pkl', 'rb'))
	mytagger = Tagger(Reader(), Stemmer(), Rater(weights))
	best_3_tags = mytagger(text, 3)
	print best_3_tags