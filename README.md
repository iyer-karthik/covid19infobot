# Slack info bot for COVID 19

## Introduction
A simple interactive bot for COVID 19 information. 

The bot is programmed to answer the number of confirmed or recovered cases or deaths due to COVID-19 in different countries with an additional functionaility of plotting the results in a graph. 
 
The bot can also answer questions on symptoms, prevention methods, vaccination or method of spread for COVID-19.

## How it works? 
The back-end of the bot is fairly straightforward. 

The intent of a chat is parsed through a bunch of regexes. Pre-set responses are delivered for most of the 
requests. Currently there is no NLP involved. 

For questions related to the number of cases for different countries, an API call is made 
to https://covid19api.com, results are formatted and if asked, a matplotlib plot is created, 
and these are then served in the response.

## How to register a Slack bot?
1. To use this bot please ensure that you create a classic slack app (https://api.slack.com/rtm#classic).
Since new Slack apps don't connect to `rtm.connect`, you'll need to have a classic Slack app to get started.

2. Give it a name and add it to a development workspace. 
![Step2](../master//images/Step2.png)


3. Select Bots - Add a bot to allow users to exchange messages with your app.\
![Step3](../master//images/Step3.png)

4. Add a legacy bot user.\
![Step4](../master//images/Step4.png)

5. Give it a user name and a default user name.\
![Step5](../master//images/Step5.png)

6. (Optional) Under "App Home" under "Features" Select Always Show My Bot as Online. When this is off, Slack automatically displays whether your bot is online based on usage of the RTM API.\
![Step6](../master//images/Step6.png)

7. Under Settings, click on "Install App" and select "Install App to workplace" and then click "Allow".\
![Step7](../master//images/Step7.png)

8. Go back to "Install App" under Settings. You should see a Bot User OAuth Access Token - a string that starts with 'xoxb'. Save this token.

## How to use this bot?
1. Once a bot is registered and a token created, clone this repository\
`git clone https://github.com/iyer-karthik/covid19infobot` 

2. Create a virtual environment and activate it. cd into the folder for the repository and run\
`pip install -r requirements.txt`

3. Finally run `main.py bot_token`\
(Substitute bot_token with your Bot User OAuth Access Token.)

 




