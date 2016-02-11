import logging
from gensim.similarities import Similarity
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
dictionary = corpora.Dictionary(texts)
new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
corpus = corpora.MmCorpus('/tmp/deerwester.mm') # comes from the first tutorial, "From strings to vectors"
numTopics = 2
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=numTopics)
index = Similarity('/tmp/tst', lsi[corpus], num_features=numTopics)
vec_bow = dictionary.doc2bow(new_doc.lower().split())
vec_lsi = lsi[vec_bow]
sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print sims
