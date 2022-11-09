from itertools import count
from socket import MsgFlag
from typing import Counter
from xmlrpc import client
from config import *
import random
from asyncio import sleep
import time
import os
import discord
import colorama
from colorama import init
from colorama import init, Fore, Back, Style
from discord.ext import commands
colorama.init()

token = token
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-n ',intents=intents)
global check
check = '\N{THUMBS UP SIGN}'
global counter
counter = 0


@bot.event
async def on_ready():
	global localcount
	global counting_channel
	counting_channel = None
	if os.path.isfile('numbers.txt') == False:
		print(f'[{Fore.RED}{Style.BRIGHT}WARNING{Fore.WHITE}] {Fore.WHITE}Cannot find numbers path, creating one now.')
		f= open("numbers.txt","w+")
		f.write("0")
		f.close()
	f = open("numbers.txt","r+")
	localcount =f.read()
	localcount = int(localcount)	
	f.close()
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='For the next number :)'))
	print(f"{Fore.WHITE}[{Fore.GREEN}{Style.BRIGHT}SUCCESS{Fore.WHITE}] Connected to {Fore.GREEN}{Style.BRIGHT}{bot.user.name}{Fore.WHITE}, and assigned localcount to {Fore.RED}{Style.BRIGHT}{localcount}{Fore.WHITE}.")


def reset():
	global localcount
	file = open("numbers.txt","r+")
	file.truncate(0)
	print(f"{Fore.WHITE}[{Fore.RED}{Style.BRIGHT}FAIL{Fore.WHITE}] Someone ruined count, whoops.")
	file.write('0')
	file.close()

@bot.command()
async def setchannel(ctx, channel: discord.TextChannel):
	await ctx.send(f'{Fore.WHITE}[{Fore.GREEN}{Style.BRIGHT}SUCCESS{Fore.WHITE}] Counting channel set.')
	global counting_channel
	counting_channel = channel.id
	await ctx.channel.purge(limit= 100)		

@bot.event
async def on_message(message):
	global counter
	await bot.process_commands(message)
	global counting_channel
	file = open("numbers.txt","r+")
	localcount =file.read()
	file.close()
	isint = True
	msg = message.content
	if message.author.id == bot.user.id:
		return print(f'{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{Style.BRIGHT}PASS{Fore.WHITE}] Skipping bot message.')
	if counting_channel == None:
		return await message.channel.send("Please set a counting channel using -n setchannel.")
	elif message.channel.id == counting_channel:
		try:
			msg = int(msg)
		except:
			print(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{Style.BRIGHT}PASS{Fore.WHITE}] Could not turn {Fore.RED}{msg} {Fore.WHITE}into a int.")
			channel = bot.get_channel(counting_channel)
			await channel.purge(limit= 1)
			isint = False
		if isint == True:
			if message.channel.id == counting_channel:
				if msg == int(localcount) + 1:
					await message.add_reaction(check)
					counter = counter + 1
					print(f"{Fore.WHITE}[{Fore.GREEN}{Style.BRIGHT}SUCCESS{Fore.WHITE}] Count increased to {Fore.GREEN}{msg}")
					getnext()
					resetvar()
				elif msg != int(localcount) + 1:
					correctnum = int(localcount) + 1
					idiot = f'<@{message.author.id}>'
					reset()
					file = open("numbers.txt","r+")
					localcount =file.read()
					file.close()
					await message.add_reaction('🚫')
					newnumber = int(localcount) + 1
					channel = bot.get_channel(counting_channel)
					await channel.purge(limit= counter + 1)
					print(f"{Fore.WHITE}[{Fore.GREEN}{Style.BRIGHT}SUCCESS{Fore.WHITE}] Purged all messages.")
					await channel.send(f'Wrong! {idiot} sent {msg}! The correct number would have been {correctnum}.')
					await channel.send(f'Next number is {newnumber}.')
	
def resetvar():
	global localcount
	file = open("numbers.txt","r+")
	file.truncate(0)
	file.write(new)
	file.close()


def getnext():
	global new
	file = open("numbers.txt","r+")
	localcount =file.read()
	localcount = int(localcount)
	new = (localcount + 1)
	new = str(new)


bot.run(token)