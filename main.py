from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
birthday1 = os.environ['BIRTHDAY1']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id1 = os.environ["USER_ID1"]
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
template_id1 = os.environ["TEMPLATE_ID1"]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days + 1

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday1():
  next = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_words1():
  words1 = requests.get("https://api.shadiao.pro/du")
  if words1.status_code != 200:
    return get_words1()
  return words1.json()['data']['text']


def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"city":{"value":city , "color":'#98FB98'},"temperature":{"value":temperature , "color":'#DB7093'},"love_days":{"value":get_count() , "color":'#FFB6C1'},"birthday_left":{"value":get_birthday(),"color":'#1E90FF'},"birthday_right":{"value":get_birthday1(),"color":'#1E90FF'},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res1 = wm.send_template(user_id1, template_id, data)
print(res)
data1 = {"words1":{"value":get_words1() , "color":get_random_color()}}
res2 = wm.send_template(user_id, template_id1, data1)
res3 = wm.send_template(user_id1, template_id1, data1)
print(res1)
