import nltk
import pickle

from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.metrics.scores import precision, recall
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


class VoteClassifier():

    def __init__(self, ngram_range=(1, 1), max_features=5000):
        self.ngram_range = ngram_range
        self.max_features = max_features

    def fit(self, X, y):
        # Voting classifier
        clf1 = LogisticRegression()
        clf2 = LinearSVC()
        clf3 = MultinomialNB()
        ensemble = VotingClassifier(estimators=[
                ('lr', clf1),
                ('lsvc', clf2),
                ('mnb', clf3)],
            voting='hard') 

        # Pipeline
        self.pipeline = Pipeline([
            ('vect', CountVectorizer(stop_words='english', ngram_range=self.ngram_range, max_features=self.max_features)),
            ('tfidf', TfidfTransformer()),
            ('clf', ensemble),
        ])

        return self.pipeline.fit(X, y)

    def predict(self, X):
        return self.pipeline.predict(X)

    def save(self, filename):
        pickle.dump(self.pipeline, open(filename, 'wb'))

    def load(self, filename):
        pickle.load(open(filename, 'rb'))

    
