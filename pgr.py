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

text = pyfiglet.figlet_format (" WELCOME TO PGR TOOLS  V1.0.0",  font="standard")
print(Fore.CYAN + text + Style.RESET_ALL)

print ("write " + Fore.CYAN + "help"+	Style.RESET_ALL +" to view all pgr")
print(Fore.RED + "created by rusher" + Style.RESET_ALL)

for i in range(100):
	pgr = input("|>")
	
	if pgr == "addition":
		number1 = int(input("| first number >"))
		number2 = int(input("| second number >"))
		result = number1 + number2
		print(Fore.CYAN + str(result) + Style.RESET_ALL )
		
	if pgr == "subtraction":
		number1 = int(input("| first number >"))
		number2 = int(input("| second number >"))
		result = number1 - number2
		print(Fore.CYAN + str(result) + Style.RESET_ALL )
		
	if pgr == "multiplication":
		number1 = int(input("| first number >"))
		number2 = int(input("| second number >"))
		result = number1 * number2
		print(Fore.CYAN + str(result) + Style.RESET_ALL )
		
	if pgr == "division":
		number1 = int(input("| first number >"))
		number2 = int(input("| second number >"))
		result = number1 / number2
		print(Fore.CYAN + str(result) + Style.RESET_ALL )
		
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
		print(Fore.CYAN + str(password) + Style.RESET_ALL)
		
		
	if pgr == "ascii text":
		textascii = input("| ecrit quelque chose... >")
		
		result = pyfiglet.figlet_format (textascii, font = "standard")
		print(result)
		
	if pgr == "hello":
		print(Fore.CYAN+ "| hi :)" + Style.RESET_ALL)
		
	if pgr == "hi":
		print(Fore.CYAN +"| hello :)" + Style.RESET_ALL)
		
	if pgr == "time tool 1":
		seconds = int(input("| time ?>"))
		for i in range(seconds, 0, -1):
			print(i)
			time.sleep(1)
		print("| out!!!")
		
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
		
	if pgr == "uninstall":
		print("| exit PGR tools and copy paste this command")
		print(Fore.CYAN + " cd ~")
		print(" rm -rf pgr-tools" + Style.RESET_ALL)
		
	if pgr == "v":
		print(Fore.CYAN + "| PGRTools	v1.0.1" + Style.RESET_ALL)
		
	if pgr == "community":
		print(Fore.CYAN + "| comming soon" + Style.RESET_ALL)
		
	if pgr == "repo":
		print("| open code")
		print(Fore.CYAN + "https://github.com/rusher-code-330/pgr-tools" + Style.RESET_ALL)
		
	if pgr == "pgr update":
		print("| updating PGR tools...")
		os.system("cd ~/pgr-tools && git pull")
		print(Fore.CYAN + "| PGR Tools restart. . ." + Style.RESET_ALL)
		os.execl(sys.executable, sys.executable, *sys.argv)
		
	if pgr == "help":
		print("| PROGRAMME :\n")

		print(Fore.CYAN + "== MATH ==")
		print("| addition")
		print("| subtraction")
		print("| multiplication")
		print("| division\n")

		print(Fore.CYAN + "== TOOLS ==")
		print("| time tool 1")
		print("| ascii text")
		print("| random password\n")

		print("== YOUTUBE ==")
		print("| ytb3")
		print("| ytb4\n")

		print("== SYSTEM ==")
		print("| pgr update")
		print("| exit")
		print("| uninstall")
		print("| credits")
		print("| v")
		print("| community")
		print("| repo" + Style.RESET_ALL)
