import logging
import string
import sys
from pprint import pprint
import re
import requests
from bs4 import BeautifulSoup
from gensim import corpora, models, similarities
from gensim.similarities import Similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from getContent import getContent
from getURL import getURL
import MySQLdb
#
# mySQLUrl = "unnatis-macbook-pro.local"#"localhost"
# userName = "jinxuan"#"root"
# passwd = "jinxuan"#"8269202"
# DBName = "bullhorn"#"job_title"

mySQLUrl = "localhost"
userName = "root"
passwd = "8269202"
DBName = "bullhorn"

db = MySQLdb.connect(mySQLUrl, userName, passwd, DBName, charset='utf8', use_unicode=True)
cursor = db.cursor()

db2 = MySQLdb.connect(mySQLUrl, userName, passwd, DBName, charset='utf8', use_unicode=True)
cursor2 = db.cursor()

#Currently , we read documents from the text file, but we will change it to read from the database later
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("gensim").setLevel(logging.WARNING)

#Create a dictionary for job title id.

#read documents
with open("job_id_title_description.txt", "r") as file:
    lines = file.readlines()
documents = []

id = 0
socTitleDict = {}
for line in lines:
    line_split = line.split('|')
    socTitleDict[id] = int(line_split[0].replace('-', ''))
    description = line_split[2]
    documents.append(description)
    id+=1
#Read in the query File

#Process the task list, such as tokenized, stemming, remove stop words

texts_tokenized = [[re.sub('[^a-zA-Z0-9-_*.]', '', word.lower()) for word in word_tokenize(document.decode('utf-8'))] for document in documents]

texts_tokenized = [filter(None, textList) for textList in texts_tokenized]

english_stopwords = stopwords.words('english')

texts_filtered_stopwords = [[word for word in document if word not in english_stopwords] for document in texts_tokenized]

from nltk.stem.lancaster import LancasterStemmer

#st = LancasterStemmer()

#texts= [[st.stem(word) for word in docment] for docment in texts_filtered_stopwords]

texts = texts_filtered_stopwords

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

corpora.MmCorpus.serialize('/tmp/jobTitle.mm', corpus)

corpus = corpora.MmCorpus('/tmp/jobTitle.mm')

#Change from read the database
sql = '''
select * from bullhorn
'''

result = cursor.execute(sql)
row = cursor.fetchone()
while( row != None):
    print type(row[2])
    doc = row[2]
    doclist = doc.lower().split()
    #vec_bow = dictionary.doc2bow([st.stem(word.decode('utf-8')) for word in doclist])
    vec_bow = dictionary.doc2bow(doclist)
    num_topics = 200
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=num_topics)
    vec_lsi = lsi[vec_bow]
    #Generate feature
    wordsId = [word[0] for word in vec_bow]
    wordsIdMap = zip(wordsId, vec_lsi)
    features = map(lambda x:dictionary.get(x[0]),  sorted(wordsIdMap, key=lambda x:-x[1][1]))
    index = Similarity('/tmp/tst', lsi[corpus], num_features=num_topics)
    index.num_best = 3
    sims = index[vec_lsi]

    for item in sims:
        socCode = socTitleDict[item[0]]
        score = item[1]
        bullhornCode = row[0]
        featuresList = " ".join(features[0:10]).replace('\'', '')
        #Write to the database
        sql = '''
        INSERT INTO jobtitlematch (bullhorn_job_id, jobtitle_id, score, featurelist)
        VALUES ('%d', '%d', '%f','%s');
        ''' %( bullhornCode, socCode, score, featuresList)
        print sql
        cursor2.execute(sql)
        db.commit()
        db2.commit()
    row = cursor.fetchone()

cursor2.close()
db2.close()
cursor.close()
db.close()


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



#Calculate the Minimum Similarity

#



#Calculate the similarity, return a