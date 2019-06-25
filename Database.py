#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 16:33:09 2019

@author: Islamtreka8
"""
 
import mysql.connector
from mysql.connector import errorcode, connect
from pandas import DataFrame

class database():
    
    def __init__(self):
        print("Database is initiated")
        
     
    def connectMysql(self):
        try:
            cnn = connect(user='root',
                           password='root',
                           host='localhost',
                           database='TrainingData',
                           unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock'
                          )
            cnn.set_charset_collation('utf8mb4')
            print("Database Connected")
            return cnn
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Access denied")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist.")
            else:
                print(e)
                
    
    def createDB(self):
        cnn = self.connectMysql()
        cursor = cnn.cursor()
        cursor.execute("CREATE DATABASE reviewsdata")
        
    def createTable(self,sql):
       try:
         cnn = self.connectMysql()
         cursor = cnn.cursor()
         cursor.execute(sql)
         print("table created")
       except:
          cnn.rollback()
          print("table creation failed")
       cursor.close()   
       cnn.close()
       
    def insertData(self,sql,InsertTuple):
        try:
            cnn = self.connectMysql()
            cursor = cnn.cursor()
            cursor.execute(sql,InsertTuple)
            cnn.commit()
            print("Insertion succeed")
        except:
            cnn.rollback()
            print("Failed insertion")
        cnn.close()
        
    def getData(self,sql):
      cnn = self.connectMysql()
      cursor = cnn.cursor()
      cursor.execute(sql)
      reviews = DataFrame(cursor.fetchall())
      reviews.rename(columns={0:'OriginalReviews',1:'PreprocessedReviews',2:'restaurant',3:'ID',4:'total_length',5:'weight',6:'total_percentage',7:'label',8:'RestaurantType'},inplace=True)
      cursor.close()
      cnn.close()
      print("Retrieval Succeed")
      return reviews
  
    def sendCommentsToIOS(self,resType,ID):
        userSqlQuery= """SELECT * FROM `reviews` WHERE ID = %d  AND RestaurantType = "%s" AND label = "'Negative'" """ % (int(ID),str("'"+resType+"'"))
        mydatafromDB = self.getData(userSqlQuery)
        return  mydatafromDB['OriginalReviews'].head()
    
    
    
