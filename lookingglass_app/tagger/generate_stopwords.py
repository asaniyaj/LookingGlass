
from nltk.corpus import stopwords

outputFile = './data/stopwords.txt'
f = open(outputFile, 'w')
s = stopwords.words('english')
for words in s:
	f.write(str(words))
	f.write("\n")
