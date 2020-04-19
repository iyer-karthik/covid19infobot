from collections import defaultdict
import requests, json, math
from requests.exceptions import ConnectionError
import logging
from datetime import date

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from utils import CaseAgnosticDict


# Set up logging
logging.basicConfig(filename='../covidbot.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO
                    )
logger = logging.getLogger(__name__)


class COVIDInfoApi:
    """
    Class for fetching live and historical information about COVID-19
    cases from https://covid19api.com. Currently only fetches information
    at the country level. 

    Attributes
    ----------
    country_slug: A dictionary with with values that represent the country
        code that are compatible with the API call. Keys of the dictionary
        represent commonly used ways of referring to the country

            self.country_slug["us"] == "united-states" # True
            self.country_slug["united states"] = "united-states" # True
            self.country_slug["usa"] == "united-states" # True
            self.country_slug["france"] == "france" # True
    """
    def __init__(self):
        self.country_slug = defaultdict(lambda: "")

        try:
            r = requests.get('https://api.covid19api.com/countries')
            if r.status_code == 200:
                for country in r.json()[1:]:
                    self.country_slug[country['Country']] = country['Slug']
                self.country_slug = CaseAgnosticDict(self.country_slug)

            # Hard-coding (alternate) country names
            self.country_slug['congo b'] = 'congo-brazzaville'
            self.country_slug['congo brazzaville'] = 'congo-brazaville'
            self.country_slug['palestine'] = 'palestine'
            self.country_slug['palestinian'] = 'palestine'
            self.country_slug['sao tome'] = 'sao-tome-and-principe'
            self.country_slug['british indian ocean'] = 'british-indian-ocean-territory'
            self.country_slug['uae']  = 'united-arab-emirates'
            self.country_slug['falkland islands malvinas'] = 'falkland-islands-malvinas'
            #self.country_slug['saint martin french part'] = 'saint-martin-french-part'
            #self.country_slug['saint martin french'] = 'saint-martin-french-part'
            self.country_slug['holy see vatican city state'] = 'holy-see-vatican-city-state'
            self.country_slug['vatican city'] = 'holy-see-vatican-city-state'
            self.country_slug['vatican'] = 'holy-see-vatican-city-state'
            self.country_slug['cote divoire'] = 'cote-divoire'
            self.country_slug['iran'] = 'iran'
            self.country_slug['macedonia'] = 'macedonia'
            self.country_slug['cocos keeling islands'] = 'cocos-keeling-islands'
            self.country_slug['uk'] = 'united-kingdom'
            self.country_slug['congo kinshasa'] = 'congo-kinshasa'
            self.country_slug['congo k'] = 'congo-kinshasa'
            self.country_slug['united states'] = 'united-states'
            self.country_slug['us'] = 'united-states'
            self.country_slug['usa'] = 'united-states'
            self.country_slug['guinea bissau'] = 'guinea-bissau'
            self.country_slug['syria'] = 'syria'
            #self.country_slug['north korea'] = 'korea-north'
            self.country_slug['venezuela'] = 'venezuela'
            self.country_slug['timor leste'] = 'timor-leste'
            self.country_slug['south korea'] = 'korea-south'
            self.country_slug['vietnam'] = 'vietnam'
            self.country_slug['us virgin islands'] = 'virgin-islands'
            self.country_slug['macao'] = 'macao-sar-china'
            self.country_slug['hong kong'] = 'hong-kong-sar-china'
            self.country_slug['hk'] = 'hong-kong-sar-china'
            self.country_slug['saint-barthelemy'] = 'saint-barthélemy'
            self.country_slug['barthelemy'] = 'saint-barthélemy'
            self.country_slug['micronesia'] = 'micronesia'

        except ConnectionError as e:
            logger.error(e)
    

    def get_live_country_info(self, country, status):
        """
        Get live COVID-19 info from https://covid19api.com
        
        Parameters
        ----------
        country : str
            country code that is compatible with the API call.
            (for a list of country codes that are compatible, look at 
            self.country_slug.values())
        status : str
            one of "confirmed", "recovered", "deaths"
        
        Returns
        -------
        (str): Latest information about the number of cases for the country 
            according to the `status`   
        
        Raises
        ------
        ConnectionError
        """        

        try:
            r = requests.get('https://api.covid19api.com/total/country/' + country + '/status/' + status)
            if r.status_code == 200:
                info = json.loads(r.text)[-1]
                if status == 'deaths':
                    live_status = "Total number of {} in {} as of {} is {}\n".format(status,
                                                                                     country.upper(),
                                                                                     str(date.today()),
                                                                                     str(info['Cases']))
                else:
                    live_status = "Total number of {} cases in {} as of {} is {}\n".format(status,
                                                                                           country.upper(),
                                                                                           str(date.today()),
                                                                                           str(info['Cases']))
                return live_status
        except ConnectionError as e:
            logger.error(e)

   
    def __get_country_cumulative_info(self, countries, status):
        """
        Internal helper method that gets the cumulative history of the 
        cases in the specified list of countries. If status is one of "confirmed",
        "deaths" or "recovered" the function gets the cumulative history for only
        those statuses. If status is "all" cumulative history is fetched for all
        the statuses.
        
        Parameters
        ----------
        countries : [str]
            List of countries with formatted names that are consistent with API call
        status : str
            One of "confirmed", "recovered", "deaths", "all"
        
        Returns
        -------
        cases, dates: (List, List)
            Cumulative history with number of cases for every recorded date

        Raises
        ------
        ConnectionError    
        """        
        cases = [[],[],[]]
        dates = [[],[],[]]

        if (status == 'all'):
            status_list = ['confirmed','recovered','deaths']
            status_index = [0, 1, 2]
        else:
            status_list = [status]
            if (status == 'confirmed'):
                status_index = [0]
            elif (status == 'recovered'):
                status_index = [1]
            else:
                status_index = [2]
        
        # Fetch cumulative history
        try:
            for i in range(len(status_list)):
                for country in countries:
                    r = requests.get(
                        'https://api.covid19api.com/total/country/' + country + '/status/' + status_list[i])
                    
                    if r.status_code == 200:
                        cases[status_index[i]].append([day_info['Cases'] 
                                                    for day_info in r.json()])

                        dates[status_index[i]].append([date.fromisoformat(day_info['Date'].split('T')[0]) 
                                                    for day_info in r.json()])
            if status == 'all':
                return cases, dates
            else:
                return cases[status_index[0]], dates[status_index[0]]
        
        except ConnectionError as e:
            logger.error(e)


    def compare_country_plot(self, countries, status, log_scale=False):
        """
        Plots number of cases for the list of countries  If status is one of "confirmed",
        "deaths" or "recovered"  cumulative history for only those statuses is plotted.
        If status is "all" cumulative history is plotted for all
        the statuses.

        Parameters
        ----------
        countries : [str]
            List of countries with formatted names that are consistent with API call
        status : str
            One of "confirmed", "recovered", "deaths", "all"
        log_scale: bool
            If True plots the numbers on a log scale
        
        Returns
        -------
        matplotlib.figure.Figure
        """
        cases, dates = self.__get_country_cumulative_info(countries, status)

        # Plotting
        num_countries = len(countries)
        subplots = math.ceil(num_countries / 3)
        grid_x = math.ceil(subplots / 3)
        if (subplots <= 2):
            grid_y = subplots
        else:
            grid_y = 3

        fig, axs = plt.subplots(grid_x, grid_y, squeeze=False, 
                               figsize=(14, 12), linewidth=1)
        for i in range(grid_x):
            for j in range(grid_y):
                if (status != 'all'):
                    if (9 * i + 3 * j < num_countries):
                        axs[i, j].plot(dates[9 * i + 3 * j],
                                       cases[9 * i + 3 * j],
                                       label=countries[9 * i + 3 * j].upper()+' ('+status+')')
                    if (9 * i + 3 * j + 1 < num_countries):
                        axs[i, j].plot(dates[9 * i + 3 * j + 1],
                                       cases[9 * i + 3 * j + 1],
                                       label=countries[9 * i + 3 * j + 1].upper()+' ('+status+')')
                    if (9 * i + 3 * j + 2 < num_countries):
                        axs[i, j].plot(dates[9 * i + 3 * j + 2],
                                       cases[9 * i + 3 * j + 2],
                                       label=countries[9 * i + 3 * j + 2].upper()+' ('+status+')')
                else:
                    status_list = ['confirmed','recovered','deaths']
                    if (9 * i + 3 * j < num_countries):
                        for a in range(len(status_list)):
                            axs[i, j].plot(dates[a][9 * i + 3 * j],
                                           cases[a][9 * i + 3 * j],
                                           marker='+',
                                           linewidth=2,
                                           label=countries[9 * i + 3 * j].upper()+' ('+status_list[a]+')',
                                           )
                    if (9 * i + 3 * j + 1 < num_countries):
                        for a in range(len(status_list)):
                            axs[i, j].plot(dates[a][9 * i + 3 * j + 1],
                                           cases[a][9 * i + 3 * j + 1],
                                           'o',
                                           label=countries[9 * i + 3 * j + 1].upper()+' ('+status_list[a]+')')
                    if (9 * i + 3 * j + 2 < num_countries):
                        for a in range(len(status_list)):
                            axs[i, j].plot(dates[a][9 * i + 3 * j + 2],
                                           cases[a][9 * i + 3 * j + 2],
                                           linewidth=2,
                                           label=countries[9 * i + 3 * j + 2].upper()+' ('+status_list[a]+')')

                axs[i, j].legend()
                if log_scale:
                    axs[i, j].set_yscale("log")

        fig.suptitle("Number of COVID-19 cases")
        fig.autofmt_xdate()
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        return plt.gcf()