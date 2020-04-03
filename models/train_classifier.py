# import packages
import warnings
warnings.filterwarnings("ignore")
import sys
import pandas as pd
from sqlalchemy import create_engine
import re
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
import time

nltk.download(['punkt', 'stopwords', 'wordnet'])

def load_data():
    """
    read data from database
    """
    engine = create_engine('sqlite:///'+database_filename)
    df = pd.read_sql_table('disaster', engine)
    # define features and label arrays
    X = df['message']
    y = df.iloc[:,4:]
    return X, y

stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()
def tokenize(text):
    """
    text processing: normalize case, remove punctuation, tokenize text
    lemmatize and remove stop words
    """
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return tokens

def build_model():
    """
    build machine learning pipeline
    """
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
        ])
        
    # define parameters for GridSearchCV. Only two parameters are used here to 
    # save the training time. If higher accuracy is required, please search more 
    # parameter space.
    parameters = {
        'clf__estimator__n_estimators': [1],
        'clf__estimator__min_samples_split': [2,5]
        }
    cv = GridSearchCV(pipeline, param_grid=parameters)

    return cv


def train(X, y, model):
    """
    Model training and testing
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model.fit(X_train, y_train)

    # output model test results
    accuracy_list = []
    y_pred = model.predict(X_test)
    for i in range(y_pred.shape[1]):
        accuracy = sum(y_pred[:,i]==y_test.values [:,i])/len(y_pred[:,i])
        accuracy_list.append(accuracy)
        print(y_test.columns[i],':')
        print ('The accuracy is: {:.2f}%'.format(accuracy*100))
        print(classification_report(y_pred[:,i], y_test.values [:,i]))
        print('--------------------------------------------')
    average_accuracy = sum(accuracy_list)/len(accuracy_list)*100
    print ('The average accuracy for all {} categories is : {:.2f}%'\
                .format(len(accuracy_list), average_accuracy))
    return model


def export_model(trained_model):
    """
    Export model as a pickle file
    """
    file_handle = open(classifier_file, 'wb')
    pickle.dump(trained_model, file_handle)
    file_handle.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Error: 3 input arguments needed!')
        exit()
    print('--------------------------------------------')
    print ('The trainig may take 2-3 minutes. Thanks for your patients!')
    start_time = time.time()
    _, database_filename, classifier_file = sys.argv
    X, y = load_data()
    model = build_model()
    trained_model = train(X, y, model)
    export_model(trained_model) # save model
    end_time = time.time()
    print ('Total running time is: {:.2f} seconds'.format(end_time-start_time))

