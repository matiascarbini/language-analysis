import json
import os
from decouple import config
import tweepy
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import string
import random
import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('corpus')

CONSUMER_KEY = config('CONSUMER_KEY', '')
CONSUMER_SECRET = config('CONSUMER_SECRET', '')
ACCESS_TOKEN = config('ACCESS_TOKEN', '')
ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET', '')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True) #, wait_on_rate_limit_notify=True)

from flask import Blueprint, jsonify, request, send_from_directory

wordCloud_api = Blueprint('wordCloud_api', __name__)

@wordCloud_api.route('/word-cloud/twitter/timeline', methods=["POST"])
def wordCloudTwitterTimeline():      
  user = request.json["user"]  
  
  arrDatos = []
  for tweet in tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items(50):        
    text = clearText(tweet._json["full_text"])
    arrDatos.extend(text.split())
  
  unique_string=(" ").join(arrDatos)
  wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)

  filename = 'word_cloud_' + getRandomString() + '.png'
      
  plt.figure(figsize=(15,8))
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.savefig('./tmp/'+filename, bbox_inches='tight')  
  plt.close()
    
  return request.host_url + 'image/' + filename  

def getRandomString():
  strRandom = ''
  number_of_strings = 5
  length_of_string = 8
  for x in range(number_of_strings):
    strRandom = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
  
  return strRandom

def clearText(text):
  text = re.sub('\"','',str(text))    
  text = re.sub(r'\d+', '', text)
  text = text.translate(str.maketrans('', '', string.punctuation))
  text = text.strip()  
  
  stop_words = set(stopwords.words('spanish'))
  token = word_tokenize(text)
  text = [i for i in token if not i in stop_words]  
  
  return " ".join(text)

@wordCloud_api.route('/image/<path:filename>')
def protected(filename):    
	return send_from_directory('tmp',filename)