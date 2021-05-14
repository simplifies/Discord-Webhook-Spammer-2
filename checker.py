import os
import requests
import ctypes
import threading
import time
from colorama import Fore, init
import random

from core.localscommands import clear, pause, title

#  set to true if needed
debug = False


init()
def start():
	clear()
	global webhookk
	webhookk = ""
	webhookk = input(Fore.YELLOW + "[?] Webhook: ")
	if webhookk == "":
		print("The value you entered was null. Please try again.")
		pause()
		start()
		return
	elif webhookk == " ":
		print("The value you entered was null. Please try again.")
		pause()
		start()
		return
	if "https://discord.com/api/webhooks/" in webhookk:
		pass
	else:
		print(Fore.RED + "[!] Please enter a valid webhook.")
		pause()
		clear()
		start()
		return
	clear()
	global username
	username = ""
	username = input(Fore.YELLOW + "[?] Username: ")
	if username == "":
		print("The value you entered was null. Please try again.")
		pause()
		start()
		return
	elif username == " ":
		print("The value you entered was null. Please try again.")
		pause()
		start()
		return
	clear()
	global message
	message = ""
	message = input(Fore.YELLOW + "[?] Message: ")
	if message == "":
		print("The value you entered was null. Please try again.")
		pause()
		start()
		return
	elif message == " ":
		print("The value you entered was null. Please try again.")
		pause()
		start()
		return
	clear()
	global img_url
	img_url = ""
	img_url = input(Fore.YELLOW + "Leave blank if no image url wanted.\n[?] Image URL: ")


sent = 0
ratelimit = 0 
total = 0
errorCodes = [100, 101, 103, 201, 202, 203, 204, 205, 206, 300, 301, 302, 303, 304, 307, 308, 400, 401, 402, 403, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 422, 425, 426, 428, 431, 451, 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511]

def getProxy():
	global proxList
	global proxList2
	prox = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=US&ssl=no&anonymity=all")
	if prox.text == "You have reached your hourly maximum API requests of 750.":
		print("Please wait an hour before running this script again.")
		pause()
		exit()
	proxyTxt = prox.text.splitlines()
	proxList = []
	for line in proxyTxt:
		proxList.append(line)
	prox2 = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=US&ssl=yes&anonymity=all")
	if prox2.text == "You have reached your hourly maximum API requests of 750.":
		print("Please wait an hour before running this script again.")
		pause()
		exit()
	proxyTxt2 = prox2.text.splitlines()
	proxList2 = []
	for line in proxyTxt2:
		proxList2.append(line)

def main():
	clear()
	print(Fore.YELLOW + "[!] If you are having issues with the spammer try restarting the script to get new proxies.")
	try:
		getProxy()
		pass
	except Exception as e:
		clear()
		print(f"Error:\n{e}")
		pause()
		exit()
	try:
		while True:
			thread = threading.Thread(target=spam, daemon=True)
			thread.start()
			time.sleep(0.5)
		pause()
	except Exception as e:
		if debug == True:
			print(e)
			pause()
			exit()
	
				

def spam():
	global ratelimit
	global sent
	global total
	global randProxy
	global randProxySSL
	randProxy = random.choice(proxList)
	randProxySSL = random.choice(proxList2)
	try:
		discordAPI = requests.post(webhookk, data={"content": message, "image_url": img_url, "username": username}, proxies={"http": randProxy,"https": randProxySSL})
	except Exception as e:
		if debug == True:
			print(e)
			pass
		return
	if discordAPI.status_code == 401:
		total += 1
		title("Discord Webhook Spammer | arshan.xyz | Sent: " + str(sent) +  " Ratelimited: " + str(ratelimit) + " Total: " + str(total))
		print(Fore.RED + f"[-] Webhook is invalid.")
	elif discordAPI.status_code == 204:
		sent += 1
		total += 1
		title("Discord Webhook Spammer | arshan.xyz | Sent: " + str(sent) +  " Ratelimited: " + str(ratelimit) + " Total: " + str(total))
		print(Fore.GREEN + f"[+] Sent message to webhook.")
	elif discordAPI.status_code == 429:
		total += 1
		ratelimit += 1
		title("Discord Webhook Spammer | arshan.xyz | Sent: " + str(sent) +  " Ratelimited: " + str(ratelimit) + " Total: " + str(total))
		print(Fore.YELLOW + "[!] You are being ratelimited.")
	elif discordAPI.status_code in errorCodes:
		total += 1
		title("Discord Webhook Spammer | arshan.xyz | Sent: " + str(sent) +  " Ratelimited: " + str(ratelimit) + " Total: " + str(total))
		print(Fore.YELLOW + "[!] An unexpected error has occured. Error Code: " + str(discordAPI.status_code))

def menu():
	title("Discord Webhook Spammer | arshan.xyz | Sent: " + str(sent) +  " Ratelimited: " + str(ratelimit) + " Total: " + str(total))
	main()

if __name__ == "__main__":
	start()
	menu()
	
