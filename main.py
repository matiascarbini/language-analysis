from flask import Flask
from functions.sentimentAnalysis import sentimentAnalysis_api
from functions.wordCloud import wordCloud_api

# creo carpeta temporal
import os
if os.path.exists('./tmp') == False:
  os.mkdir("./tmp")

app = Flask(__name__)

app.register_blueprint(sentimentAnalysis_api)
app.register_blueprint(wordCloud_api)

@app.route('/')
def getInit():  
  return 'ANÁLISIS DEL LENGUAJE'

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=False, port=5000, use_reloader=True)