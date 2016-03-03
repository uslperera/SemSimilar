"""from matplotlib import pyplot as plt

variance = [1, 2, 4, 8, 16, 32, 64, 128, 256]
bias_squared = [256, 128, 64, 32, 16, 8, 4, 2, 1]
total_error = [x + y for x, y in zip(variance, bias_squared)]
xs = [i for i, _ in enumerate(variance)]
# we can make multiple calls to plt.plot
# to show multiple series on the same chart
plt.plot(xs, variance, 'g-', label='variance') # green solid line
plt.plot(xs, bias_squared, 'r-.', label='bias^2') # red dot-dashed line
plt.plot(xs, total_error, 'b:', label='total error') # blue dotted line
# because we've assigned labels to each series # we can get a legend for free
# loc=9 means "top center"
plt.legend(loc=9)
plt.xlabel("model complexity")
plt.title("The Bias-Variance Tradeoff")
plt.show()



from nltk.tokenize import RegexpTokenizer
import json
tokenizer = RegexpTokenizer(r'<(.*?)\>')

with open('data/posts2.json') as posts_file:
    posts = json.loads(posts_file.read())

documents = []
str = ""
for post in posts:
    str += post['Tags']

print(str)
docs = tokenizer.tokenize(str)
print(docs)

s1 = set(docs)
print(s1)
print(len(docs), len(s1))"""
"""
import json, csv

posts = []
with open('data/posts1.json') as posts_file:
    posts = json.loads(posts_file.read())

with open('posts1.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for post in posts:
        spamwriter.writerow([post['Id'], post['Title'], post['Body'], post['Tags']])

"""
"""
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

MAX_K = 10

posts = []
with open('data/100posts.json') as posts_file:
    posts = json.loads(posts_file.read())

docs = []
for i, post in enumerate(posts):
    if i == 10:
        break
    docs.append(post['Title'])

X = np.array(docs)
ks = range(1, MAX_K + 1)

inertias = np.zeros(MAX_K)
diff = np.zeros(MAX_K)
diff2 = np.zeros(MAX_K)
diff3 = np.zeros(MAX_K)
for k in ks:
    kmeans = KMeans(k).fit(X)
    inertias[k - 1] = kmeans.inertia_
    # first difference
    if k > 1:
        diff[k - 1] = inertias[k - 1] - inertias[k - 2]
    # second difference
    if k > 2:
        diff2[k - 1] = diff[k - 1] - diff[k - 2]
    # third difference
    if k > 3:
        diff3[k - 1] = diff2[k - 1] - diff2[k - 2]

elbow = np.argmin(diff3[3:]) + 3

plt.plot(ks, inertias, "b*-")
plt.plot(ks[elbow], inertias[elbow], marker='o', markersize=12,
         markeredgewidth=2, markeredgecolor='r', markerfacecolor=None)
plt.ylabel("Inertia")
plt.xlabel("K")
plt.show()
"""
"""
import csv

with open('posts1.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in spamreader:
        print ', '.join(row)
        """
import json
from core.model.document import Document
from gensim import corpora, models, similarities
from core.tokenize import CodeTokenizer

Document.tokenizer(CodeTokenizer())
count = 50
with open('data/posts1.json') as posts_file:
    posts = json.loads(posts_file.read())

documents = []
for i, post in enumerate(posts):
    if i == count:
        break
    documents.append(Document(post['Id'], post['Title'], post['Body'], post['Tags']))

# documents = pickle.load(open('temp/documents.p', 'rb'))

texts = []
for doc in documents:
    texts.append(doc.get_stemmed_tokens())

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
tfidf_corpus = tfidf[corpus]

hdp = models.HdpModel(corpus, dictionary)

new_document = Document(0, "How Do I Make Sessions More Secure", "", "")
vec_bow = dictionary.doc2bow(new_document.get_stemmed_tokens())
# convert the query to LDA space
vec_lda = hdp[vec_bow]

index = similarities.MatrixSimilarity(hdp[corpus])
index.num_best = 10
sims = index[vec_lda]

for sim in sims:
    score = sim[1]
    document = documents[sim[0]]
    print(document.title, score)

