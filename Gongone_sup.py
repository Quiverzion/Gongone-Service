import discord
from discord.ext import commands
from keep_alive import keep_alive
import os


bot = commands.Bot(command_prefix=';;',
                   status=discord.Status.online, intents=discord.Intents.all())


@bot.event
async def on_ready():
  print(f'Gongone.Service: Pay Script Runned on [{bot.user}]')


@bot.event
async def on_message(ctx):
  if ctx.author.id == bot.user.id:
    return

  if ctx.channel.id == 937561123912306758:
    if ctx.content[0] == "!":
      await ctx.channel.send("전적이는 여기서! <#934776289884262441>", reference=ctx)
  
  ban_words = ["시발", "ㅅㅂ", "존나", "ㅈㄴ", "좆", "ㅈ같", "애미", "개새끼"]
  for i in range(len(ban_words)):
    for j in range(len(ctx.content)-len(ban_words[i])+1):
      if ctx.content[j:j+len(ban_words[i])] == ban_words[i]:
        await ctx.delete()
        await ctx.channel.send(f"{ctx.author.mention} 부적절한 단어를 사용했어요..!")
        return



keep_alive()


bot.run(os.environ["token"])
