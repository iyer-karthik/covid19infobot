# Slack info bot for COVID 19

## Introduction
A lightweight interactive bot for COVID 19 information developed by [iyer-karthik](https://github.com/iyer-karthik) and [srk2siva](https://github.com/srk2siva).

The bot can also answer questions on symptoms, prevention methods, vaccination or method of spread for COVID-19.

Additionally the bot can also get the number of confirmed or recovered cases or deaths due to COVID-19 in different countries with an additional functionality of plotting the results in a graph.
 
Here's a demo. 

![screenshot](../master//images/screenshot-bot.gif)

## Table of contents
1. [ How it works? ](#works)
2. [ How to register a Slack bot?](#register)
3. [ How to run the bot?](#run)
4. [ How to host the bot?](#host)

<a name="works"></a>
### How it works? 
The back-end of the bot is fairly straightforward. 

The intent of a chat is parsed through a bunch of regexes. Pre-set responses are delivered for most of the 
requests. Currently there is no NLP involved. 

For questions related to the number of cases for different countries, an API call is made 
to https://covid19api.com, results are formatted and if asked, a matplotlib plot is created, 
and these are then served in the response. Results are updated every hour.

<a name="register"></a>
### How to register a Slack bot?
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

<a name="run"></a>
### How to run the bot?
1. Once a bot is registered and a token created, clone this repository\
`git clone https://github.com/iyer-karthik/covid19infobot` 
https://github.com/iyer-karthik/
2. Create a virtual environment in Python 3.7 and activate it. cd into the folder for the repository and run\
`pip install -r requirements.txt`

3. Finally run `main.py YOUR-BOT-TOKEN`\
(Use your Bot User OAuth Access Token.)
The bot is now activated and you can interact with it. 


<a name="host"></a>
Since the main script always needs to be running in order for the bot to be used, it is better
to migrate the running to the cloud. We will use Amazon Web Service's free EC2 instance to
host this script and keep it continually running. 

1. Follow the steps outlined in this [tutorial](https://towardsdatascience.com/deploying-a-python-web-app-on-aws-57ed772b2319) to launch an EC2 instance and SSH into it. 
We used an Ubuntu Server 18.04 AMI. 

2. This AMI comes equipped with Python 3.6. However we need Python 3.7 to run the bot. 

3. Follow the steps outlined in this [blog](https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/) to install Python 3.7 on the EC2 instance. 

4. Install pip for python 3.7 with \
`python3.7 -m pip install pip`. If the Python 3.7 
install is missing pip you could try installing it using: `python3.7 -m ensurepip`

5. Now get this repository using \
`git clone https://github.com/iyer-karthik/covid19infobot.git`

6. Move into the repository and run\
 `python3.7 -m pip install -r requirements.txt`

7. Finally run `python 3.7 main.py YOUR-BOT-TOKEN`

8. If you want the script to keep running even after you log out of the instance, run it in a Screen session

```
# From within the repository folder
screen -R deploy
python3.7 main.py YOUR-BOT-TOKEN
```


 




