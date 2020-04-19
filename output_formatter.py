from covid_info_api import COVIDInfoApi
import requests
import json


class _OutputFormatter:
    """
    A simple internal class to format output response for a given message for the 
    Covid-19 info bot. 
    """
    def __init__(self):
        pass

    def _format_for_status_updates(self, processed_message_details, api_object):
        """
        Format output response if country names are detected in the message to
        the bot. 
        
        Parameters
        ----------
        processed_message_details : dict
            A dictionary that is the output of `MessageProcessor.process()` method
            
        api_object : API
            [description]
        
        Returns
        -------
        response, plot: (str, figure object/ None)
            response: Properly formatted response for when the message to the bot
                contains names of countries
            plot: Matplotlib figure object that plots the number of confirmed/ recovered/ deaths
                cases for the list of countries detected in the message. Plotting happens
                only if the plotting trigger words are detected in the message. 
                Defaults to None otherwise. 
        """        
        response = ""
        plot = None

        # Detect status intent. Defaults to "all"
        _status_detected = processed_message_details.get('status_detected') or "all"

        if _status_detected == "all":
            _complete_status_list = ["confirmed", "recovered", "deaths"]
        else:
            _complete_status_list = [_status_detected]
        
        for country in processed_message_details.get('countries_detected'):
            for _status in _complete_status_list:
                response += api_object.get_live_country_info(country, _status)

        if processed_message_details["talking_about_plot"]:
            plot = api_object.compare_country_plot(
                                countries=processed_message_details.get('countries_detected'), 
                                status=_status_detected
                                )

        return response, plot

    def _format_for_symptoms(self):
        response = "Symptoms:\nThe most common symptoms of COVID-19 are fever, tiredness, and dry cough. " +\
        "Some patients may have aches and pains, nasal congestion, runny nose, sore throat or diarrhea.\n" +\
        "\nThese symptoms are usually mild and begin gradually. Some people become infected but don’t develop " +\
        "any symptoms and don't feel unwell.\nMost people (about 80%) recover from the disease without needing" +\
        "special treatment.\n\nAround 1 out of every 6 people who gets COVID-19 becomes seriously ill and " +\
        "develops difficulty breathing.\nOlder people, and those with underlying medical problems like " +\
        "high blood pressure, heart problems or diabetes, are more likely to develop serious illness. " +\
        "\nPeople with fever, cough and difficulty breathing should seek medical attention."
        return response

    def _format_for_spread(self):
        response = "Spreading mechanism:\nPeople can catch COVID-19 from others who have the virus. " +\
            "The disease can spread from person to person through small droplets from the nose or mouth " +\
            "which are spread when a person with COVID-19 coughs or exhales.\n\nThese droplets land on objects "+\
            "and surfaces around the person. Other people then catch COVID-19 by touching these objects or "+\
            "surfaces, then touching their eyes, nose or mouth.\n\nPeople can also catch COVID-19 if they breathe "+\
            "in droplets from a person with COVID-19 who coughs out or exhales droplets. This is why it is "+\
            "important to stay more than 1 meter (3 feet) away from a person who is sick."
        return response
    
    def _format_for_vaccine(self):
        response = "Treatment:\nNot yet. To date, there is no vaccine and no specific antiviral medicine to " +\
        "prevent or treat COVID-2019.\n\nHowever, those affected should receive care to relieve symptoms. " +\
        "People with serious illness should be hospitalized. Most patients recover thanks to supportive care.\n" +\
        "Possible vaccines and some specific drug treatments are under investigation.\nThey are being tested through "+\
        "clinical trials. WHO is coordinating efforts to develop vaccines and medicines to prevent and treat COVID-19. "+\
        "\n\nThe most effective ways to protect yourself and others against COVID-19 are to frequently clean your hands, " +\
        "cover your cough with the bend of elbow or tissue, and maintain a distance of at least 1 meter (3 feet) from " +\
        "people who are coughing or sneezing."
        return response

    def _format_for_prevention(self):
        response = "DO THE FIVE and help stop coronavirus.\n\n" +\
                    "HANDS - Wash them often 🧼👐🚰\n" +\
                    "ELBOW - Cough into it ✅🤧💪\n" +\
                    "FACE - Don't touch it 🚫🤦\n" +\
                    "SPACE - Keep safe distance 🚫🧑‍🤝‍🧑\n"+\
                    "HOME - Stay if you can 🏠 \n" 
        return response

    def _format_for_thanks(self):
        response = " You're welcome!🙂 "
        return response


    def _format_default_response(self):
        response = "I'm sorry, I do not understand your message 🙁 \n" +\
        "You can ask me about number of confirmed or recovered cases or deaths " +\
        "due to COVID-19 in different countries. You can also ask me to plot the results in a graph.\n" +\
        "Additionally, you can also ask me about symptoms, prevention methods, vaccination " +\
        "or method of spread for COVID-19.\n\n" +\
        "Here are some examples:\n" +\
        "`@covid19-info-bot Can you tell me the number of confirmed cases in US and Spain?`\n" +\
        "`@covid19-info-bot Can you tell me the number of deaths in China and Italy?`\n" +\
        "`@covid19-info-bot Can you plot the number of confirmed cases in Mexico and India?`" +\
        "`@covid19-info-bot How does the virus spread?`\n" +\
        "`@covid19-info-bot What are the symptoms?`\n" +\
        "`@covid19-info-bot How does one prevent the virus?`\n" +\
        "`@covid19-info-bot Has any vaccine been found so far for this virus?`\n"
        return response

    def _format_for_introduction(self):
        response = "Hi! I am covid-19-info bot 🙂 \n\n" +\
        "I will give you latest information about number of confirmed or recovered cases or deaths " +\
        "due to COVID-19 in different countries. You can also ask me to plot the results in a graph.\n\n" +\
        "Additionally, you can also ask me about symptoms, prevention methods, vaccination " +\
        "or method of spread for COVID-19.\n"
        return response
    
    def _format_for_bye(self):
        response = "Goodbye! Stay safe and stay home 🙂 "
        return response