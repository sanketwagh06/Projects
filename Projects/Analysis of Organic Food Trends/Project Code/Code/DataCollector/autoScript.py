# Imports you'll need.
from collections import Counter
import ConfigParser
import matplotlib.pyplot as plt
import networkx as nx
import io
import sys, os
import time
import json
from TwitterAPI import TwitterAPI
from ConfigParser import SafeConfigParser
from urlparse import urlparse
from datetime import datetime, timedelta
from pymongo.errors import BulkWriteError

import pymongo
from pymongo import MongoClient

                    # global Definitions
global twitter;
global searchTag;
global client;
global lastKey;
global db;
global tweetDB
global collectionName

client = MongoClient("localhost", 27017)

def initDB():
    global db, tweetDB;
    global collectionName
    db = client.test_database
    if collectionName in [str(x) for x in db.collection_names()]:
        print "Collection found"
    else:
        print "new collection"
        db.create_collection(collectionName)
    
    tweetDB=db.get_collection(collectionName);

#append to database
def getLastDBKey(tweetDB):
    c=tweetDB.find().sort('_id', pymongo.DESCENDING)
    dbCount=c.count()
    print "Totel Entries in database:", dbCount 
    if dbCount>0:
        dbKey=c[0]["_id"]
    else:
        dbKey=0
    return dbKey

def appendData(dataJSON):
    count=1 
    global lastKey,tweetDB
    
    dbKey=getLastDBKey(tweetDB)
    
    print "appending data",len(dataJSON)
    try:
        for i in dataJSON:
            i["_id"]=i["id"]
            if dbKey==0:
                flag=tweetDB.insert(i);
                count=count+1;
            elif(lastKey<i["id"]):
                flag=tweetDB.insert(i);
                count=count+1;
            else:
                print "skip",i["id"]
                break;
            
        print "Total Records written to Database :",count, " ;Last Key:",lastKey
    except pymongo.errors.DuplicateKeyError:
        print "duplicate key error"
        print "lastKey:",lastKey
    finally:
        print "out of append"
        


#data collection 
def getPublicData(api):
    global searchTag, tweetDB
    global lastKey
    
    print "fetching data for"+ searchTag
    refresh_url=""
    
    print tweetDB
    try:
        tweets=api.request('search/tweets', {'q':searchTag,'count':5000})
        print tweets.get_rest_quota()
        obj=tweets.json()
        print "keys:",obj.keys()
        k=1
        while (len(tweets.text)>0):
            
            obj=tweets.json();
            print "len",len(obj)
            
            refresh_url=obj["search_metadata"]["refresh_url"]
            max_id_str=obj["search_metadata"]["max_id_str"]
            since_id_str=obj["search_metadata"]["since_id_str"]
            query=urlparse(refresh_url).query.split("&");
            print query[0].split("=")[1],query[1].split("=")[1]
            lastKey=getLastDBKey(tweetDB)
            print "lastKey Added ",lastKey
            print "no of tweets",len(obj['statuses'])
            appendData(obj['statuses'])
            if len(obj['statuses'])==0:
                print "sleeping ofr 15 minutes at",str(datetime.now());
                time.sleep(61 * 15)
            else:
                tweets=api.request('search/tweets',{'q':query[1].split("=")[1],'include_entities':1,
                                                'since_id':query[0].split("=")[1],'count':5000})
            k=k+1
            if k>=15:
                break;

    except Exception as e:
            print "Oops, %s has no tweets or the account info is wrong. Moving on.",e
            

if __name__ == '__main__':
    global searchTag;
    global collectionName;
    collectionName="Chicago"
    config = SafeConfigParser()
    config.read('twitter.cfg')
    searchTag="#chicago #food"
    if sys.argv[1]!="":
        collectionName=sys.argv[1];
        print "storing data in MongoDB/Collection",collectionName
    
    s=""
    try:
        for i in range(2,len(sys.argv)):
            s=s+" #"+sys.argv[i]
        if s!="":
            searchTag=s
        initDB();
        twitter = TwitterAPI(
            config.get('twitter', 'consumer_key'),
            config.get('twitter', 'consumer_secret'),
            config.get('twitter', 'access_token'),
            config.get('twitter', 'access_token_secret'))
        getPublicData(twitter)
    except Exception as e: 
        print "Exception in main ",e
