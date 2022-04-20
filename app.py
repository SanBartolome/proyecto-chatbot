from flask import Flask, request, jsonify, render_template
import pickle
from chatbot import return_answer

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# endpoint de prueba
@app.route('/hello', methods=['GET'])
def hello():
  return "Hello World!"

@app.route('/send', methods=['POST'])
def send_message():
  intents = {
    "solicitud_de_tarjeta" : "Hemos terminado de validar tus datos personales, damos inicio a la solicitud del trámite el día $fecha a las $hora. El plazo de entrega de tu nueva tarjeta es de 4 a 6 días y se realizará en el domicilio ingresado en el sistema.",
    "entrega_de_tarjeta" : "La tarjeta en la oficina $NombreOficina puedes recogerla en dicho local o esperar 2 días hábiles. Si no se te entrega en ese plazo, por favor, vuelve a comunicarte con nosotros.",
    "cancelacion_tarjeta" : "",
    "saludos" : "Con fecha 23 de abril, a las 6:30 p.m., se ha procedido con la cancelación de tu tarjeta con número: 1111 1111 1111 1111",
    "robo_tarjeta" : "Con fecha 23 de abril, a las 6:30 p.m. Se ha procedido con el bloqueo de tu tarjeta con número: 1111 1111 1111 1111",
    "consulta_millas" : "Al día de hoy cuentas con 1500 millas disponibles que expiran el 30 de abril del 2023",
    "cobro_no_reconocido" : "Para continuar con el registro de un reclamo te voy a transferir a un agente especializado",
    "ver_estado_cuenta" : "Tienes un consumo del 10 de abril por 150 en el restaurant el Hornero, un consumo del 11 de abril por 300 soles a la empresa Bitel y un consumo de 50 en Rappi.",
    "hablar_con_humano" : "Te estamos transfiriendo a la cola de atención de agentes especializados.",
    "volver_a_empezar" : "",
    "afirmación" : "",
    "negacion" : "",
    "despedida" : "",
    "enojo" : "",
  }

  message = request.form['message']
  
  count_vectorizer = pickle.load(open("count_vectorizer.pickle", "rb"))
  decision_tree_classifier = pickle.load(open("decision_tree_classifier.pickle", "rb"))
  rules = pickle.load(open("rules.pickle", "rb"))
  utterances_examples = pickle.load(open("utterances_examples.pickle", "rb"))
  
  # if message != 'Yakarta':
  #   answer, intent = return_answer(message, count_vectorizer, decision_tree_classifier, rules, utterances_examples)
  # else:
  #   answer = message
  if not ('res' in globals()):
    global res
    answer, intent = return_answer(message, count_vectorizer, decision_tree_classifier, rules, utterances_examples)
    res = intents[intent]
  else:
    if res != '':
      if message.capitalize() == 'Si' or message.capitalize() == 'Sí':
        global personalData
        personalData = True
      if message.capitalize() != 'No' and not ('cardNumber' in globals()):
        global cardNumber
        cardNumber = ''
        answer = 'Por favor, bríndanos tus datos. Ingresa el número de tu tarjeta.'
        personalData = False
      elif message.capitalize() != 'No' and not ('identityNumber' in globals()):
        cardNumber = message
        global identityNumber
        identityNumber = ''
        answer = 'Por favor, ingresa el número de tu DNI'
        personalData = False
      elif message.capitalize() != 'No' and not ('birthDate' in globals()):
        identityNumber = message
        global birthDate
        birthDate= ''
        answer = 'Ahora por favor, ingresa tu fecha de nacimiento'
        personalData = False
      else:
        birthDate = message
        if not personalData: 
          answer = 'Validación de datos confirmada, muchas gracias.\n' + res
        else:
          answer = res
        answer = answer + '\n¿Necesitas algo más?'
        if message.capitalize() == 'No':
          answer = '¿En que más puedo ayudarte?'
        res = ''
        personalData = True
    else:
      if  message.capitalize() == 'No':
        answer = 'Fue un gusto atenderte. Adiós.'
      elif message.capitalize() == 'Si' or message.capitalize() == 'Sí':
        answer = '¿En qué más puedo ayudarte?'
      else:
        answer, intent = return_answer(message, count_vectorizer, decision_tree_classifier, rules, utterances_examples)
        if intent in intents:
          res = intents[intent]

  
  response_text = { "message":  answer }
  return jsonify(response_text)


if __name__ == '__main__':
    app.run(debug=True)