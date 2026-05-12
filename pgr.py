import time
import random
import colorama
from colorama import init, Fore
from colorama import init, Style
import pyfiglet
import downloader
from downloader import mp4_ytb
from downloader import mp3_ytb
import os
import sys

text = pyfiglet.figlet_format (" WELCOME TO PGR TOOLS  (beta)",  font="standard")
print(Fore.CYAN + text + Style.RESET_ALL)

print ("write " + Fore.GREEN + "help"+	Style.RESET_ALL +" to view all pgr")
print(Fore.RED + "created by rusher" + Style.RESET_ALL)

for i in range(100):
	pgr = input("|>")
	
	if pgr == "addition":
		number1 = int(input("| first number >"))
		number2 = int(input("| second number >"))
		result = number1 + number2
		print(Fore.GREEN + str(result) + Style.RESET_ALL )
		
	if pgr == "subtraction":
		number1 = int(input("| first number >"))
		number2 = int(input("| second number >"))
		result = number1 - number2
		print(Fore.GREEN + str(result) + Style.RESET_ALL )
		
	if pgr == "multiplication":
		number1 = int(input("| first number >"))
		number2 = int(input("| second number >"))
		result = number1 * number2
		print(Fore.GREEN + str(result) + Style.RESET_ALL )
		
	if pgr == "division":
		number1 = int(input("| first number >"))
		number2 = int(input("| second number >"))
		result = number1 / number2
		print(Fore.GREEN + str(result) + Style.RESET_ALL )
		
	if pgr == "random password":
		letters = "abcdefghijklmnopqrstuvwxyz"
		numbers = "123456789"
		maj_letters = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
		
		password = ""
		
		for i in range(10):
			password += random.choice(letters)
			password += random.choice(numbers)
			password += random.choice(maj_letters)
			
		print("| password generated >")
		print(Fore.GREEN + str(password) + Style.RESET_ALL)
		
		
	if pgr == "ascii text":
		textascii = input("| ecrit quelque chose... >")
		
		result = pyfiglet.figlet_format (textascii, font = "standard")
		print(result)
		
	if pgr == "hello":
		print(Fore.GREEN+ "| hi :)" + Style.RESET_ALL)
		
	if pgr == "hi":
		print(Fore.GREEN +"| hello :)" + Style.RESET_ALL)
		
	if pgr == "time tool 1":
		seconds = int(input("| time ?>"))
		for i in range(seconds, 0, -1):
			print(i)
			time.sleep(1)
		print("out!!!")
		
	if pgr == "ytb4":
		mp4_ytb()
		
	if pgr == "ytb3":
		mp3_ytb()
		
	if pgr == "credits":
		print(Fore.CYAN +"| DEV : Rusher")
		print("| thank for use pgr tools" + Style.RESET_ALL)
		
	if pgr == "exit":
		print(Fore.CYAN + "| bye user :)" + Style.RESET_ALL)
		exit()
		
	if pgr == "-v":
		print(Fore.CYAN + "| PGR	V.beta" + Style.RESET_ALL)
		
	if pgr == "community":
		print(Fore.CYAN + "| comming soon" + Style.RESET_ALL)
		
	if pgr == "help":
		print("| PROGRAMME :")
		print(Fore.GREEN + "| addition")
		print("| subtraction")
		print("| multiplication")
		print("| division")
		print("| time tool 1")
		print("| ascii text")
		print("| exit")
		print("| ytb4")
		print("| ytb3")
		print("| credits")
		print("| -v")
		print("| community")
		print(Fore.GREEN + "| random password" + Style.RESET_ALL)
