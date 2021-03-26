
from __future__ import print_function
import requests
import random
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }




# --------------- Functions that control the skill's behavior ------------------
def get_indices_response(intent):

    session_attributes = {}
    index = requests.get(" http://api.kpiro.com/allindices.json").json()
    object = intent['slots']['indice']['value'].upper()
    # print(object)
    card_title = "INDEX_PRICE"
    object = object.replace(" ", "")
    names = index.keys()
    lst = ['nifty fifty','nifty next fifty','nifty five hundred','nifty auto','nifty hundred']
    if object not in names:
        speech_output = 'I am not sure about it as you have given a wrong index name, please try again. Try saying price of {}. If you want to close the application say cancel or stop'.format(random.choice(lst))
        reprompt_text = "You never responded to the first message. Sending another one."
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        if intent_name == "indices":
            return get_indices_response(intent)
        
    else :
        cost = index[object]['ltp']
        speech_output = 'last traded price of {0} is {1}. If you want to close the application say cancel or stop, else try for some index name'.format(object,str(cost))
        reprompt_text = "You never responded to the first test message. Sending another one."
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello my friend, tell me the name of index and I'll give you its last traded price. You can start by saying 'price of nifty fifty or nifty auto"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your index price alexa application! Start by saying 'price of nifty auto or price of nifty fifty'"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the index price application. If you again want to start application, say 'Alexa run index price application'. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "indices":
        return get_indices_response(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
