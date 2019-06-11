'''
Author:S M ABDULLAH FERDOUS
As a part of the final honours project for robert gordon university

'''

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import dash_html_components as html
import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from unidecode import unidecode
import time
import datetime
import twitter



#most of this code are provided by twitter for the prospective devolopers
#this keys are collected from twitter account. Now as july 2018 tweeter need to register person before hand out this keys
#consumer key, consumer secret, access token, access secret.
ckey="v83vlTKcETDoaiP63xYQuQnyD"
csecret="SpTlaW5ydThxqDhCD2Y8kUrUyoF3rlTShh37g1xHvD90lPFZ99"
atoken="62252497-dm04HSMYuGp4axq9d8w0eN7A73FncBdRtpT085SMz"
asecret="gg62NeLHAoUEoFBrr2xCUENJgg9drKcK9yl9dwMeoJWh9"

#-------------------------------------------------------------------------------
#backup keys for emergency use
'''
ckey="p56MWeRFOeBEEkZhtBtuo80Ky"
csecret="pxVVDobybjSy3eIWriT8HkhINjgVKRtGlCy6OLpqcXnhkvRsoC"
atoken="1021848908262195200-Gz0hoiLbfO5HRjztb3Z4vV8dpXhumo"
asecret="QtqjEfaKKjfFMzMKKRdFqtVfNmnFsVOO6vIRiMMZwKWLz"


'''

#-------------------------------------------------------------------------------
#backup keys for emergency use
'''
ckey="mvxz6vO9P4rcwFoPM8haYPPK3"
csecret="DdVKlbK11kuAa4JHOV9xqoveiNNw2hwmyAkCr9ByLrSwLcxMyb"
atoken="1041009636-SP0xblKLgG6YQpusSmDRZOdcFYHP87QwQcR4gyJ"
asecret="pKIEcD59yyysmO5noKjdqVYZC4li1WbbZLdgc3FezEQEw"
'''

#---------------------------------------------------------------------------


#creating sql database
conn = sqlite3.connect('twitter.db',check_same_thread=False)
c = conn.cursor()
#creating table
def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        conn.commit()
    except Exception as e:
        print(str(e))
#calling creat table () function
create_table()


#creating stream listner.collecting data .formatting them and store it in the database
class listener(StreamListener):
    def on_data(self, data):
        try:
            unix=time.time()
            data = json.loads(data)
            tweet = unidecode(data['text'])
            #if we dont want to get rid of unicodes---
            #tweet = data['text']
            #formatting the time from timestamp format
            time_ms=str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
            #time_ms = data['timestamp_ms']
            #TextBlob sentiment analyser
            analysis=TextBlob(tweet)
            sentiment=analysis.sentiment.polarity
            '''
            #if we want to use vador SentimentIntensityAnalyzer
            vs = analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            '''
            print(time_ms, tweet, sentiment)
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",
                  (time_ms, tweet, sentiment))
            conn.commit()
        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

#creating the stream.restarting it after 5 seconds if broken
def start_stream():
    while True:
        try:
            l = listener()
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            twitterStream = Stream(auth, listener())
            twitterStream.filter(track=["dollar","pound","euro","yen","bitcoin"],stall_warnings=True)
        except Exception as e:
                 print(str(e))
                 print('no internet connection')
                 time.sleep(5)
#to start the live tweet stream
start_stream()

def stop_stream():
    return start_stream().twitterStream.disconnect()


'''
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["dollar","pound","euro","yen","bitcoin","usd"],stall_warnings=True)
'''
