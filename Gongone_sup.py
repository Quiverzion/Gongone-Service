import discord
from discord.ext import commands
import Project_manager


bot = commands.Bot(command_prefix=';;',
                   status=discord.Status.online, intents=discord.Intents.all())

pm_data = Project_manager.data()


@bot.event
async def on_ready():
  print(f'Gongone.Service: Sup Script Runned on [{bot.user}]')


@bot.event
async def on_message(ctx):
  await bot.process_commands(ctx)

  if ctx.author.id == bot.user.id:
    return

  if ctx.channel.id == 937561123912306758:
    if ctx.content[0] == "!":
      await ctx.channel.send("전적이는 여기서! <#934776289884262441>", reference=ctx)

  ban_words = pm_data.secrets_get("ban_words")
  for i in range(len(ban_words)):
    for j in range(len(ctx.content)-len(ban_words[i])+1):
      if ctx.content[j:j+len(ban_words[i])] == ban_words[i]:
        await ctx.delete()
        await ctx.channel.send(f"{ctx.author.mention} 부적절한 단어를 사용했어요..!")
        return


@bot.command()
async def join(ctx):
  if ctx.author.voice and ctx.author.voice.channel:
    channel = ctx.author.voice.channel
    await channel.connect()
  else:
    await ctx.send("채널에 연결되지 않았습니다.")


bot.run(pm_data.secrets_get("tokens")["Gongone_sup"])
