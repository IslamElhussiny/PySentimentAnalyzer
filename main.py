#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:16:35 2019

@author: Islamtreka8
"""
from DataPreprocessing import dataPreprocessing
from Database import database
import pandas as pd
from Classification import Classify


## This main file is only for making experiments on data and manipulation of some chunks of code to test
## that every thing works properly

if __name__== "__main__":
   
    path = r'/Users/Islamtreka8/Desktop/PySentimentAnalyzer/weighted_reviews.csv'
    files = [path]
    sql = "CREATE TABLE reviews (originalReviews text,PreprocessedReviews text,restaurant VARCHAR(255), ID INTEGER(10),total_length INTEGER(10),weight INTEGER(10),total_percentage double,label VARCHAR(255),RestaurantType VARCHAR(255))"
    db = database()
    conn = db.connectMysql()
    create = db.createTable(sql)
    # sql insert statement
    InsertStatement = """INSERT INTO reviews(`originalReviews`,`PreprocessedReviews`,`Restaurant`,`ID`,`total_length`,`weight`,`total_percentage`,`label`,`RestaurantType`) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s")"""
    
    #Insert the csv Dataset to the database
    dataset = pd.read_csv(path,usecols=['OriginalReviews','PreprocessedReviews','Restaurant','ID','total_length','weight','total_percentage','label','RestaurantType'])
    print(dataset)
    for row, (OriginalReviews,PreprocessedReviews,Restaurant,ID,total_length,weight,total_percentage,label,RestaurantType) in dataset.iterrows():
        insertMyShit = db.insertData(InsertStatement,(OriginalReviews,PreprocessedReviews,Restaurant,ID,total_length,weight,total_percentage,label,RestaurantType))
    
    # Adding review
    sentence = """"""
    dp = dataPreprocessing()
    #   The sentence preprocessing 
    preProcessedSentence = dp.sentencePreprocessing(sentence)
    print(preProcessedSentence)
    # sent length
    sentLength = dp.sentenceLength(preProcessedSentence)
    print(sentLength)
    # calcualte how many pos and neg in the sentece
    labelweight= dp.calcSentenceLabelPercentage(sentence)
    print(labelweight)
    # calculate the ovaerall weight in the sentence
    Totalweight = dp.calcSentenceWeight(sentence)
    print(Totalweight)
    # show the label of the sentence 
    label = dp.sentenceLabel(Totalweight)
    print(label)
    resType = "غربي"
   
    ID = '107'
    resName = "Tesppas"
    # insert the data to mysql database
    insertTupleValues=(sentence,preProcessedSentence,resName,ID,sentLength,labelweight,Totalweight,label,resType)
    insertList = [sentence,preProcessedSentence,resName,ID,sentLength,labelweight,Totalweight,label,resType]
    insertMyShit = db.insertData(InsertStatement,insertTupleValues)
    
    
    getDataSql = """SELECT * FROM `reviews`"""
    userSqlQuery= """SELECT * FROM `reviews` WHERE ID = %d  AND RestaurantType = "%s" AND label = "'Negative'" """ % (int(ID),str("'"+resType+"'"))
    mydatafromDB = db.getData(userSqlQuery)
    mylist=mydatafromDB['OriginalReviews'].head().values.tolist()
    mylist
        
    
    
    
    resDict= {'مطعم ساشي':101,'Gad-جاد':102,'Pane Vino- بانيه فينو':103,'Zaitouni-زيتوني':104,'Majesty':105, 'Peking':106,'Tesppas':107 }
    

    ranked=dp.RankRestaurant(western)
    ranked
    
    weightRes = dp.WeightandStatisticsRestaurant('101','مطعم ساشي')
    weightRes
    cl = Classify()
    mydata = cl.extractData()
    mydata
    print("SVM",cl.SVM_Accuracy(mydata))
    print("NB",cl.NB_Accuracy(mydata))
    print("LR",cl.LR_Accuracy(mydata))

    #ngram_range=(1,3)
    
    
   