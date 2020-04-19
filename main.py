from message_processor import MessageProcessor
from output_formatter import _OutputFormatter
from covid_info_api import COVIDInfoApi

import re
import tempfile
import os
import logging
import time 
import argparse

import slack
from slack.errors import SlackApiError
from slack.rtm.client import RTMClient
from slack.web.client import WebClient

# The next two lines are to address python event loop runtime error
import nest_asyncio
nest_asyncio.apply()

# Set up logging
logging.basicConfig(filename='../covidbot.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO
                            )
logger = logging.getLogger(__name__)


@RTMClient.run_on(event='message')
def msg_detected(**payload):
    logger.info(payload)
    data = payload['data']

    message_text = (data['text'].lower())  # make all text lower to simplify pattern matching
    channel_id = data['channel']
    webclient = payload['web_client']

    # check if the message event is from the bot
    if list(data)[0] == 'subtype':
        logger.info('message from bot, ignoring message')
        return

    # check if this is just a general message or a DM to the bot
    if bot_id not in message_text:
        logger.info('Not a DM to the bot. Ingorning the message')
        return

    processed_message_details = msg_processor.process(message_text)
    print(processed_message_details)
    logger.info("Processed message details")
    logger.info(processed_message_details)

    if re.search(r'(\bhi\b|\bhello\b)', message_text):
        user = data['user']
        webclient.chat_postMessage(
            channel=channel_id,
            text="Hello <@{}>!".format(user),
        )
    
    if re.search(r'(are\syou(\sdo)?|is\sit\sgo)', message_text):
        webclient.chat_postMessage(
            channel=channel_id,
            text="Doing good. How about yourself?",
        )
    if processed_message_details.get('countries_detected')!= []:
        webclient.chat_postMessage(
            channel=channel_id,
            text= "Fetching results. Give me a few seconds...",
        )

        response, plot = _output_formatter._format_for_status_updates(processed_message_details, api_object)

        webclient.chat_postMessage(
            channel=channel_id,
            text= response
        )

        if plot is not None:
            with tempfile.TemporaryDirectory() as tmpdirname:
                full_path = os.path.join(tmpdirname, 'plot.png')
                plot.savefig(full_path)
                with open(full_path, 'rb') as att:
                    r = webclient.api_call("files.upload", files={
                        'file': att,
                            }, data={
                        'channels': channel_id,
                        'filename': 'downloaded_filename.jpeg',
                        'title': 'Requested plot',
                        'initial_comment': 'Requested plot'
                    })
            assert os.path.exists(full_path) == False # temp directory must be deleted outside 
                                                      # context manager

    if processed_message_details.get('talking_about_symptoms'): 
        time.sleep(_pause_for_seconds_before_reply)
        webclient.chat_postMessage(
            channel=channel_id,
            text=_output_formatter._format_for_symptoms(),
        )
    
    if processed_message_details.get('talking_about_spread'):
        time.sleep(_pause_for_seconds_before_reply)
        webclient.chat_postMessage(
            channel=channel_id,
            text=_output_formatter._format_for_spread(),
        )
    
    if processed_message_details.get('talking_about_vaccine'):
        time.sleep(_pause_for_seconds_before_reply)
        webclient.chat_postMessage(
            channel=channel_id,
            text=_output_formatter._format_for_vaccine(),
        )

    if processed_message_details.get('talking_about_prevention'):
        time.sleep(_pause_for_seconds_before_reply)
        webclient.chat_postMessage(
            channel=channel_id,
            text= _output_formatter._format_for_prevention(),
        )

    if processed_message_details.get('talking_about_thanks'):
        time.sleep(_pause_for_seconds_before_reply)
        webclient.chat_postMessage(
            channel=channel_id,
            text=_output_formatter._format_for_thanks(),
        )
    if processed_message_details.get('talking_about_yourself'):
        webclient.chat_postMessage(
            channel=channel_id,
            text=_output_formatter._format_for_introduction(),
        )
    if processed_message_details.get('talking_about_bye'):
        time.sleep(_pause_for_seconds_before_reply)
        webclient.chat_postMessage(
            channel=channel_id,
            text=_output_formatter._format_for_bye(),
        )
        
    if not any(bool(e) for e in processed_message_details.values()) and\
         re.search(r'(\bhi\b|\bhello\b)', message_text) is None and\
         re.search(r'(are\syou(\sdo)?|is\sit\sgo)', message_text) is None:
        time.sleep(_pause_for_seconds_before_reply)
        webclient.chat_postMessage(
            channel=channel_id,
            text=_output_formatter._format_default_response(),
        )     

if __name__ =="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("bot_token", 
                        type=str,
                        help="use the bot token to connect the bot. This token can be found " +\
                             "under Bot User OAuth Access Token tab of `OAuth and Permissions` " +\
                             "page of your bot. The bot token will start with an 'xoxb-'")
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(filename='../covidbot.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO
                        )

    logger = logging.getLogger(__name__)

    # Initialize the message processing and ouput 
    api_object = COVIDInfoApi()
    msg_processor = MessageProcessor(api_object)
    _output_formatter = _OutputFormatter()
    _pause_for_seconds_before_reply = 1

    # Initialize the proper slack clients
    try:
        slack_bot_token = args.bot_token
        rtmclient = RTMClient(token=slack_bot_token, connect_method='rtm.start', auto_reconnect=True)
        web_client = WebClient(slack_bot_token, timeout=30) # Used for posting messages
        bot_id = (web_client.api_call("auth.test")["user_id"].lower())
    except (SlackApiError, TypeError) as e:
        logger.error(e)

    # Start the client
    rtmclient.start()



# TODO: Add video of slack bot in README and details
# on deployment