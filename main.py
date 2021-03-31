import discord

import requests
import json
import random
from dotenv import load_dotenv
import os 
from keep_alive import keep_alive
load_dotenv()
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  

client = discord.Client()
analyzer = SentimentIntensityAnalyzer()

# GIF
def get_quote(com):
  search = "https://g.tenor.com/v1/search?q="
  search2 = "&key=FE8D3GPUMIAH&limit=10"
  search = search + com + search2
  response = requests.get(search)
  json_data = json.loads(response.text)
  quote_random = random.randint(0,9)
  a = json_data["results"][quote_random]["media"][0]["mediumgif"]["url"]
  return a

def sentiment_analyzer_scores(text):
	score = analyzer.polarity_scores(text)
	lb = score['compound']
	if lb >= 0.05:
		return 'positive'
	elif (lb > -0.05) and (lb < 0.05):
		return 'neutral'
	else:
		return 'negative'

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  if msg.startswith('$gif'):
    com = msg
    com = com[:20]
    com = com.strip("$gif")
    com = com.replace(" ","")
    print(com)
    quote = get_quote(com)
    await message.channel.send(quote) 
  sentiment = sentiment_analyzer_scores(msg)
  await message.channel.send('The sentiment of your text is ' + str(sentiment))


keep_alive()
client.run(os.getenv('TOKEN'))
