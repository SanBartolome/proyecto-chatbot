from flask import Flask, request, jsonify, render_template, make_response, session
import pickle
from chatbot import return_answer

app = Flask(__name__)
app.secret_key = '123dJSi&JHD$jJDnk754'

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

  response = session.get('response')
  if response == None:
    answer, intent = return_answer(message, count_vectorizer, decision_tree_classifier, rules, utterances_examples)
    res = intents[intent]
    session['response'] = res
  else:
    if response != '':
      personalData = session.get('personalData')
      cardNumber = session.get('cardNumber')
      identityNumber = session.get('identityNumber')
      identityBirthdate = session.get('identityBirthdate')     
      if message.capitalize() == 'Si' or message.capitalize() == 'Sí':
        session['personalData'] = True
      if message.capitalize() != 'No' and cardNumber == None:
        session['cardNumber'] = ''
        session['personalData'] = False
        answer = 'Por favor, bríndanos tus datos. Ingresa el número de tu tarjeta.'
      elif message.capitalize() != 'No' and identityNumber == None:
        session['cardNumber'] = message
        session['identityNumber'] = ''
        session['personalData'] = False
        answer = 'Por favor, ingresa el número de tu DNI'
      elif message.capitalize() != 'No' and identityBirthdate == None:
        session['identityNumber'] = message
        session['identityBirthdate'] = ''
        session['personalData'] = False
        answer = 'Ahora por favor, ingresa tu fecha de nacimiento'
        print('No. Ask date')
      else:
        session['identityBirthdate'] = message
        if personalData == False: 
          answer = 'Validación de datos confirmada, muchas gracias.\n' + response
        else:
          answer = response
        answer = answer + '\n¿Necesitas algo más?'
        if message.capitalize() == 'No':
          answer = '¿En que más puedo ayudarte?'
        session['response'] = ''
        session['personalData'] = True
    else:
      if  message.capitalize() == 'No':
        answer = 'Fue un gusto atenderte. Adiós.'
      elif message.capitalize() == 'Si' or message.capitalize() == 'Sí':
        answer = '¿En qué más puedo ayudarte?'
      else:
        answer, intent = return_answer(message, count_vectorizer, decision_tree_classifier, rules, utterances_examples)
        if intent in intents:
          session['response'] = intents[intent]

  
  response_text = { "message":  answer }
  return jsonify(response_text)


if __name__ == '__main__':
    app.run(debug=True)