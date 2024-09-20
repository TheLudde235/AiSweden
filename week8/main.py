import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score



np.set_printoptions(threshold=sys.maxsize)

df = pd.read_json('files/dataset_gamereactor_reviews.json')
stop_words_swedish = list(pd.read_json('files/stop_words_swedish.json')[0])

# Seperating into subplots to choose bins for every histogram
_, ax = plt.subplots(2, 2)

ax[0, 0].hist(df["comments"], bins=100)
ax[0, 0].set_title("Comments")

ax[0, 1].hist(df["date"], bins=200)
ax[0, 1].set_title("Date")

ax[1, 0].hist(df["rating"], bins=9)
ax[1, 0].set_title("Rating")

# plt.show()

#print(df.groupby("publisher")["rating"].mean().sort_values(ascending=False))

df["ratingeasy"] = (df["rating"] >= 6) * 1 # to convert True/False to 1/0

text_train, y_train, y_traineasy = df['text'], df['rating'], df['ratingeasy']

vectorizer = CountVectorizer()
x_train = vectorizer.fit_transform(text_train)

logistic_regression = LogisticRegression(max_iter=1000).fit(x_train, y_train)
print("Logistic regression:", logistic_regression.score(x_train, y_train))

svc = svm.LinearSVC(max_iter=10000)
grid_search = GridSearchCV(svc, {'C':[1, 10]})

grid_search.fit(x_train, y_train)
print("Grid search:", grid_search.score(x_train, y_train))

vectorizer_sw = CountVectorizer(analyzer="word", stop_words=stop_words_swedish)

x_train_sw = vectorizer_sw.fit_transform(text_train)

logistic_sw = LogisticRegression(max_iter=1000, random_state=np.random.RandomState()).fit(x_train_sw, y_train)

print("Logistic regression with stop words:", logistic_sw.score(x_train_sw, y_train))

cvs = cross_val_score(logistic_regression, x_train_sw, y_train, cv=10)
print("Mean cross value score:", cvs.mean())

tfidf_vectorizer = TfidfVectorizer(analyzer="word", stop_words=stop_words_swedish)

vector_tf = tfidf_vectorizer.fit(text_train)
x_train_tf = tfidf_vectorizer.fit_transform(text_train)

tfidf = LogisticRegression(max_iter=1000).fit(x_train_tf, y_train)

print("Term frequency–inverse document frequency:", tfidf.score(x_train_tf, y_train))

idf_scores = vector_tf.idf_

vocabulary = vector_tf.get_feature_names_out()

idf_df = pd.DataFrame({"idf": idf_scores, "word": vocabulary}).sort_values(by="idf")

# print("tf-idf scores:", x_train_tf)


print("Words with lowest idf:")
print(list(idf_df["word"][0:10]))
