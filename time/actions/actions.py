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
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from db_connectivity import DataUpdate

city_db = {
    'Brussels': 'Europe/Brussels',
    'Zagreb': 'Europe/Zagreb',
    'Brasilia': 'America/Fortaleza',
    'Paris': 'Europe/Paris',
    'Washington': 'US/Pacific',
    'Moscow': 'Europe/Moscow',
    'Buenos Aires': 'America/Argentina/Buenos_Aires',
    'London': 'Europe/London',
    'Lisbon': 'Europe/Lisbon',
    'Madrid': 'Europe/Madrid',
    'Amsterdam': 'Europe/Amsterdam',
    'Cairo': 'Africa/Cairo',
    'Karlsruhe': 'Europe/Berlin',
    'Berlin': 'Europe/Berlin',
}

ALLOWED_EDUCATION_LEVELS = [
    "Ensino Fundamental",
    "Ensino Médio",
    "Ensino Técnico",
    "Ensino Superior",
    "Especialização",
    "Mestrado",
    "Doutorado",
]


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        name = tracker.get_slot("name")
        age = tracker.get_slot("age")
        education_level = tracker.get_slot("education_level")

        dispatcher.utter_message(text=f"Eu vou submeter o seu cadastro agora!")
        msg = f"Seu cadastro:\n - Nome: {name} \n - Idade: {age} anos\n - Nível educacional: {education_level}"  
        DataUpdate(name, age, education_level)
        dispatcher.utter_message(text=msg)

        return []

class AskForEducationLevelAction(Action):
    def name(self) -> Text:
        return "action_ask_education_level"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        #if tracker.get_slot("person_register"):
        dispatcher.utter_message(
            text=f"Qual é o seu nível educacional?",
            buttons=[{"title": p, "payload": p} for p in ALLOWED_EDUCATION_LEVELS],
        )
       # else:
            #dispatcher.utter_message(
                #text=f"Tchau!",
            #)
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

        if isinstance(slot_value.lower(), str):
            dispatcher.utter_message(text=f"OK! Seu nome é {slot_value}.")
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

        dispatcher.utter_message(text=f"OK! Você tem {slot_value} anos.")
        return {"age": slot_value}

    def validate_education_level(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `education_level` value."""

        if slot_value not in ALLOWED_EDUCATION_LEVELS:
            dispatcher.utter_message(text=f"Eu não reconheço esse nível educacional. Escolha entre: {', '.join(ALLOWED_EDUCATION_LEVELS)}.")
            return {"education_level": None}
        dispatcher.utter_message(text=f"OK! Você tem o seguinte nível educacional: {slot_value}.")
        return {"education_level": slot_value}

class ActionRememberWhere(Action):

    def name(self) -> Text:
        return "action_remember_where"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #if tracker.get_intent_of_latest_message() == "where_i_live":
            #dispatcher.utter_message(
                #text=f"Onde você mora?",
                #buttons=[{"title": p, "payload": p} for p in city_db],
            #) 

        current_place = (next(tracker.get_latest_entity_values("place"), None)).capitalize()
        utc = arrow.utcnow()

        if not current_place:
            msg = f"Eu não entendi onde você vive. Escolha uma das cidades disponíveis"
            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": p} for p in city_db],
            )    
            return []

        tz_string = city_db.get(current_place, None)

        if not tz_string:
            msg = f"Eu não reconheci {current_place}. Escolha uma das cidades disponíveis"
            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": p} for p in city_db],
            )             
            #msg = f"I didn't recognize {current_place}. Is it spelled correctly?"
            return []
        
        msg = f"Ok. Irei me lembrar que você mora em {current_place}."
        dispatcher.utter_message(text=msg)

        msg = f"É {utc.to(city_db[current_place]).format('HH:mm')} em {current_place} agora."
        dispatcher.utter_message(text=msg)

        return [SlotSet("location", current_place)]


class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()

        if not current_place:
            msg = f"É {utc.format('HH:mm')} utc agora. Você também pode me dar uma localização."
            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": "Moro em " + p} for p in city_db],
            )     
            return []

        tz_string = city_db.get(current_place.capitalize(), None)

        if not tz_string:
            msg = f"Eu não reconheci {current_place}. Escolha uma das cidades disponíveis"
            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": "Moro em " + p} for p in city_db],
            )                 
            return []

        msg = f"É {utc.to(city_db[current_place]).format('HH:mm')} em {current_place} agora."
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
        
        if not timezone_in:
            msg = "Para calcular a diferença em horas eu preciso saber onde você mora."
            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": "Moro em " + p} for p in city_db],
            )     
            return []            
        
        if not timezone_to:
            msg = "Eu não entendi com qual timezone você deseja comparar. Escolha uma das disponíveis:"
            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": "Qual a diferença para " + p} for p in city_db],
            )     
            #msg = "I didn't get the timezone you'd like to compare against. Are you sure it's spelled correctly?"
            return []  

        tz_string = city_db.get(timezone_to.capitalize(), None)

        if not tz_string:
            msg = f"Eu não reconheci {timezone_to}. Escolha uma das disponíveis:"
            dispatcher.utter_message(
                text=msg,
                buttons=[{"title": p, "payload": "Qual a diferença para " + p} for p in city_db],
            )     
            return []
        
        t1 = arrow.utcnow().to(city_db[timezone_to])
        t2 = arrow.utcnow().to(city_db[timezone_in])     

        max_t = max(t1, t2) 
        min_t = min(t1, t2)      

        diff_seconds = dateparser.parse(str(max_t)[:19]) - dateparser.parse(str(min_t)[:19])
        diff_hours = int(diff_seconds.seconds/3600)

        if diff_hours == 0:
            msg = f"De " + timezone_in.capitalize() + " para " + timezone_to.capitalize() + ", não há diferença horária."
        elif diff_hours == 1:
            msg = f"De " + timezone_in.capitalize() + " para " + timezone_to.capitalize() + ", há apenas 1 hora de diferença."
        else:
            msg = f"De " + timezone_in.capitalize() + " para " + timezone_to.capitalize() + f", há {min(diff_hours, 24-diff_hours)} horas de diferença."
        #msg = f"From {timezone_in} to {timezone_to}, there is a {min(diff_hours, 24-diff_hours)}H time difference."
        dispatcher.utter_message(text=msg)

        return []
