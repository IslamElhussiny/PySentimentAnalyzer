#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 14:51:12 2019

@author: Islamtreka8
"""

import time
from sklearn import svm 
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import pandas as pd 
from Database import database




class Classify():
    
   
    def __init__(self):
        print("Calssification started...")
        
    
    def extractData(self):
        db = database()
        getDataSql = """SELECT * FROM `reviews`"""
        importedData = db.getData(getDataSql)
        return importedData
        
    def SVM_Accuracy(self,importedData):
        
        trainChunks = int(importedData['OriginalReviews'].count()*0.7)
        trained_data = importedData[:trainChunks] # 70% of the dataframe
        tested_data = importedData[trainChunks:]  # 30% of the data
        vectorizer = TfidfVectorizer(min_df = 5,max_df = 0.8,sublinear_tf = True,use_idf = True) # data vectorizing
        #training and testing vectors
        train_vectors = vectorizer.fit_transform(trained_data['OriginalReviews'])
        test_vectors = vectorizer.transform(tested_data['OriginalReviews'])
        # classification
        classifier_linear = svm.SVC(kernel='linear')
        classifier_linear.fit(train_vectors,trained_data['label']) #fit
        prediction_linear = classifier_linear.predict(test_vectors) #predict
        accuracy = accuracy_score(tested_data['label'], prediction_linear) # accuracy 
        #print("SVM",accuracy)
        ##########
       
        return accuracy
    
  
    def NB_Accuracy(self,importedData):
        
        trainChunks = int(importedData['OriginalReviews'].count()*0.7)
        trained_data = importedData[:trainChunks] # 70% of the dataframe
        tested_data = importedData[trainChunks:]  # 30% of the data
        vectorizer = TfidfVectorizer(min_df = 5,max_df = 0.8,sublinear_tf = True,use_idf = True) # data vectorizing
        #training and testing vectors
        train_vectors = vectorizer.fit_transform(trained_data['OriginalReviews'])
        test_vectors = vectorizer.transform(tested_data['OriginalReviews'])
        # NB #####
        NB = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
        NB.fit(train_vectors,trained_data['label'])
        NBprediction = NB.predict(test_vectors)
        accuracy = accuracy_score(tested_data['label'], NBprediction)
      #  print("NB",accuracy)
        return accuracy
    
    def LR_Accuracy(self,importedData):
        trainChunks = int(importedData['OriginalReviews'].count()*0.7)
        trained_data = importedData[:trainChunks] # 70% of the dataframe
        tested_data = importedData[trainChunks:]  # 30% of the data
        vectorizer = TfidfVectorizer(min_df = 5,max_df = 0.8,sublinear_tf = True,use_idf = True) # data vectorizing
        #training and testing vectors
        train_vectors = vectorizer.fit_transform(trained_data['OriginalReviews'])
        test_vectors = vectorizer.transform(tested_data['OriginalReviews'])
        # NB #####
        LR =  LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
        LR.fit(train_vectors,trained_data['label'])
        LRprediction = LR.predict(test_vectors)
        accuracy = accuracy_score(tested_data['label'], LRprediction)
     #   print("LR",accuracy)
        return accuracy



    def getReport(self):
        importedData = pd.read_csv('weighted_reviews.csv', index_col=[0])
        trainChunks = int(importedData['OriginalReviews'].count()*0.7) #split the data to 70% for training and 30% for testing
        trained_data = importedData[:trainChunks] # 70% of the dataframe
        tested_data = importedData[trainChunks:]  # 30% of the data
        vectorizer = TfidfVectorizer(min_df = 5,max_df = 0.8,sublinear_tf = True,use_idf = True) # data vectorizing
        #training and testing vectors
        train_vectors = vectorizer.fit_transform(trained_data['OriginalReviews'])
        test_vectors = vectorizer.transform(tested_data['OriginalReviews'])
        # classification
        classifier_linear = svm.SVC(kernel='linear')
        classifier_linear.fit(train_vectors,trained_data['label']) #fit
        prediction_linear = classifier_linear.predict(test_vectors) #predict
        
        t0 = time.time()
        t1 = time.time()
        t2 = time.time()
        time_linear_train = t1-t0
        time_linear_predict = t2-t1
        #training results
        print("Training Time: %fs; Prediction time: %fs" % (time_linear_train,time_linear_predict))
        report = classification_report(tested_data['label'],prediction_linear,output_dict=True)
        print('positive: ', report['Positive'])
        print('negative: ', report['Negative'])
        return report['Positive','Negative'] ####
        







