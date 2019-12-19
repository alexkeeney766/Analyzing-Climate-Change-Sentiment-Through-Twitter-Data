import re

states_psuedonym = {
    "Alabama": ["Alabama", "AL"],
    "Alaska": ["Alaska", "AK"],
    "Arizona": ["Arizona", "AZ"],
    "Arkansas": ["Arkansas", "AR"],
    "California": ["California", "CA", "San Diego", "Los Angeles"],
    "Colorado": ["Colorado", "CO"],
    "Connecticut": ["Connecticut", "CT"],
    "Delaware": ["Delaware", "DE"],
    "Florida": ["Florida", "FL"],
    "Georgia": ["Georgia", "GA"],
    "Hawaii": ["Hawaii", "HI"],
    "Idaho": ["Idaho", "ID"],
    "Illinois": ["Illinois", "IL"],
    "Indiana": ["Indiana", "IN"],
    "Iowa": ["Iowa", "IA"],
    "Kansas": ["Kansas", "KS"],
    "Kentucky": ["Kentucky", "KY"],
    "Louisiana": ["Louisiana", "LA"], # Might conflict with LA california
    "Maine" : ["Maine", "ME"],
    "Maryland": ["Maryland", "MD"],
    "Massachusetts": ["Massachusetts", "MA"],
    "Michigan": ["Michigan", "MI"],
    "Minnesota": ["Minnesota", "MN"],
    "Mississippi": ["Mississippi", "MS"],
    "Missouri": ["Missouri", "MO"],
    "Montana": ["Montana", "MT"],
    "Nebraska": ["Nebraska", "NE"],
    "Nevada": ["Nevada", "NV"],
    "New Hampshire": ["New Hampshire", "NH"],
    "New Jersey": ["New Jersey", "NJ"],
    "New Mexico": ["New Mexico", "NM"],
    "New York": ["New York", "NY"],
    "North Carolina": ["North Carolina", "NC"],
    "North Dakota": ["North Dakota", "ND"],
    "Ohio": ["Ohio", "OH"],
    "Oklahoma": ["Oklahoma", "OK"],
    "Oregon": ["Oregon", "OR"],
    "Pennsylvania": ["Pennsylvania", "PA"],
    "Rhode Island": ["Rhode Island", "RI"],
    "South Carolina": ["South Carolina", "SC"],
    "South Dakota": ["South Dakota", "SD"],
    "Tennessee": ["Tennessee", "TN"],
    "Texas": ["Texas", "TX", "Houston"],
    "Utah": ["Utah", "UT"],
    "Vermont": ["Vermont", "VT"],
    "Virginia": ["Virginia", "VA"],
    "Washington": ["Washington", "WA"],
    "West Virginia": ["West Virginia", "WV"],
    "Wisconsin": ["Wisconsin", "WI"],
    "Wyoming": ["Wyoming", "WY"]
}

class StateMatcher(object):
    def __init__(self, state, psuedonyms):
        self.state = state
        self.psuedonyms = psuedonyms

    def get_state(self):
        return self.state

    def __eq__(self, other):
        if not isinstance(other, str):
            return False

        for ps in self.psuedonyms:
            if re.search(ps, other, re.IGNORECASE):
                return True

        return False


states_list = []
for key, value in states_psuedonym.items():
    sm = StateMatcher(key, value)
    states_list.append(sm)