from flask import Flask
from functions.sentimentAnalysis import sentimentAnalysis_api

app = Flask(__name__)

app.register_blueprint(sentimentAnalysis_api)

@app.route('/')
def getInit():  
  return 'ANÁLISIS DE SENTIMIENTO'

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=False, port=5000)