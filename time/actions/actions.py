# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



from typing import Any, Text, Dict, List

import arrow
import dateparser

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import EventType
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from db_connectivity import PersonInsert, PersonSelect, CitySelect, PersonDelete

city_db = {
    'Brussels': 'Europe/Brussels',
    'Zagreb': 'Europe/Zagreb',
    'Fortaleza': 'America/Fortaleza',
    'Paris': 'Europe/Paris',
    'Washington': 'US/Pacific',
    'Moscow': 'Europe/Moscow',
    'Buenos Aires': 'America/Argentina/Buenos_Aires',
    'London': 'Europe/London',
    'Lisbon': 'Europe/Lisbon',
    'Madrid': 'Europe/Madrid',
    'Amsterdam': 'Europe/Amsterdam',
    'Cairo': 'Africa/Cairo',
    'Berlin': 'Europe/Berlin',
}

ALLOWED_LANGUAGES = {
    "en": "I want to speak in English",
    "pt": "Eu quero falar em Português",
    "de": "Ich will auf Deutsch sprechen",
}

ALLOWED_EDUCATION_LEVELS_PORT = [
    "Ensino Fundamental",
    "Ensino Médio",
    "Ensino Técnico",
    "Ensino Superior",
    "Especialização",
    "Mestrado",
    "Doutorado",
]

ALLOWED_EDUCATION_LEVELS_ENG = [
    "Elementary Education",
    "Secondary Education",
    "Technical or Vocational Education",
    "Bachelor",
    "Master",
    "PhD",
]

ALLOWED_EDUCATION_LEVELS_DEUT = [
    "Grundschule",
    "Hauptschule",
    "Realschule",
    "Gesamtschule",
    "Gymnasium",
    "Berufsschule oder Fachoberschule",
    "Bachelor",
    "Master",
    "Promotion",
]

class DeletePersonAction(Action):
    def name(self) -> Text:
        return "action_delete_person"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        current_language = tracker.get_slot("language")
        person_id = tracker.get_slot("person_id")

        person = PersonSelect(person_id)
        name = person['name']
        age = person['age']
        education_level = person['education_level']
        language = person['language']

        if current_language == 'pt':
            dispatcher.utter_message(text=f"Encontrei seu cadastro.") 
            dispatcher.utter_message(text=f"Seu cadastro:\n - ID: {person_id}\n - Nome: {name} \n - Idade: {age} anos\n - Nível educacional: {education_level}\n - Idioma: {language}")  
            PersonDelete(person_id)
            dispatcher.utter_message(text=f"Eu deletei seu cadastro.")
        elif current_language == 'de':
            dispatcher.utter_message(text=f"Ich habe Ihre Anmeldung gefunden")
            dispatcher.utter_message(text=f"Ihre Anmeldung:\n - ID: {person_id}\n - Vorname: {name} \n - Alter: {age} Jahren\n - Bildungsniveau: {education_level}\n - Sprache: {language}")  
            PersonDelete(person_id)
            dispatcher.utter_message(text=f"Ich habe Ihre Registrierung gelöscht.")
        elif current_language == 'en':
            dispatcher.utter_message(text=f"I have found your registration.")
            dispatcher.utter_message(text=f"Your registration:\n - ID: {person_id}\n - Name: {name} \n - Age: {age} years\n - Educational Level: {education_level}\n - Language: {language}") 
            PersonDelete(person_id)
            dispatcher.utter_message(text=f"I deleted your registration.")
        else:
            dispatcher.utter_message(text=f"I have found your registration.")
            dispatcher.utter_message(text=f"Your registration:\n - ID: {person_id}\n - Name: {name} \n - Age: {age} years\n - Educational Level: {education_level}\n - Language: {language}") 
            PersonDelete(person_id)
            dispatcher.utter_message(text=f"I deleted your registration.")


        return []

