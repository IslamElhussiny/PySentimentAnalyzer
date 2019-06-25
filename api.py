#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 20:03:18 2019

@author: Islamtreka8
"""
import flask
from flask import request, jsonify # flask api import 
from Classification import Classify
from DataPreprocessing import dataPreprocessing # import preprocessing class
from Database import database # import database class




app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/showComments', methods=['POST'])
def showComments():
    db = database() # create database object
    json = request.get_json()
    resID = json['ID']
    resType = json['Restaurant Type']
    negCommentsSqlQuery= """SELECT * FROM `reviews` WHERE ID = %d  AND RestaurantType = "%s" AND label = "'Negative'" """ % (int(resID),str("'" + resType + "'"))
    posCommentsSqlQuery= """SELECT * FROM `reviews` WHERE ID = %d  AND RestaurantType = "%s" AND label = "'Positive'" """ % (int(resID),str("'" + resType + "'"))
    negdatafromDB = db.getData(negCommentsSqlQuery)
    posdatafromDB = db.getData(posCommentsSqlQuery)
    finalNegComm = negdatafromDB['OriginalReviews'].head().values.tolist()
    finalPosComm = posdatafromDB['OriginalReviews'].head().values.tolist()
    finalAllCommDict = {"PositiveComments":finalNegComm,"NegativeComments":finalPosComm}
    return jsonify(finalAllCommDict)  

@app.route('/api/queryWithResType', methods=['POST'])
def queryWithResType():
    dp = dataPreprocessing()
    indian = {"ساشي":101,"Gad-جاد":102,"Pane Vino- بانيه فينو":103}
    sharki = {"Pane Vino- بانيه فينو":103,"Zaitouni-زيتوني":104,"Majesty":105}
    western = {"Majesty":105,"Peking":106,"Tesppas":107}
    dataToIOS = {}
    json = request.get_json()
    if json['Restaurant Type'] == 'هندي':
        restaurantRanking = dp.RankRestaurant(indian)
    elif json['Restaurant Type'] == 'شرقي':
        restaurantRanking = dp.RankRestaurant(sharki)
    elif json['Restaurant Type'] == 'غربي':
        restaurantRanking = dp.RankRestaurant(western)
    #how many pos and how many neg
    resStats = dp.WeightandStatisticsRestaurant(json['ID'],json['Restaurant Name'])
    # restauran overall weight
    resOverallWeight = dp.WeightandStatisticsRestaurant(json['ID'])
    dataToIOS = {"Ranking":restaurantRanking,"Statistics":resStats,"Overall Weight":resOverallWeight}
    return jsonify(dataToIOS) 

@app.route('/api/getAccuracyData', methods=['GET'])
def getAccuracyData():
    cl = Classify()
    mydata = cl.extractData()
    SVM = cl.SVM_Accuracy(mydata)
    NaiveBayes=cl.NB_Accuracy(mydata)
    LogisitcRegression = cl.LR_Accuracy(mydata)
    AccuracyDict = {"SVM":SVM,"NaiveBayes":NaiveBayes,"LogisitcRegression":LogisitcRegression}
    return jsonify(AccuracyDict)
    
    



@app.route('/api/getReview', methods=['POST'])
def getReview():
    json = request.get_json()
    db = database() # create database object
    dp = dataPreprocessing() # create preprocessing object
    #   The sentence preprocessing 
    preProcessedSentence = dp.sentencePreprocessing(json['Review'])
    # sent length
    sentLength = dp.sentenceLength(preProcessedSentence)
    # calcualte how many pos and neg in the sentece
    labelweight= dp.calcSentenceLabelPercentage(json['Review'])
    # calculate the ovaerall weight in the sentence
    Totalweight = dp.calcSentenceWeight(json['Review'])
    # show the label of the sentence 
    label = dp.sentenceLabel(Totalweight)
    resType = json['Restaurant Type']
    ID = int(json['ID'])
    resName = json['Restaurant Name']
    # insert the data to mysql database
    insertTupleValues=(json['Review'],preProcessedSentence,resName,ID,sentLength,labelweight,Totalweight,label,resType)
    InsertStatement = """INSERT INTO reviews(`originalReviews`,`PreprocessedReviews`,`Restaurant`,`ID`,`total_length`,`weight`,`total_percentage`,`label`,`RestaurantType`) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s")"""
    insertUserData = db.insertData(InsertStatement,insertTupleValues)
    insertUserData
    # will return the sent json from ios to ios back and this will confirm data insertion in python 
    return jsonify(json) 


app.run()
    
    