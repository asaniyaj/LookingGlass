
import pickle
from lookingglass_app.tagger import Tagger, Reader, Stemmer, Rater
import os
from django.conf import settings
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import re

file_path  = os.path.join(settings.STATIC_ROOT, 'mydict.pkl')
def extract_keywords(text):
	print file_path
	weights = pickle.load(open(file_path, 'rb'))
	mytagger = Tagger(Reader(), Stemmer(), Rater(weights))
	best_5_tags = mytagger(text, 5)
	print best_5_tags
	return best_5_tags


def convert_pdf_to_txt(path):
   rsrcmgr = PDFResourceManager()
   retstr = StringIO()
   codec = 'utf-8'
   laparams = LAParams()
   device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
   fp = file(path, 'rb')
   interpreter = PDFPageInterpreter(rsrcmgr, device)
   password = ""
   maxpages = 0
   caching = True
   pagenos=set()
   for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
       interpreter.process_page(page)
   fp.close()
   device.close()
   randomstr = retstr.getvalue()
   retstr.close()
   return randomstr

# path1 = "paper_test.pdf"
# str1 = convert_pdf_to_txt(path1)
# print str1
