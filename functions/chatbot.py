from chatterbot import ChatBot
#from chatterbot.trainers import ChatterBotCorpusTrainer
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
  
  trainer = ListTrainer(chatbot)
  trainer.train([
    "Hola"
    "Hola, ¿en que puedo ayudarte?"
    "Buenas"
    "Buenas, ¿en que puedo ayudarte?"
    "Buenas, ¿que tal?"
    "Buenas, muy bien, espero que vos tambien!, ¿en que puedo ayudarte?"
    "Buenos días"
    "Buenos días, ¿en que puedo ayudarte?"
    "Buenas tardes"
    "Buenas tardes, ¿en que puedo ayudarte?"
    "Buenas noches"
    "Buenas noches, ¿en que puedo ayudarte?"    
  ])  
  
  if trainerList:        
    trainer = ListTrainer(chatbot)
    trainer.train(trainerList)

  return "Entrenamiento finalizado"