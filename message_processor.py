import re
from functools import reduce


class MessageProcessor(object):
    """
    A simple class to process a text and extract relevant information from a text. 
    Intended for downstream tasks for the COVID-19 info bot. 
    
    Currently the following information can be extracted from a text:
        1. List of countries in the text and status intent ((confirmed/ recovered/ deaths))
        2. Whether the message talks about plotting (plotting happens only if a country
        name and status intent is detected in the text.)
        3. Whether the message talks about `you/ yourself`. (Intended for when a user
        asks the bot to describe or talk about itself.)
        4. Whether the message contains `bye/ goodbye`. (Intended for when a user
        bids goodbye to the bot.) 
        5. Whether the message is talking about the symptoms of the virus. 
        6. Whether the message is talking about the spread of the virus.
        7. Whether the message is talking about treatment or vaccination for the virus.
        8. Whether the message is talking about prevention or stopping the spread of the virus. 
        9. Whether the message contains 'thanks/ thank you'.
    """
    def __init__(self, api_object):
        self.api_object = api_object

    def process(self, message) -> dict:
        """
        Extracts relevant information from a text and outputs a dictionary that
        is then formatted for output before being posted in a Slack channel. 

        Parameters
        ----------
        message (str): 
            Some text that is used as an input by the Covid-19 info bot
        
        Returns
        --------
        dict (dict):
            A dictionary with relevant information extracted from the message.
            Dictionary has the following format
            {
            "countries_detected": [list_of_countries_extracted_from_the_text],
            "status_detected": one of "confirmed"/ "deaths"/ "recovered", 
            "talking_about_plot": bool, 
            "talking_about_yourself": bool, 
            "talking_about_bye": bool, 
            "talking_about_symptoms": bool, 
            "talking_about_spread": bool, 
            "talking_about_vaccine": bool, 
            "talking_about_prevention": bool, 
            "talking_about_thanks": bool
            }
        """
        message = message.lower()

        # Extract list of countries from the message. Some country names are 
        # seperated by spaces. To get those country names, do a n-gram scan (n=2,3,4)
        # of the message. We stop at n=4 since all country names are atmost 4 words
        # in length.
        extracted_countries = [token for token in re.split("(\W+|\,+)", message) 
                              if token in self.api_object.country_slug]
        extracted_countries += self.__ngram_countries(message) 
        print(extracted_countries)

        # Since we have a many-to-one mapping of the country names to country codes,
        # extract only the unique country codes
        extracted_country_codes = list(set([self.api_object.country_slug[k]
                                           for k in extracted_countries]))

        extracted_status = self._get_status(message)

        return {"countries_detected":  extracted_country_codes,

                "status_detected": extracted_status,

                "talking_about_plot": bool(re.search(r'(plot|figure|chart|image)', 
                                                     message)),

                "talking_about_yourself": bool(re.search(r'(\byourself\b|\byou\b\s\bdo\b)', 
                                               message)),

                "talking_about_bye":  bool(re.search(r'(\bbye\b|\bgoodbye\b)', 
                                           message)),

                "talking_about_symptoms": bool(re.search(r'symptoms?[\s\S]*(virus|coronavirus|covid)?',
                                               message)),

                "talking_about_spread": bool(re.search(r'(virus|covid)?[\s\S]*spreads?', 
                                                       message)),

                "talking_about_vaccine": bool(re.search(r'(vaccin|drugs?|treatment|cure)', 
                                                        message)),
                
                "talking_about_prevention": bool(re.search(r'(prevent|stop)[\s\S]*', 
                                                           message)),

                "talking_about_thanks": bool(re.search(r'(thanks|thank\syou)', message))
                }
 

    def __ngram_countries(self, message):

        def ngrams(word_list, n):
            return [" ".join(word_list[i:i+n]) for i in range(len(word_list) - n + 1)]
        word_list = message.split(" ")

        all_ngrams = ngrams(word_list, n=2) + ngrams(word_list, n=3) + ngrams(word_list, n=4)
       
        # Remove all non-unicode characters and possible , in the words
        cleaned_all_ngrams = [re.sub(",", "", re.sub('(?![ -~]).', '', token)) 
                              for token in all_ngrams]

        return [token for token in cleaned_all_ngrams if token in self.api_object.country_slug]

    def _get_status(self, message):
        
        __confirm_regex = r'(confirm|confrim|verify|verifi)(s|ed)?'
        __recover_regex = r'(recover)(s|ed)?'
        __death_regex = r'(die|died|death|deaths)'

        if re.search(__confirm_regex, message):
            return "confirmed"

        if re.search(__recover_regex, message):
            return "recovered"
        
        if re.search(__death_regex, message):
            return "deaths"