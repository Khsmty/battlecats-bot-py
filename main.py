import discord
import os
import re
import numpy as np
from keep_alive import keep_alive
from googletrans import Translator
from dispander import dispand

client = discord.Client()
translator = Translator()

@client.event
async def on_ready():
    print("Botが起動しました")
    print(client.user)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('.trans'):
        say = message.content
        say = say[7:]
        if say.find('-') == -1:
            str = say
            detact = translator.detect(str)
            befor_lang = detact.lang
            if befor_lang == 'ja':
                convert_string = translator.translate(str, src=befor_lang, dest='en')
                embed = discord.Embed(title='Translator', color=0xff0000)
                embed.add_field(name='Before', value=str)
                embed.add_field(name='After', value=convert_string.text, inline=False)
                await message.channel.send(embed=embed)
            else:
                convert_string = translator.translate(str, src=befor_lang, dest='ja')
                embed = discord.Embed(title='Translator', color=0xff0000)
                embed.add_field(name='Before', value=str)
                embed.add_field(name='After', value=convert_string.text, inline=False)
                await message.channel.send(embed=embed)
        else:
            trans, str = list(say.split('='))
            befor_lang, after_lang = list(trans.split('-'))
            convert_string = translator.translate(str, src=befor_lang, dest=after_lang)
            embed = discord.Embed(title='Translator', color=0xff0000)
            embed.add_field(name='Before', value=str)
            embed.add_field(name='After', value=convert_string.text, inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith('.detect'):
        say = message.content
        s = say[8:]
        detect = translator.detect(s)
        m = 'この文字列の言語はたぶん ' + detect.lang + ' です。'
        await message.channel.send(m)

    if message.author.bot:
        return
    await dispand(message)

    if message.channel.category_id == 712220796449456238:
        await message.channel.edit(position=0)
        print(message.channel.name)
    elif message.channel.category_id == 712222487798349845:
        await message.channel.edit(position=0)
        print(message.channel.name)
    elif message.channel.category_id == 712236287599575141:
        await message.channel.edit(position=0)
        print(message.channel.name)

async def on_message(self, message):
      if message.author.bot:
          return

      if re.match(r'.d .*', message.content):  
        content = message.content.replace('.d ', '')
        splitPlus = content.split('+')
        formatedContent = content.replace(' ', '').replace('+', ' + ')
        reply = message.author
        
        response = "**" + formatedContent + "**\n"

        result = 0
        for (i, context) in enumerate(splitPlus):
          splited = context.split('d')

          if len(splited) == 1:
            result = result + int(splited[0])
            response = response + splited[0]
          else:
            for dice in range(int(splited[0])):
              res = np.random.randint(1, splited[1])
              result = result + res
              response = response + str(res)

              if not (int(splited[0]) == 1):
                if not ((dice == (int(splited[0]) - 1))):            
                  response = response + " , "
                elif (dice == int(splited[0]) - 1) and (len(splitPlus) == 1):
                  response = response + "\n合計: **" + str(result) + "**"

          if not (len(splitPlus) == 1):
            if not (i == (len(splitPlus) - 1)):
              response = response + " , "
            elif (i == len(splitPlus) - 1):
              response = response + "\n合計: **" + str(result) + "**"

        await message.reply(response, mention_author=True)

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)