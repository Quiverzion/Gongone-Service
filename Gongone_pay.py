import discord
from discord.ext import commands, tasks
import random
import Project_manager

bot = commands.Bot(command_prefix=';',
                   status=discord.Status.online, intents=discord.Intents.all())

pm_data = Project_manager.data()


def convertion(num: int):
    if num >= 100000000:
        if num % 100000000//10000 == 0:
            return f"{num//100000000}억 코인"
        else:
            return f"{num//100000000}억 {num%100000000//10000}만 코인"
    elif num >= 10000:
        if num % 10000 == 0:
            return f"{num//10000}만 코인"
        else:
            return f"{num//10000}만 {num%10000}코인"
    else:
        return f"{num}코인"


async def service_join(user_id: int):
    d = pm_data.data_get()
    for key in d:
        if key == f"User:{user_id}":
            return False
    d[f"User:{user_id}"] = {"money": 0, "stocks": {"ChunbaeStock": 0, "BirdMusic": 0,
                                                   "MarsCoin": 0, "SeojunCoin": 0}, "exp": 0, "is_smtm": False, "role": 0}
    pm_data.data_set(d)
    return True


async def set_money(user_id: int, num: int):
    d = pm_data.data_get()
    for key in d:
        if key == f"User:{user_id}":
            return False
    d[f"User:{user_id}"]["money"] = num
    pm_data.data_set(d)
    return True


@bot.event
async def on_ready():
    print(f'Gongone.Service: Pay Script Runned on [{bot.user}]')
    stocks.start()


@tasks.loop(seconds=1)
async def stocks():
    d = pm_data.secrets_get()
    x = d["stocks"]["seconds"]
    sjc = d["stocks"]["SeojunCoin"][0]
    if x >= 30:
        x = 1
        d["stocks"]["SeojunCoin"][1] = sjc
        if sjc <= 100:
            sjc += random.randint(0, 100)
        else:
            sjc += random.randint(-80, 80)
    else:
        x += 1
    d["stocks"]["seconds"] = x
    d["stocks"]["SeojunCoin"][0] = sjc
    pm_data.secrets_set(d)


@bot.command(aliases=["계좌", "지갑", "돈", "ㄱㅈ", "ㅈㄱ", "ㄷ", "rw", "wr", "e"])
async def show_money(ctx):
    await service_join(ctx.author.id)
    data = pm_data.data_get()
    embed = discord.Embed(title="Gongone Pay 지갑정보")
    d = convertion(data[f"User:{ctx.author.id}"]["money"])
    embed.add_field(name="소지금액", value=f"{d}")
    embed.set_footer(text=f"{ctx.author} | {ctx.author.id}",
                     icon_url=ctx.author.avatar.url)
    if data[f"User:{ctx.author.id}"]["stocks"]["SeojunCoin"] > 0:
        SJC = data[f"User:{ctx.author.id}"]["stocks"]["SeojunCoin"]
        embed.add_field(name="서준코인", value=f"{SJC}개", inline=False)
    await ctx.send(embed=embed, reference=ctx.message)


def inf_stocks(stocks_name: str):
    d = pm_data.secrets_get()["stocks"][stocks_name]
    if d[0] - d[1] > 0:
        return f"```diff\n+  {d[0]}  ▲ {d[0] - d[1]}```"
    if d[0] - d[1] < 0:
        return f"```diff\n-  {d[0]}  ▼ {abs(d[0] - d[1])}```"
    if d[0] - d[1] == 0:
        return f"```diff\n   {d[0]}    {abs(d[0] - d[1])}```"


@bot.command(aliases=["주식", "코인", "ㅈㅅ", "ㅋㅇ", "wt", "zd"])
async def show_stocks(ctx):
    await service_join(ctx.author.id)
    data = pm_data.secrets_get()
    embed = discord.Embed(title="Gongone Pay 주식차트")
    embed.add_field(name="춘배증권", value=inf_stocks(
        "ChunbaeStock"), inline=False)
    embed.add_field(name="버드뮤직", value=inf_stocks("BirdMusic"), inline=False)
    embed.add_field(name="쵝앙코인", value=inf_stocks("MarsCoin"), inline=False)
    embed.add_field(name="서준코인", value=inf_stocks("SeojunCoin"), inline=False)
    t = data["stocks"]["seconds"]
    if t == 30:
        embed.set_footer(text=f"지금 변동됨")
    else:
        embed.set_footer(text=f"다음 변동: {30-t}초 후")
    await ctx.send(embed=embed, reference=ctx.message)


bot.run(pm_data.secrets_get()["tokens"]["Gongone_pay"])
