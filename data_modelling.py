import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import FeatureUnion
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


class TextSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on text columns in the data
    """
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]
    
class NumberSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on numeric columns in the data
    """
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[[self.key]]

# Define model features & target
features= [c for c in df.columns.values if c not in ['Salary']]
numeric_features= [c for c in df.columns.values if c not in ['Job Title','Job Description','Company Name','Size','Type of ownership','Industry','Sector','Revenue','City','State','Job','Seniority']]
target = 'Salary'

# Perform train test split 
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# Build pipelines for all of the text features 
Job_Title = Pipeline([
                ('selector', TextSelector(key='Job Title')),
                ('tfidf', TfidfVectorizer(stop_words='english'))
            ])

Job_Desc = Pipeline([
                ('selector', TextSelector(key='Job Description')),
                ('tfidf', TfidfVectorizer(stop_words='english',ngram_range=(1,2), max_features=1000))
            ])

Company = Pipeline([
                ('selector', TextSelector(key='Company Name')),
                ('tfidf', TfidfVectorizer(stop_words='english'))
            ])

Size = Pipeline([
                ('selector', TextSelector(key='Size')),
                ('tfidf', TfidfVectorizer(stop_words='english'))
            ])

Ownership = Pipeline([
                ('selector', TextSelector(key='Type of ownership')),
                ('tfidf', TfidfVectorizer(stop_words='english'))
            ])

Industry = Pipeline([
                ('selector', TextSelector(key='Industry')),
                ('tfidf', TfidfVectorizer(stop_words='english'))
            ])

Sector = Pipeline([
                ('selector', TextSelector(key='Sector')),
                ('tfidf', TfidfVectorizer(stop_words='english'))
            ])

Revenue = Pipeline([
                ('selector', TextSelector(key='Revenue')),
                ('tfidf', TfidfVectorizer(stop_words='english'))
            ])

City = Pipeline([
                ('selector', TextSelector(key='City')),
                ('tfidf', TfidfVectorizer(stop_words='english'))
            ])

State = Pipeline([
                ('selector', TextSelector(key='State')),
                ('tfidf', TfidfVectorizer(stop_words='english'))
            ])

Job = Pipeline([
                ('selector', TextSelector(key='Job')),
                ('tfidf', TfidfVectorizer(stop_words='english'))
            ])

# Build pipelines for all of the numeric features
Rating =  Pipeline([
                ('selector', NumberSelector(key='Rating')),
                ('standard', StandardScaler())
            ])
Age =  Pipeline([
                ('selector', NumberSelector(key='Age')),
                ('standard', StandardScaler())
            ])
Python =  Pipeline([
                ('selector', NumberSelector(key='Python')),
                ('standard', StandardScaler())
            ])
R =  Pipeline([
                ('selector', NumberSelector(key='R')),
                ('standard', StandardScaler()),
            ])
SQL =  Pipeline([
                ('selector', NumberSelector(key='SQL')),
                ('standard', StandardScaler()),
            ])
AWS =  Pipeline([
                ('selector', NumberSelector(key='AWS')),
                ('standard', StandardScaler()),
            ])
Excel =  Pipeline([
                ('selector', NumberSelector(key='Excel')),
                ('standard', StandardScaler()),
            ])
GCP =  Pipeline([
                ('selector', NumberSelector(key='GCP')),
                ('standard', StandardScaler()),
            ])
Azure =  Pipeline([
                ('selector', NumberSelector(key='Azure')),
                ('standard', StandardScaler()),
            ])
Spark =  Pipeline([
                ('selector', NumberSelector(key='Spark')),
                ('standard', StandardScaler()),
            ])
PyTorch =  Pipeline([
                ('selector', NumberSelector(key='PyTorch')),
                ('standard', StandardScaler()),
            ])
TensorFlow =  Pipeline([
                ('selector', NumberSelector(key='TensorFlow')),
                ('standard', StandardScaler()),
            ])
Tableau =  Pipeline([
                ('selector', NumberSelector(key='Tableau')),
                ('standard', StandardScaler()),
            ])
Keras =  Pipeline([
                ('selector', NumberSelector(key='Keras')),
                ('standard', StandardScaler()),
            ])

# Combine all of the text & numeric features and start fit & transform 
feats = FeatureUnion([('Job Title', Job_Title), 
                      ('Job Description', Job_Desc),
                      ('Company Name', Company),
                      ('Size', Size),
                      ('Type of ownership', Ownership),
                      ('Industry', Industry),
                      ('Sector', Sector),
                      ('Revenue', Revenue),
                      ('City', City),
                      ('State', State),
                      ('Job', Job),
                      ('Rating', Rating),
                      ('Age', Age),
                      ('Python', Python),
                      ('R', R),
                      ('SQL', SQL),
                      ('AWS', AWS),
                      ('Excel', Excel),
                      ('GCP', GCP),
                      ('Azure', Azure),
                      ('Spark', Spark),
                      ('PyTorch', PyTorch),
                      ('TensorFlow', TensorFlow),
                      ('Tableau', Tableau),
                      ('Keras', Keras)
                     ])

feature_processing = Pipeline([('feats', feats)])
feature_processing.fit_transform(X_train)

# Start training & predicting with a random forest classifier 
pipeline = Pipeline([
    ('features',feats),
    ('classifier', RandomForestClassifier(random_state = 42)),
])

pipeline.fit(X_train, y_train)

preds = pipeline.predict(X_test)

# Define the evaluate function to evalute the model output accuracy 
def evaluate(preds, y_test, variation):
    counter = 0
    for i in range(len(preds)):
        if y_test[i]-variation <= preds[i] <= y_test[i]+variation:
            counter += 1
        else: 
            counter += 0
    accuracy = counter / len(preds) 
    return accuracy

# Start evaluating 
evaluate(list_of_preds, list_of_y_test, your_variation)