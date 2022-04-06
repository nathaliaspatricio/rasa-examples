# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



from typing import Any, Text, Dict, List

import arrow
import dateparser

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

city_db = {
    'brussels': 'Europe/Brussels',
    'zagreb': 'Europe/Zagreb',
    'brasilia': 'America/Fortaleza',
    'paris': 'Europe/Paris',
    'washington': 'US/Pacific',
    'moscow': 'Europe/Moscow',
    'buenos aires': 'America/Argentina/Buenos_Aires',
    'london': 'Europe/London',
    'lisbon': 'Europe/Lisbon',
    'madrid': 'Europe/Madrid',
    'amsterdam': 'Europe/Amsterdam',
    'cairo': 'Africa/Cairo',
    'karlsruhe': 'Europe/Berlin',
    'berlin': 'Europe/Berlin',
}

class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = next(tracker.get_latest_entity_values("name"), None)
        
        if not name:
            msg = f"Oi, como você está?"
            dispatcher.utter_message(text=msg)
        else:
            msg = f"Oi, {name}. Como você está?"
            dispatcher.utter_message(text=msg)
        
        return []

class ActionRememberWhere(Action):

    def name(self) -> Text:
        return "action_remember_where"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()

        if not current_place:
            msg = f"Eu não entendi onde você vive. Você tem certeza que está escrito corretamente?"
            dispatcher.utter_message(text=msg)
            return []

        tz_string = city_db.get(current_place, None)

        if not tz_string:
            msg = f"Eu não reconheci {current_place}. Está escrito corretamente?"            
            #msg = f"I didn't recognize {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
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
            dispatcher.utter_message(text=msg)
            return []

        tz_string = city_db.get(current_place, None)

        if not tz_string:
            msg = f"Eu não reconheci {current_place}. Está escrito corretamente?"            
            dispatcher.utter_message(text=msg)
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

        timezone_in = tracker.get_slot("location")
        timezone_to = next(tracker.get_latest_entity_values("place"), None)
        
        if not timezone_in:
            msg = "Para calcular a diferença em horas eu preciso saber onde você mora."
            #msg = "To calculate the time difference I need to know where you live."
            dispatcher.utter_message(text=msg)
            return []            
        
        if not timezone_to:
            msg = "Eu não entendi com qual timezone você deseja comparar. Você tem certeza que está escrito corretamente?"
            #msg = "I didn't get the timezone you'd like to compare against. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []  

        tz_string = city_db.get(timezone_to, None)

        if not tz_string:
            msg = f"Eu não reconheci {timezone_to}. Está escrito corretamente?"
            dispatcher.utter_message(text=msg)
            return []
        
        t1 = arrow.utcnow().to(city_db[timezone_to])
        t2 = arrow.utcnow().to(city_db[timezone_in])     

        max_t = max(t1, t2) 
        min_t = min(t1, t2)      

        diff_seconds = dateparser.parse(str(max_t)[:19]) - dateparser.parse(str(min_t)[:19])
        diff_hours = int(diff_seconds.seconds/3600)

        if diff_hours == 0:
            msg = f"De {timezone_in} para {timezone_to}, não há diferença horária."
        elif diff_hours == 1:
            msg = f"De {timezone_in} para {timezone_to}, há apenas 1 hora de diferença."
        else:
            msg = f"De {timezone_in} para {timezone_to}, há {min(diff_hours, 24-diff_hours)} horas de diferença."
        #msg = f"From {timezone_in} to {timezone_to}, there is a {min(diff_hours, 24-diff_hours)}H time difference."
        dispatcher.utter_message(text=msg)

        return []
