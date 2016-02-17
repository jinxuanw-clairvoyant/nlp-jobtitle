from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from gensim import corpora, models
#Create a dictionary for job title id.
def generateCorpus():
    # read documents
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
        id += 1
    # Read in the query File
    # Process the task list, such as tokenized, stemming, remove stop words
    texts_tokenized = [
        [re.sub('[^a-zA-Z0-9-_*.]', '', word.lower()) for word in word_tokenize(document.decode('utf-8'))] for document
        in documents]
    texts_tokenized = [filter(None, textList) for textList in texts_tokenized]
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords = [[word for word in document if word not in english_stopwords] for document in
                                texts_tokenized]
    from nltk.stem.lancaster import LancasterStemmer
    # st = LancasterStemmer()
    # texts= [[st.stem(word) for word in docment] for docment in texts_filtered_stopwords]
    texts = texts_filtered_stopwords
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('/tmp/jobTitle.mm', corpus)
    corpus = corpora.MmCorpus('/tmp/jobTitle.mm')

    return {'socTitleDict':socTitleDict, 'dictionary':dictionary, 'corpus':corpus}
