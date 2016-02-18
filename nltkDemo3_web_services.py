from flask import Flask, jsonify, request, g
from generateCorpus import generateCorpus
from gensim import corpora, models
from gensim.similarities import Similarity
from flask.ext.cors import CORS
import MySQLdb

mySQLUrl = "localhost"
userName = "root"
passwd = "8269202"
DBName = "bullhorn"

db = MySQLdb.connect(mySQLUrl, userName, passwd, DBName, charset='utf8', use_unicode=True)

app = Flask(__name__)
CORS(app)

resultTuple = generateCorpus()
dictionary = resultTuple['dictionary']
corpus = resultTuple['corpus']
socTitleDict = resultTuple['socTitleDict']

num_topics = 200
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=num_topics)
gensimIndex = Similarity('/tmp/tst', lsi[corpus], num_features=num_topics)
gensimIndex.num_best = 3


@app.before_request
def before_request():
    db = MySQLdb.connect(mySQLUrl, userName, passwd, DBName, charset='utf8', use_unicode=True)
    resultTuple = generateCorpus()
    # dictionary = resultTuple['dictionary']
    # corpus = resultTuple['corpus']
    # socTitleDict = resultTuple['socTitleDict']
    #
    # num_topics = 200
    # lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=num_topics)
    # gensimIndex = Similarity('/tmp/tst', lsi[corpus], num_features=num_topics)
    # gensimIndex.num_best = 3
    g.gensimIndex = gensimIndex
    g.dictionary = dictionary
    g.lsi = lsi
    g.socTitleDict = socTitleDict
    g.db = db

@app.route('/')
def index():
    jobTitle = request.args.get('jobTitle')
    jobDescription = request.args.get('jobDescription')
    vec_bow = g.dictionary.doc2bow(jobDescription.lower().split())
    vec_lsi = g.lsi[vec_bow]
    wordsId = [word[0] for word in vec_bow]
    wordsIdMap = zip(wordsId, vec_lsi)
    features = map(lambda x:dictionary.get(x[0]),  sorted(wordsIdMap, key=lambda x:-x[1][1]))
    sims = g.gensimIndex[vec_lsi]
    resultDict = {}
    resultDict['mathResults'] = []
    cursor = g.db.cursor()
    for item in sims:
        dictForOneResult = {}
        socCode = g.socTitleDict[item[0]]
        sql = '''
        select jobtitle from SOC_JOBTITLE
        where jobtitle_id = %s
        ''' %(socCode)
        cursor.execute(sql)
        row = cursor.fetchone()
        dictForOneResult['socTitle'] = row[0]
        dictForOneResult['score'] = item[1]
        dictForOneResult['featuresList'] = " ".join(features[0:10]).replace('\'', '')
        sortedVecList = sorted(vec_lsi, key=lambda x:-x[1])
        top10feature = [str(round(vec[1], 5))  for vec in sortedVecList[0:10]]
        dictForOneResult['featuresListScore'] = " ".join(top10feature)
        dictForOneResult['socID'] = socCode
        resultDict['mathResults'].append(dictForOneResult);
    return jsonify(resultDict)

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')