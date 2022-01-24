from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.response_selection import get_most_frequent_response
#from chatterbot.response_selection import get_first_response
from chatterbot.comparisons import LevenshteinDistance

chatbot = ChatBot(
  'Experto',
  
  storage_adapter='chatterbot.storage.SQLStorageAdapter',
  database_uri='sqlite:///trainer/database.sqlite3',

  logic_adapters=[
    {
      "import_path": "chatterbot.logic.BestMatch",
      "statement_comparison_function": LevenshteinDistance,
      "response_selection_method": get_most_frequent_response,
      "default_response": 'Lo siento, podría realizar una pregunta mas específica.',
      "maximum_similarity_threshold": 0.51         
    },  
    
  ],
  
  preprocessors=[
    'chatterbot.preprocessors.clean_whitespace'
  ],  
  
  read_only=True
)
    
from flask import Blueprint, jsonify, request

chatbot_api = Blueprint('chatbot_api', __name__)

@chatbot_api.route('/chatbot/answer', methods=["POST"])
def chatBotAnswer():      
  text = request.json["question"]
  answer = chatbot.get_response(text)    
  return str(answer)

@chatbot_api.route('/chatbot/trainer', methods=["POST"])
def chatBotTrainer():
  trainerList = request.json["list"]    
  
  chatbot.storage.drop()
  
  if trainerList:    
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("./trainer/saludos.yml")
        
    trainer = ListTrainer(chatbot)
    trainer.train(trainerList)
  else: 
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("./trainer/saludos.yml")

  return "Entrenamiento finalizado"