import re
import os
import json
import random

import datetime
import requests
import time

from flask import Flask, request, Response


application = Flask(__name__)

# FILL THESE IN WITH YOUR INFO
my_bot_name = 'ank_bot' #e.g. zac_bot
my_slack_username = 'ankitparekh' #e.g. zac.wentzell


slack_inbound_url = 'https://hooks.slack.com/services/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'


# this handles POST requests sent to your server at SERVERIP:41953/slack
@application.route('/slack', methods=['POST'])
def inbound():
    # Adding a delay so that all bots don't answer at once (could overload the API).
    # This will randomly choose a value between 0 and 10 using a uniform distribution.
    #delay = random.uniform(0, 10)
    #time.sleep(delay)

    print '========POST REQUEST @ /slack========='
    response = {"username": "ank_bot", "icon_url": "http://images.zaazu.com/img/Wolverine-Wolverine-X-men-Logan-smiley-emoticon-001162-medium.gif", "text": ""}
    print 'FORM DATA RECEIVED IS:'
    print request.form

    channel = request.form.get('channel_name') #this is the channel name where the message was sent from
    username = request.form.get('user_name') #this is the username of the person who sent the message
    text = request.form.get('text') #this is the text of the message that was sent
    d=True;
    b=len(re.findall(r"\[([A-Za-z0-9_]+)\]", text))
    c="I_NEED_HELP_WITH_CODING" in text
    d="WHAT'S_THE_WEATHER_LIKE_AT" in text
    a=c or d or text=="&lt;BOTS_RESPOND&gt;"
    ab=not(a)
    now = datetime.datetime.now()
    date = now.strftime("%d-%b-%Y %H:%M")
    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message

    if username in [my_slack_username, 'zac.wentzell']:
        # Your code for the assignment must stay within this if statement


        if c and b!=0:
            #d=False;
            m = re.findall(r"\[([A-Za-z0-9_]+)\]", text)
            temp = text.split(':')
            temp1 = temp[1].split('[')
            temp2=temp1[0]
            payload = {'order': 'desc', 'sort': 'relevance', 'q': temp2, 'accepted': 'True', 'answers': '0', 'tagged': [m[0], m[1]], 'views': '100', 'site': 'stackoverflow'}
            temp3 = requests.get('http://api.stackexchange.com/2.2/search/advanced', params=payload).json()
            #print temp3
            print 'task 3'
            #c=len(temp2['items'])
            for x in range(0, 5, 1):
                response={"username": "ank_bot", "icon_url": "http://images.zaazu.com/img/Wolverine-Wolverine-X-men-Logan-smiley-emoticon-001162-medium.gif","attachments": [{"fallback": "Required plain-text summary of the attachment.","color": "#36a64f","pretext": "Solutions","author_name": "StackOverflow","title": temp2,"title_link": temp3['items'][x]['link'],"text":str(x+1)+"Answer","footer": date,"footer_icon": "http://images.zaazu.com/img/hiro-hiro-nakamura-hero-smiley-emoticon-000382-medium.gif"}]}
                #response['text']= temp2['items'][x]['link']
                r = requests.post(slack_inbound_url, json=response)

        if c and b==0:
            #d=False
            temp = text.split(':')
            temp1 = temp[1]
            payload = {'order': 'desc', 'sort': 'relevance', 'q': temp1, 'accepted': 'True', 'answers': '0', 'views': '100', 'site': 'stackoverflow'}
            temp2 = requests.get('http://api.stackexchange.com/2.2/search/advanced', params=payload).json()
            #print temp2
            print 'task 2'
            for x in range(0, 5, 1):
                response={"username": "ank_bot", "icon_url": "http://images.zaazu.com/img/Wolverine-Wolverine-X-men-Logan-smiley-emoticon-001162-medium.gif", "attachments": [{"fallback": "Required plain-text summary of the attachment.","color": "#36a64f","pretext": "Solutions","author_name": "StackOverflow","title": temp1,"title_link": temp2['items'][x]['link'],"text":str(x+1)+"Answer","footer": date,"footer_icon": "http://images.zaazu.com/img/hiro-hiro-nakamura-hero-smiley-emoticon-000382-medium.gif"}]}
                #response['text']= temp2['items'][x]['link']
                r = requests.post(slack_inbound_url, json=response)


        if "WHAT'S_THE_WEATHER_LIKE_AT" in text :
            temp=text.split(':')[1]
            numbers=re.findall(r'\b\d+\b', text)
            digits=len(numbers[0])
            if digits==5:
                payload = {'zip': temp+",us", 'appid': '2025dd8c5b03edf26f663ce21b376667'}
                t = requests.get('http://api.openweathermap.org/data/2.5/weather', params=payload).json()
                #print t
                print 'task4 zip wala'
                main=t['weather'][0]['main']
                des=t['weather'][0]['description']
                ctemp=str(t['main']['temp'])+"F"
                tmax=str(t['main']['temp_min'])+"F"
                tmin=str(t['main']['temp_max'])+"F"
                hum=str(t['main']['humidity'])+"%"
                pres=str(t['main']['pressure'])+"pasc"
                win=str(t['wind']['speed'])+"km/hr"
                gus=str(t['wind']['gust'])+"."
                response={"username": "ank_bot", "icon_url": "http://images.zaazu.com/img/Wolverine-Wolverine-X-men-Logan-smiley-emoticon-001162-medium.gif","attachments": [{"fallback": "Required plain-text summary of the attachment.","color": "#36a64f","pretext": "Todays Weather be like","author_name": main,"title": "Weather updates","title_link": "http://www.accuweather.com/en/world-weather","text": des,"fields": [{"title": "Current Temperature","value": ctemp,"short": "false"},{"title": "Max","value": tmax,"short": "true"},{"title": "Min","value": tmin,"short": "false"},{"title": "Humidity","value": hum,"short": "true"},{"title": "Pressure","value": pres,"short": "true"},{"title": "Wind","value": win,"short": "true"	},{"title": "Gust","value": gus,"short": "true"}],"footer": date,"footer_icon": "http://images.zaazu.com/img/Relax-relax-rest-cool-smiley-emoticon-000628-medium.gif"}]}
            else:
                temp2=temp.split(',')[1]
                payload = {'q': temp+",us", 'appid': '2025dd8c5b03edf26f663ce21b376667'}
                t = requests.get('http://api.openweathermap.org/data/2.5/weather', params=payload).json()
                #print t
                print 'task4 not zip'
                main=t['weather'][0]['main']
                des=t['weather'][0]['description']
                ctemp=str(t['main']['temp'])+"F"
                tmax=str(t['main']['temp_min'])+"F"
                tmin=str(t['main']['temp_max'])+"F"
                hum=str(t['main']['humidity'])+"%"
                pres=str(t['main']['pressure'])+"pasc"
                win=str(t['wind']['speed'])+"km/hr"
                gus=str(t['wind']['gust'])+"."
                response={"username": "ank_bot", "icon_url": "http://images.zaazu.com/img/Wolverine-Wolverine-X-men-Logan-smiley-emoticon-001162-medium.gif","attachments": [{"fallback": "Required plain-text summary of the attachment.","color": "#36a64f","pretext": "Todays Weather be like","author_name": main,"title": "Weather updates","title_link": "http://www.accuweather.com/en/world-weather","text": des,"fields": [{"title": "Current Temperature","value": ctemp,"short": "false"},{"title": "Max","value": tmax,"short": "true"},{"title": "Min","value": tmin,"short": "false"},{"title": "Humidity","value": hum,"short": "true"},{"title": "Pressure","value": pres,"short": "true"},{"title": "Wind","value": win,"short": "true"	},{"title": "Gust","value": gus,"short": "true"}],"footer": date,"footer_icon": "http://images.zaazu.com/img/Relax-relax-rest-cool-smiley-emoticon-000628-medium.gif"}]}



#"attachments": [{"fallback": "Required plain-text summary of the attachment.","color": "#36a64f","pretext": "Requested Weather conditions","author_name": "Ankit","title": "Weather updates","title_link": "https://api.slack.com/","text": "","fields": [{"title": "Temperature","value": "temp","short": false}],"footer": "ANK_BOT","footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png","ts": 123456789}]








        # A sample response:
        if text == "&lt;BOTS_RESPOND&gt;":
        # you can use print statments to debug your code
            print 'Bot is responding to favorite color question'
            response['text'] = 'Hello, my name is ank_bot. I belong to ankitparekh. I live at 50.112.200.232'
            print 'Response text set correctly'
            print response['text']
            print b,c,
            r = requests.post(slack_inbound_url, json=response)

        if slack_inbound_url and ab :
            response['text'] = 'Sorry cannot understand what you saying. Wrong input..!'
            r = requests.post(slack_inbound_url, json=response)
            print b,c
    print '========REQUEST HANDLING COMPLETE========\n\n'

    return Response(), 200


# this handles GET requests sent to your server at SERVERIP:41953/
@application.route('/', methods=['GET'])
def test():
    return Response('Your flask app is running!...')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)
