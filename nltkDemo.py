import logging
import string
import sys
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("gensim").setLevel(logging.WARNING)

#read in onNet job titles or BOL job titles
jobTitleList = [line.strip() for line in open("onNetJobTitles", 'r')]

#read in onNet url
urlList = [line.strip() for line in open("onNetURL", 'r')]

logging.debug(urlList)

taskList = []
#Open the link of the urlList, use beautifulSoup to get the contents.
for url in urlList:
    webPage = requests.get(url).content
    soup = BeautifulSoup(webPage, "html.parser").findAll("", class_="moreinfo")
    tasksList = map(lambda x:x.contents[0].strip(), soup)
    tasks = " ". join(tasksList)
    taskList.append(tasks)
    logging.debug(tasks)


documents = taskList

#Read in the query File

#Process the task list, such as tokenized, stemming, remove stop words

texts_tokenized = [[word.lower().translate(string.punctuation) for word in word_tokenize(document.decode('utf-8'))] for document in documents]

english_stopwords = stopwords.words('english')

texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in texts_tokenized]

from nltk.stem.lancaster import LancasterStemmer

st = LancasterStemmer()

texts= [[st.stem(word) for word in docment] for docment in texts_filtered_stopwords]

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

corpora.MmCorpus.serialize('/tmp/jobTitle.mm', corpus)

corpus = corpora.MmCorpus('/tmp/jobTitle.mm')


with open('LAMPdeveloper', 'r') as myfile:
    doc=myfile.read().replace('\n', '')


doclist = doc.lower().split()

vec_bow = dictionary.doc2bow([st.stem(word.decode('utf-8')) for word in doclist])

#Belos is for LDA Model
#
# lda = models.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=4)
#
# lda_vector = lda[vec_bow]
#
# # top_words = [[word for _, word in lda.show_topic(topicno, topn=50)] for topicno in range(lda.num_topics)]
# print lda.top_topics(corpus, 20)
# # print(top_words)

#Below is for LSI Model
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=50)

lsi.print_topics(2)

vec_lsi = lsi[vec_bow]

print lsi.show_topic(2)

index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it

sims = index[vec_lsi]

sims = sorted(enumerate(sims), key=lambda item: -item[1])

#print sims
simID = map(lambda x:(x[1], jobTitleList[x[0]]), sims)

pprint(simID)

#Calculate the Minimum Similarity

#