class SelectPersonAction(Action):
    def name(self) -> Text:
        return "action_select_person"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        current_language = tracker.get_slot("language")
        person_id = tracker.get_slot("person_id")

        person = PersonSelect(person_id)
        name = person['name']
        age = person['age']
        education_level = person['education_level']
        language = person['language']

        if current_language == 'pt':
            dispatcher.utter_message(text=f"Encontrei seu cadastro.") 
            dispatcher.utter_message(text=f"Seu cadastro:\n - ID: {person_id}\n - Nome: {name} \n - Idade: {age} anos\n - Nível educacional: {education_level}\n - Idioma: {language}")  
        elif current_language == 'de':
            dispatcher.utter_message(text=f"Ich habe Ihre Anmeldung gefunden")
            dispatcher.utter_message(text=f"Ihre Anmeldung:\n - ID: {person_id}\n - Vorname: {name} \n - Alter: {age} Jahren\n - Bildungsniveau: {education_level}\n - Sprache: {language}")  
        elif current_language == 'en':
            dispatcher.utter_message(text=f"I have found your registration.")
            dispatcher.utter_message(text=f"Your registration:\n - ID: {person_id}\n - Name: {name} \n - Age: {age} years\n - Educational Level: {education_level}\n - Language: {language}") 
        else:
            dispatcher.utter_message(text=f"I have found your registration.")
            dispatcher.utter_message(text=f"Your registration:\n - ID: {person_id}\n - Name: {name} \n - Age: {age} years\n - Educational Level: {education_level}\n - Language: {language}") 

        return []

class ActionStart(Action):

    def name(self) -> Text:
        return "action_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(
            text=f"Which language do you want to speak? \n Em qual idioma você deseja conversar? \n Welche Sprach möchten Sie sprechen?",
            buttons=[{"title": q, "payload": p} for p,q in ALLOWED_LANGUAGES.items()],
        )
        return []

class ActionChooseLanguage(Action):

    def name(self) -> Text:
        return "action_choose_language"

    def run(
    self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        current_language = tracker.get_slot("language")

        if current_language == 'pt':
            msg=f"Então, vamos falar em Português!"
        elif current_language == 'de':
            msg=f"Sie sprechen auf Deutsch!"
        elif current_language == 'en':
            msg=f"Then, we will speak in English!"
        else:
            msg=f"I can't speak this language.\n Eu não falo esse idioma. \n Ich kann diese Spache nicht sprechen."

        dispatcher.utter_message(text=msg)
        return []


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        name = tracker.get_slot("name")
        age = tracker.get_slot("age")
        education_level = tracker.get_slot("education_level")
        current_language = tracker.get_slot("language")

        id = PersonInsert(name, age, education_level, current_language)

        if current_language == 'pt':
            dispatcher.utter_message(text=f"Eu vou submeter o seu cadastro agora!") 
            dispatcher.utter_message(text=f"Seu cadastro:\n - ID: {id}\n - Nome: {name} \n - Idade: {age} anos\n - Nível educacional: {education_level}\n - Idioma: {current_language}")  
        elif current_language == 'de':
            dispatcher.utter_message(text=f"Ich werde Ihre Anmeldung jetzt absenden!")
            dispatcher.utter_message(text=f"Ihre Anmeldung:\n - ID: {id}\n - Vorname: {name} \n - Alter: {age} Jahren\n - Bildungsniveau: {education_level}\n - Sprache: {current_language}")  
        elif current_language == 'en':
            dispatcher.utter_message(text=f"I will submit your registration now!")
            dispatcher.utter_message(text=f"Your registration:\n - ID: {id}\n - Name: {name} \n - Age: {age} years\n - Educational Level: {education_level}\n - Language: {current_language}")  
        else:
            dispatcher.utter_message(text=f"I will submit your registration now!")
            dispatcher.utter_message(text=f"Your registration:\n - ID: {id}\n - Name: {name} \n - Age: {age} years\n - Educational Level: {education_level}\n - Language: {current_language}") 

        return []

class AskForEducationLevelAction(Action):
    def name(self) -> Text:
        return "action_ask_education_level"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        current_language = tracker.get_slot("language")

        if current_language == 'pt':
            dispatcher.utter_message(
                text=f"Qual é o seu nível educacional?",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_EDUCATION_LEVELS_PORT],
            )
        elif current_language == 'de':
            dispatcher.utter_message(
                text=f"Was ist Ihr Bildungsniveau?",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_EDUCATION_LEVELS_DEUT],
            )
        elif current_language == 'en':
            dispatcher.utter_message(
                text=f"What is your educational level?",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_EDUCATION_LEVELS_ENG],
            )
        else:
            dispatcher.utter_message(
                text=f"What is your educational level?",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_EDUCATION_LEVELS_ENG],
            )

        return []

class ValidateSimplePersonForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_person_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name` value."""

        current_language = tracker.get_slot("language")

        if isinstance(slot_value.lower(), str):
            if current_language == 'pt':
                dispatcher.utter_message(text=f"OK! Seu nome é {slot_value}.")
            elif current_language == 'de':
                dispatcher.utter_message(text=f"OK! Ihre Vorname ist {slot_value}.")
            elif current_language == 'en':
                dispatcher.utter_message(text=f"OK! Your name is {slot_value}.")
            return {"name": slot_value}            
        
        dispatcher.utter_message(text=f"Por favor, digite apenas caracteres.")
        return {"name": None}

    def validate_age(
        self,
        slot_value: float,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `age` value."""

        current_language = tracker.get_slot("language")

        if current_language == 'pt':
            dispatcher.utter_message(text=f"OK! Você tem {slot_value} anos.")
        elif current_language == 'de':
            dispatcher.utter_message(text=f"OK! Sie sind {slot_value} Jahre alt.")
        elif current_language == 'en':
            dispatcher.utter_message(text=f"OK! You are {slot_value} years old.")
        else:
            dispatcher.utter_message(text=f"OK! You are {slot_value} years old.")

        return {"age": slot_value}

    def validate_education_level(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `education_level` value."""

        current_language = tracker.get_slot("language")

        if current_language == "pt" and slot_value not in ALLOWED_EDUCATION_LEVELS_PORT:
            dispatcher.utter_message(text=f"Eu não reconheço esse nível educacional.")
            dispatcher.utter_message(
                text=f"Escolha um dos níveis abaixo:",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_EDUCATION_LEVELS_PORT],
            )
            return {"education_level": None}
        elif current_language == "en" and slot_value not in ALLOWED_EDUCATION_LEVELS_ENG:
            dispatcher.utter_message(text=f"I don't recognise this educational level.")
            dispatcher.utter_message(
                text=f"Choose one of the following:",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_EDUCATION_LEVELS_ENG],
            )
            return {"education_level": None}
        elif current_language == "de" and slot_value not in ALLOWED_EDUCATION_LEVELS_DEUT:
            dispatcher.utter_message(text=f"Ich erkenne dieses Bildungsniveau nicht an.")
            dispatcher.utter_message(
                text=f"Wähle eines der Folgenden:",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_EDUCATION_LEVELS_DEUT],
            )
        elif current_language == None and slot_value not in ALLOWED_EDUCATION_LEVELS_DEUT:
            dispatcher.utter_message(text=f"I don't recognise this educational level.")
            dispatcher.utter_message(
                text=f"Choose one of the following:",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_EDUCATION_LEVELS_ENG],
            )
            return {"education_level": None}

        if current_language == 'pt':
            dispatcher.utter_message(text=f"OK! Você tem o seguinte nível educacional: {slot_value}.")
        elif current_language == 'de':
            dispatcher.utter_message(text=f"OK! Sie haben folgendes Bildingsniveau  : {slot_value}.")
        elif current_language == 'en':
            dispatcher.utter_message(text=f"OK! You have the following educational level: {slot_value}.")
        else:
            dispatcher.utter_message(text=f"OK! You have the following educational level: {slot_value}.")

        return {"education_level": slot_value}

class ActionRememberWhere(Action):

    def name(self) -> Text:
        return "action_remember_where"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_language = tracker.get_slot("language")
        current_place = (next(tracker.get_latest_entity_values("place"), None)).capitalize()
        utc = arrow.utcnow()

        if not current_place:
            if current_language == 'pt':
                msg = f"Eu não entendi onde você vive. Escolha uma das cidades disponíveis"
            elif current_language == 'en':
                msg = f"I didn't understand where you live. Choose one of the available cities."
            elif current_language == 'de':
                msg = f"Ich habe nicht verstanden, wo Sie leben. Wählen Sie eine der verfügbaren Städte aus."
            else:
                msg = f"I didn't understand where you live. Choose one of the available cities."
            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": p} for p in city_db],
            )    
            return []

        #tz_string = city_db.get(current_place, None)
        tz_string = CitySelect(current_place)

        if not tz_string:
            if current_language == 'pt':
                msg = f"Eu não reconheci {current_place}. Escolha uma das cidades disponíveis"
            elif current_language == 'en':
                msg = f"I didn't recognize {current_place}. Choose one of the available cities."
            elif current_language == 'de':
                msg = f"Ich habe {current_place} nicht wiedererkannt. Wählen Sie eine der verfügbaren Städte aus."
            else:
                msg = f"I didn't recognize {current_place}. Choose one of the available cities."
            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": p} for p in city_db],
            )             
            return []


        if current_language == 'pt':
            msg = f"Ok. Irei me lembrar que você mora em {current_place}."
        elif current_language == 'en':
            msg = f"Ok. I will remember that you live in {current_place}."
        elif current_language == 'de':
            msg = f"Ok. Ich werde mich daran erinnern, dass Sie in {current_place} leben."
        else:
            msg = f"Ok. I will remember that you live in {current_place}."
    
        dispatcher.utter_message(text=msg)


        if current_language == 'pt':
            msg = f"É {utc.to(tz_string).format('HH:mm')} em {current_place} agora."
        elif current_language == 'en':
            msg = f"It is {utc.to(tz_string).format('HH:mm')} in {current_place} now."
        elif current_language == 'de':
            msg = f"Es ist jetzt {utc.to(tz_string).format('HH:mm')} in {current_place}."
        else:
            msg = f"It is {utc.to(tz_string).format('HH:mm')} in {current_place} now."

        dispatcher.utter_message(text=msg)

        return [SlotSet("location", current_place)]


class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_language = tracker.get_slot("language") 
        current_place = next(tracker.get_latest_entity_values("place"), None)
        dispatcher.utter_message(msg="current_place")
        utc = arrow.utcnow()

        if not current_place:

            if current_language == 'pt':
                msg = f"É {utc.format('HH:mm')} utc agora. Você também pode me dar uma localização."
            elif current_language == 'de':
                msg = f"Es ist jetzt {utc.format('HH:mm')} utc. Sie können mir auch einen Standort nennen."
            elif current_language == 'en':
                msg = f"It is {utc.format('HH:mm')} utc now. You can give me a place."
            else:
                msg = f"It is {utc.format('HH:mm')} utc now. You can give me a place."

            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": "Moro em " + p} for p in city_db],
            )     
            return []

        tz_string = CitySelect(current_place)
        #tz_string = city_db.get(current_place.capitalize(), None)

        if not tz_string:
            if current_language == 'pt':
                msg = f"Eu não reconheci {current_place}. Escolha uma das cidades disponíveis"
            elif current_language == 'en':
                msg = f"I didn't recognize {current_place}. Choose one of the available cities."
            elif current_language == 'de':
                msg = f"Ich habe {current_place} nicht wiedererkannt. Wählen Sie eine der verfügbaren Städte aus."
            else:
                msg = f"I didn't recognize {current_place}. Choose one of the available cities."

            dispatcher.utter_message(
                text=msg,
                #buttons=[{"title": p, "payload": "Moro em " + p} for p in city_db],
            )                 
            return []

        if current_language == 'pt':
            msg = f"É {utc.to(tz_string).format('HH:mm')} em {current_place} agora."
        elif current_language == 'en':
            msg = f"It is {utc.to(tz_string).format('HH:mm')} in {current_place} now."
        elif current_language == 'de':
            msg = f"Es ist jetzt {utc.to(tz_string).format('HH:mm')} in {current_place}."
        else:
            msg = f"It is {utc.to(tz_string).format('HH:mm')} in {current_place} now."

        dispatcher.utter_message(text=msg)

        return []

class ActionTimeDifference(Action):

    def name(self) -> Text:
        return "action_time_difference"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        timezone_in = (tracker.get_slot("location")).capitalize()
        timezone_to = next(tracker.get_latest_entity_values("place"), None)
        
        current_language = tracker.get_slot("language")

        if not timezone_in:
            if current_language == 'pt':
                msg = "Para calcular a diferença em horas eu preciso saber onde você mora."
            elif current_language == 'en':
                msg = "To calculate the difference in hours, I need to know where you live."
            elif current_language == 'de':
                msg = "Um den Studenunterschied zu berechnen, muss ich wissen, wo Sie wohnen."
            else:
                msg = "To calculate the difference in hours, I need to know where you live."

            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": "Moro em " + p} for p in city_db],
            )     
            return []            
        
        if not timezone_to:

            if current_language == 'pt':
                msg = "Eu não entendi com qual timezone você deseja comparar. Escolha uma das disponíveis:"
            elif current_language == 'en':
                msg = "I didn't understand which timezone you want to compare with. Choose one of the availables ones:"
            elif current_language == 'de':
                msg = "Ich verstehe nicht, mit welcher Zeitzone Sie vergleichen möchten. Wählen Sie eine der verfügbaren aus:"
            else:
                msg = "I didn't understand which timezone you want to compare with. Choose one of the availables ones:"

            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": "Qual a diferença para " + p} for p in city_db],
            )     

            return []  

        #tz_string = city_db.get(timezone_to.capitalize(), None)
        tz_string = CitySelect(timezone_to)

        if not tz_string:
            if current_language == 'pt':
                msg = f"Eu não reconheci {timezone_to}. Escolha uma das disponíveis:"
            elif current_language == 'en':
                msg = f"I didn't recognize {timezone_to}. Choose one of the available ones:"
            elif current_language == 'de':
                msg = f"Ich habe {timezone_to} nicht wiedererkannt. Wählen Sie eine der verfügbaren aus:"
            else:
                msg = f"I didn't recognize {timezone_to}. Choose one of the available ones:"

            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": "Qual a diferença para " + p} for p in city_db],
            )     
            return []
        
        t1 = arrow.utcnow().to(CitySelect(timezone_to))
        t2 = arrow.utcnow().to(CitySelect(timezone_in)) 

        #t1 = arrow.utcnow().to(city_db[timezone_to])
        #t2 = arrow.utcnow().to(city_db[timezone_in])    

        max_t = max(t1, t2) 
        min_t = min(t1, t2)      

        diff_seconds = dateparser.parse(str(max_t)[:19]) - dateparser.parse(str(min_t)[:19])
        diff_hours = int(diff_seconds.seconds/3600)

        if diff_hours == 0:
            if current_language == 'pt':
                msg = f"Entre " + timezone_in.capitalize() + " e " + timezone_to.capitalize() + ", não há diferença horária."
            elif current_language == 'en':
                msg = f"Among " + timezone_in.capitalize() + " and " + timezone_to.capitalize() + ", there is no time difference."
            elif current_language == 'de':
                msg = f"Zwischen " + timezone_in.capitalize() + " und " + timezone_to.capitalize() + " gibt es keinen Zeitunterschied."
            else:
                msg = f"Among " + timezone_in.capitalize() + " and " + timezone_to.capitalize() + ", there is no time difference."

        elif diff_hours == 1:
            if current_language == 'pt':
                msg = f"Entre " + timezone_in.capitalize() + " e " + timezone_to.capitalize() + ", há apenas 1 hora de diferença."
            elif current_language == 'en':
                msg = f"Among " + timezone_in.capitalize() + " and " + timezone_to.capitalize() + ", there is only 1 hour difference."
            elif current_language == 'de':
                msg = f"Zwischen " + timezone_in.capitalize() + " und " + timezone_to.capitalize() + " gibt es nur eine Stunde Unterschied."
            else:
                msg = f"Among " + timezone_in.capitalize() + " and " + timezone_to.capitalize() + ", there is only 1 hour difference."

        else:
            if current_language == 'pt':
                msg = f"Entre " + timezone_in.capitalize() + " e " + timezone_to.capitalize() + f", há {min(diff_hours, 24-diff_hours)} horas de diferença."
            elif current_language == 'en':
                msg = f"Among " + timezone_in.capitalize() + " and " + timezone_to.capitalize() + f", there is a {min(diff_hours, 24-diff_hours)} hours difference."
            elif current_language == 'de':
                msg = f"Zwischen " + timezone_in.capitalize() + " und " + timezone_to.capitalize() + f", gibt es {min(diff_hours, 24-diff_hours)} Stunden Unterschied."
            else:
                msg = f"Among " + timezone_in.capitalize() + " and " + timezone_to.capitalize() + f", there is a {min(diff_hours, 24-diff_hours)} hours difference."

        dispatcher.utter_message(text=msg)

        return []
