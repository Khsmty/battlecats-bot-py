import discord
import os
import re
import numpy as np
from keep_alive import keep_alive
from googletrans import Translator
from dispander import dispand
from discord.ext import commands
from PIL import Image
import img_searcher

bot = commands.Bot(".")
translator = Translator()

@bot.event
async def on_ready():
  print("Botが起動しました")
  print(bot.user)

@bot.event
async def on_message(message):
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
  
  await bot.process_commands(message)

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

  await bot.process_commands(message)

@bot.command()
async def detect(ctx, arg):
  detect = translator.detect(arg)
  m = 'この文字列の言語はたぶん ' + detect.lang + ' です。'
  await ctx.send(m)

@bot.command()
async def trans(ctx, arg):
  if arg.find('-') == -1:
    str = arg
    detact = translator.detect(str)
    befor_lang = detact.lang
    if befor_lang == 'ja':
      convert_string = translator.translate(str, src=befor_lang, dest='en')
      embed = discord.Embed(title='Translator', color=0xff0000)
      embed.add_field(name='Before', value=str)
      embed.add_field(name='After', value=convert_string.text, inline=False)
      await ctx.send(embed=embed)
    else:
      convert_string = translator.translate(str, src=befor_lang, dest='ja')
      embed = discord.Embed(title='Translator', color=0xff0000)
      embed.add_field(name='Before', value=str)
      embed.add_field(name='After', value=convert_string.text, inline=False)
      await ctx.send(embed=embed)
  else:
    trans, str = list(arg.split('='))
    befor_lang, after_lang = list(trans.split('-'))
    convert_string = translator.translate(str, src=befor_lang, dest=after_lang)
    embed = discord.Embed(title='Translator', color=0xff0000)
    embed.add_field(name='Before', value=str)
    embed.add_field(name='After', value=convert_string.text, inline=False)
    await ctx.send(embed=embed)



icon_size = (247, 192)
icon_positions = [
  (396, 80), (724, 80), (1052, 80), (1380, 80), (1708, 80),
  (396, 292), (724, 293), (1052, 294), (1380, 295), (1708, 296)
]

#returns list of names failed to get
def create_image(names):
  i = 0
  failed_names = []
  for name in names:
        
    icon = img_searcher.search_icon(name)
    if icon != None:
      resized_icon = icon.resize(icon_size)
      bg.paste(resized_icon, icon_positions[i])
      i += 1
    else:
      failed_names.append(name)
    
  return failed_names

@bot.command()
async def hensei(ctx, *names):
  if len(names) == 0:
    await ctx.send("```キャラクターの名前を入力してください```")
    return
  if len(names) > 10:
    await ctx.send("```キャラクターの数を10体までにしてください```")
    return

  wait_message = await ctx.send("```少々お待ちください…```")
  global bg
  bg = Image.open("hensei_gamen.jpeg").convert("RGBA")
    
  failed_names = create_image(names)
  message_content = ""
  if len(failed_names) == 0:
    message_content = "```" + ctx.author.name + "の編成:```"
  else:
    message_content = "```" + ctx.author.name + "さん、" + "、".join(failed_names) + "の画像が見つかりませんでした```"
    
  bg.save("new_image.png")
  await ctx.send(content = message_content, file = discord.File("new_image.png"))
  await wait_message.delete()

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)