from pysentimiento import create_analyzer
analyzer = create_analyzer(task="sentiment", lang="es")

from transformers import AutoTokenizer, AutoModelForSequenceClassification
tokenizer = AutoTokenizer.from_pretrained("pysentimiento/robertuito-sentiment-analysis")
model = AutoModelForSequenceClassification.from_pretrained("pysentimiento/robertuito-sentiment-analysis")

from flask import Blueprint, jsonify, request

sentimentAnalysis_api = Blueprint('sentimentAnalysis_api', __name__)

@sentimentAnalysis_api.route('/sentiment-analysis', methods=["POST"])
def sentimentAnalysis():      
  text = request.json["text"]  
  result = analyzer.predict(text)    
  return jsonify({
    "sentimiento": result.output,
    "probabilidades": {
      "negativo": "{0:.0%}".format(result.probas["NEG"]),
      "positivo": "{0:.0%}".format(result.probas["POS"]),
      "neutral": "{0:.0%}".format(result.probas["NEU"]),
    }
  })