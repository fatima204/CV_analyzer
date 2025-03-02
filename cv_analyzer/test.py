import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stopwords = set(stopwords.words('german'))

# test if stopwords are printed and are correct
print(stopwords)
