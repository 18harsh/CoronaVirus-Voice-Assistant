from bs4 import BeautifulSoup
import requests
import re
import pandas
import pyttsx3
import speech_recognition as sr
from selenium import webdriver




def speak(text):
	engine = pyttsx3.init()
	engine.setProperty('rate',150)
	engine.setProperty('voice','en+m7')
	engine.say(text)
	engine.runAndWait()	

def get_audio():

	r=sr.Recognizer()
	print("Listening.....")
	with sr.Microphone() as source:
		audio = r.listen(source)
		said=""
		print("loading.....")
		try:
			said = r.recognize_google(audio)
			print(said)
		except Exception as e:
			print("Exception: "+str(e))

	return said.lower()		

def load_data():
	r = requests.get("https://news.google.com/covid19/map?hl=en-IN&gl=IN&ceid=IN%3Aen", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
	c = r.content
	soup = BeautifulSoup(c,"html.parser")
	l=[]
	d={}
	id = 0
	worldwide = soup.find("tr",{"class":"sgXwHf wdLSAe ROuVee"})
	d['ID'] = id
	d['Country'] = (worldwide.find("th",{"class":"l3HOY"}).text)
	d['Confirmed'] =(worldwide.find_all("td",{"class":"l3HOY"})[0].text)
	d['CPMP'] = (worldwide.find_all("td",{"class":"l3HOY"})[1].text)
	d['Recovered'] = (worldwide.find_all("td",{"class":"l3HOY"})[2].text)
	d['Death'] = (worldwide.find_all("td",{"class":"l3HOY"})[3].text)
	l.append(d)


	all = soup.find_all("tr",{"class":"sgXwHf wdLSAe YvL7re"})
	id +=1
	for item in all:
		d={}
		d['ID'] = id
		d['Country'] = (item.find("div",{"class":"pcAJd"}).text)
		d['Confirmed'] =(item.find_all("td",{"class":"l3HOY"})[0].text)
		d['CPMP'] = (item.find_all("td",{"class":"l3HOY"})[1].text)
		d['Recovered'] = (item.find_all("td",{"class":"l3HOY"})[2].text)
		d['Death'] = (item.find_all("td",{"class":"l3HOY"})[3].text)
		id +=1
		l.append(d)

	r = requests.get("https://news.google.com/covid19/map?hl=en-IN&gl=IN&ceid=IN%3Aen&mid=%2Fm%2F03rk0", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
	c = r.content
	soup = BeautifulSoup(c,"html.parser")

	india = soup.find_all("tr",{"class":"sgXwHf wdLSAe YvL7re"})
	for item in india:
		d={}
		d['ID'] = id
		d['Country'] = (item.find("div",{"class":"pcAJd"}).text)
		d['Confirmed'] =(item.find_all("td",{"class":"l3HOY"})[0].text)
		d['CPMP'] = (item.find_all("td",{"class":"l3HOY"})[1].text)
		d['Recovered'] = (item.find_all("td",{"class":"l3HOY"})[2].text)
		d['Death'] = (item.find_all("td",{"class":"l3HOY"})[3].text)
		id +=1
		l.append(d)
	
	return l

def get_data(text):
	text = text.lower()
	country = None
	case = None
	active = None
	death = None
	recover =None
	
	for word in text.split():
		for i in df['Country']:
			if word == i.lower():
				country= i
	try:
		if country == None:
			country = df['Country'][0]
		if text.count("cases") > 0 or text.count("case")>0 or text.count("confirm")>0 or text.count("confirmed")>0:
			case = (df[df.Country == country].Confirmed).tolist()	
			result = case
		if text.count("active") > 0:
			case = (df[df.Country == country].Confirmed).tolist()	
			recover=(df[df.Country==country].Recovered).tolist()
			case = "".join(case[0].split(","))
			recover = "".join(recover[0].split(","))
			result = []
			result.append(str(int(case)-int(recover)))
			
		if 	text.count("death") > 0:
			death = (df[df.Country==country].Death).tolist()
			print(death)
			result =death
		if 	text.count("recovered") > 0 or text.count("recover") > 0:
			recover = (df[df.Country==country].Recovered).tolist()
			result =recover
		
		result = "".join(result[0].split(","))	
		print(result)
	except:
		result = None	
	if case != None:
		speak("There are "+str(result)+" cases in "+ country)
	elif death !=None:
		speak("There are "+str(result)+" deaths in" +country)
	elif recover!=None:
		speak("There are "+str(result)+" recovered cases in"+ country)
	else:
		try:
			search = text.replace(" ","+")
			speak("This is what I found on web")
			PATH = "C:\Program Files (x86)\chromedriver.exe"
			driver = webdriver.Chrome(PATH)
			driver.get("https://www.google.com/search?q="+search+"&oq="+search+"&aqs=chrome.0.0j69i57j0l3.9430j0j7&sourceid=chrome&ie=UTF-8")
		except:
			pass

speak("wait for few seconds, while it's loading")
print("Loading....")
l = load_data()
df= pandas.DataFrame(l)
df.set_index("ID",inplace = True)
df.to_csv("Output.csv")

speak("Hi, I am Corona virus voice assistant. Made by Harsh Gandhi. I can give you latest updates on corona virus.")
speak("say 'hello' to wake me up")
speak("say 'goodbye' to make me sleep")

WAKE = "hello"
GOODBYE = "goodbye"

while True:
	text = get_audio()
	if text.count(WAKE) > 0:
		speak("I am ready")
		text = get_audio()
		if text.count(GOODBYE) > 0:
			speak("Good bye!")		
			break
		else:
			get_data(text)
	if text.count(GOODBYE) > 0:
		speak("Good bye!")		
		break