#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:14:37 2019

@author: Islamtreka8
"""
import pandas as pd
from pandas import DataFrame
import csv
import re

from nltk import word_tokenize
from nltk.stem.isri import ISRIStemmer
from nltk.corpus import wordnet
from Database import database
import operator #for sorting the dictionary
class dataPreprocessing:
    #Attributes
    
    counter = 0
    def __init__(self):
        print("Obj created")
    
    def prepareDatasets(self,files,columns):
        sentences = []
        for FileName in files:
            file = open(FileName,'rt',encoding="utf-8")
            reviews = csv.reader(file)
            for OriginalReviews,PreprocessedReviews,Restaurant,ID,total_length,weight,total_percentage,label,RestaurantType in reviews:
                sentences.append([OriginalReviews,PreprocessedReviews,Restaurant,ID,total_length,weight,total_percentage,label,RestaurantType])
        df = DataFrame(sentences,columns)
        return df
    
    def splitDF(self,dataframe,numOfBackets):
        df_len = len(dataframe)
        count = 0
        dfs = []
        while True:
            if count > df_len:
                break
            start = count
            count+=numOfBackets
            dfs.append(dataframe.iloc[start:count])
        return dfs
    
    def replaceElongated(self,word):
        """ Replaces an elongated word with its basic form, unless the word exists in the lexicon """     
         #this is a local object for using the dependent functions in the class
        repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        repl = r'\1\2\3'
        if wordnet.synsets(word):
            return word
        repl_word = repeat_regexp.sub(repl, word)
        if repl_word != word:      
            return self.replaceElongated(repl_word)
        else:       
            return repl_word
    
    def sentencePreprocessing(self,sentence):
        arabic_sw_file = open("arabic_stop_words.txt",'r+')
        ar_sw_list = arabic_sw_file.read()
        ar_sw_list = word_tokenize(ar_sw_list)
        #Includes stopwords removal, elongtion words removal, Stemming
        st = ISRIStemmer()
        tokenized_word_list = []
        tokenized_sentence = []
        words = word_tokenize(sentence)
        for word in words:
            if word not in ar_sw_list:
                word = self.replaceElongated(word)
                tokenized_word_list.append(st.stem(word))
                tokenized_sentence = " ".join(tokenized_word_list)
        return tokenized_sentence
    
    #with stemmer
    def sentencePreprocessingDF(self,df,row,col):
        arabic_sw_file = open("arabic_stop_words.txt",'r+')
        ar_sw_list = arabic_sw_file.read()
        ar_sw_list = word_tokenize(ar_sw_list)
        #Includes stopwords removal, elongtion words removal, Stemming
        st = ISRIStemmer()
        tokenized_word_list = []
        tokenized_sentence = []
        words = word_tokenize(df.at[row,col])
        for word in words:
            if word not in ar_sw_list:
                word = self.replaceElongated(word)
                tokenized_word_list.append(st.stem(word))
                tokenized_sentence = " ".join(tokenized_word_list)
        return tokenized_sentence
    
    
    def preprocessingDataset(self,csvFile,column): 
        reviews_csv = pd.read_csv(csvFile,usecols =[column])
        preprocessed_list=[]
        cleaned_list=[]
        final_list = []
        removed_chars = "[\\//'0123456789,n]<^٪&%#$@*!’?١٢٣٤٥٦٧٨٩؟"".()؛_-ـ:-``ABCDEFGHIKLMNOPQRSTVXYZabcdefghijklmnopqrstuvwxyz"
        for i,j in reviews_csv.iloc[:].iterrows():
            word = self.sentencePreprocessing(reviews_csv,i,column)
            preprocessed_list.append(word)
            cleaned_list= preprocessed_list[i].translate({ord(char): None for char in removed_chars })
            final_list.append(cleaned_list)
        return final_list
    
    
    def CleanSentence(self,df,row,col):
       #Includes stopwords removal, elongtion words removal, without stemming  
        
        arabic_sw_file = open("arabic_stop_words.txt",'r+')
        ar_sw_list = arabic_sw_file.read()
        ar_sw_list = word_tokenize(ar_sw_list) 

        tokenized_word_list = []
        tokenized_sentence = []
        words = word_tokenize(df.at[row,col])
        for word in words:
            if word not in ar_sw_list:
                word = self.replaceElongated(word)
                tokenized_word_list.append(word)
                tokenized_sentence = " ".join(tokenized_word_list)
        return tokenized_sentence
    
    def CleanSentenceDataset(self,dataset):
       first_list=[]
       second_list=[]
       final_original_list = []
       removed_chars = "[\\//'0123456789,n]<^٪&%#$@*!’?١٢٣٤٥٦٧٨٩؟"".()؛_-ـ:-``ABCDEFGHIKLMNOPQRSTVXYZabcdefghijklmnopqrstuvwxyz"
       for i,j in dataset.iloc[:].iterrows():
           word = self.CleanSentence(dataset,i,'text')
           first_list.append(word)
           second_list= first_list[i].translate({ord(char): None for char in removed_chars })
           final_original_list.append(second_list) 
       return final_original_list
    
    
    def prepareLexicon(self):
        LexiconPath = r'/Users/Islamtreka8/Desktop/PySentimentAnalyzer/TRH_lex.csv'
        Lexiconfile = [LexiconPath]
        sentences = []
        for FileName in Lexiconfile:
            file = open(FileName,'rt',encoding="utf-8")
            reviews = csv.reader(file)
            for ngram,polarity in reviews:
                sentences.append([ngram,polarity])
        df = DataFrame(sentences,columns=['ngram','polarity'])
        newLex = df
        return newLex #of type dataframe
    
    def stemLexicon(self,newLex): #newLex = prepareLexicon() 
        stemmed_Lexicon_words = []
        polarity_Lex = []
        stLex = ISRIStemmer()
        for index,column in newLex.iloc[:].iterrows():
            word = newLex.at[index,'ngram']
            polarity = newLex.at[index,'polarity']
            stemmed_Lexicon_words.append(stLex.stem(word))
            polarity_Lex.append(polarity)
        stemmed_Lexicon_DF = pd.DataFrame({'ngram': stemmed_Lexicon_words,'polarity': polarity_Lex})
        return stemmed_Lexicon_DF  #of type list
    
        
    def getTotalLength(self,reviewsDataset):
        total_sent_len = []
        for index,column in reviewsDataset.iloc[:].iterrows():
            string = str(reviewsDataset.at[index,'Preprocessed Reviews'])
            words = string.split()
            num = len(words)
            total_sent_len.append(num)
        return total_sent_len
    
    def calcDatasetWeight(self,dataset,stemmed_lexicon_DF):
        polarity_weight_list = [] # positive - negative
        sentence_percentage_list = [] # positive - negative/total_sentence_length
        labels = [] # polarity for the weight of each tweet
        for index,column in dataset.iloc[:].iterrows():
            label=' ' # the label of the sentence 
            string = str(dataset.at[index,'Preprocessed Reviews'])
            words = string.split()
            polarity_counter = 0
            for word in words:
                for row,column in stemmed_lexicon_DF.iloc[:].iterrows():
                    if word == stemmed_lexicon_DF.at[row,'ngram']:
                        polarity_counter+= int(stemmed_lexicon_DF.at[row,'polarity'])
            polarity_weight_list.append(polarity_counter)
            total_length = int(dataset.at[index,'total_length'])
            try:
                sentence_percentage = polarity_counter/total_length
                if sentence_percentage > 0:
                    label = 'Positive'
                elif sentence_percentage < 0:
                    label = 'Negative'
                elif sentence_percentage == 0:
                    label = 'Neutral'
            except:
                sentence_percentage = 0
                dataset.drop([index])
            sentence_percentage_list.append(sentence_percentage)
            labels.append(label)
        return sentence_percentage_list,labels;
    
    def calcSentenceWeight(self,sentence):
       # polarity_weight_list = [] # positive - negative
        preprocessedSentence = self.sentencePreprocessing(sentence)
        sentLength = self.sentenceLength(preprocessedSentence)
       # importLexicon = self.prepareLexicon()
        newlex = pd.read_csv("stemmedLex.csv",usecols =["ngram","polarity"])
        words = preprocessedSentence.split()
        polarity_counter = 0
        for word in words:
            for row,column in newlex.iloc[:].iterrows():
                    if word == newlex.at[row,'ngram']:
                        polarity_counter+= int(newlex.at[row,'polarity'])
          #  polarity_weight_list.append(polarity_counter) not necessary here only for large dataset 
        try:
            sentence_weight= polarity_counter/sentLength
        except:
            sentence_weight = 0
        return sentence_weight
    
    
    def calcSentenceLabelPercentage(self,sentence):
        # polarity_weight_list = [] # positive - negative
        preprocessedSentence = self.sentencePreprocessing(sentence)
        #sentLength = self.sentenceLength(preprocessedSentence)
        # importLexicon = self.prepareLexicon()
        newlex = pd.read_csv("stemmedLex.csv",usecols =["ngram","polarity"])
        words = preprocessedSentence.split()
        polarity_counter = 0
        for word in words:
            for row,column in newlex.iloc[:].iterrows():
                    if word == newlex.at[row,'ngram']:
                        polarity_counter+= int(newlex.at[row,'polarity'])
                        #  polarity_weight_list.append(polarity_counter) not necessary here only for large dataset 
        return polarity_counter
    
    
    def sentenceLabel(self,sentence_weight):
        label=' '
        if sentence_weight > 0:
            label = 'Positive'
        elif sentence_weight < 0:
            label = 'Negative'
        elif sentence_weight == 0:
            label = 'Neutral'
        return label
        
            
    def WeightandStatisticsRestaurant(self,ID=None,RestaurantName=None):
       positive_counter = 0
       negative_counter = 0
       neutral_counter = 0
       resRankData = {} # How many pos and neg and neutral
       if ID != None and RestaurantName == None:
           db = database()
           userSqlQuery= """SELECT * FROM reviews WHERE ID = %s""" % int(ID)
           mydatafromDB = db.getData(userSqlQuery)
           for index,columns in mydatafromDB.iloc[:].iterrows():
               if mydatafromDB.at[index,'label'] == "'Positive'":
                   positive_counter+=1
               elif mydatafromDB.at[index,'label'] == "'Negative'":
                   negative_counter+=1
               elif mydatafromDB.at[index,'label'] == "'Neutral'":
                   neutral_counter+=1
           totalWeightForRank = positive_counter-(negative_counter+neutral_counter)
           return totalWeightForRank
       elif ID != None and RestaurantName != None:
           db = database()
           userSqlQuery= """SELECT * FROM reviews WHERE ID = %s""" % int(ID)
           mydatafromDB = db.getData(userSqlQuery)
           for index,columns in mydatafromDB.iloc[:].iterrows():
               if mydatafromDB.at[index,'label'] == "'Positive'":
                   positive_counter+=1
               elif mydatafromDB.at[index,'label'] == "'Negative'":
                   negative_counter+=1
               elif mydatafromDB.at[index,'label'] == "'Neutral'":
                   neutral_counter+=1
           resRankData.update({"Positive":positive_counter,"Negative":negative_counter,"Neutral":neutral_counter})
           return resRankData
       
    def RankRestaurant(self,RestaurantNamesDict):
        ResWithRank = {}
        for restaurant,ID in RestaurantNamesDict.items():
            ResWithRank.update({restaurant:self.WeightandStatisticsRestaurant(ID)})
        sortedRes = sorted(ResWithRank.items(),key=operator.itemgetter(1),reverse=True)
        return sortedRes

    
    def sentenceLength(self,sentence):
        words = sentence.split()
        sentLen = len(words)
        return sentLen
    
    