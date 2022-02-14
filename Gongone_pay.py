from email import message
import discord
from discord.ext import commands, tasks
import random
import Project_manager
import numbers

bot = commands.Bot(command_prefix=';',
                   status=discord.Status.online, intents=discord.Intents.all())

pm_data = Project_manager.data()


def conversion(num: int):
    num = abs(num)
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
    d[f"User:{user_id}"] = {"money": 1000000, "stocks": {"ChunbaeStock": [0, 0], "BirdMusic": [0, 0],
                                                   "MarsCoin": [0, 0], "SeojunCoin": [0, 0]}, "exp": 0, "is_smtm": False, "role": 0}
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


async def message_money(ctx, message: str, num: int):
    if num > 0:
        await ctx.send(f"{message}\n`+ {conversion(num)}`", reference=ctx.message)
    elif num < 0:
        await ctx.send(f"{message}\n`- {conversion(num)}`", reference=ctx.message)


def inf_stocks(stocks_name: str):
    d = pm_data.secrets_get()["stocks"][stocks_name]
    ats = format(d[0], ",")
    att = abs(d[0] - d[1])
    if d[0] - d[1] > 0:
        return f"```diff\n+  {ats}  ▲ {att}```"
    if d[0] - d[1] < 0:
        return f"```diff\n-  {ats}  ▼ {att}```"
    if d[0] - d[1] == 0:
        return f"```diff\n   {ats}  ● {att}```"


def stocks_sjc(d):
    d["stocks"]["SeojunCoin"][1] = d["stocks"]["SeojunCoin"][0]
    if d["stocks"]["SeojunCoin"][0] <= 900:
        d["stocks"]["SeojunCoin"][0] += random.randint(0, 400)
    elif d["stocks"]["SeojunCoin"][0] >= 4000:
        d["stocks"]["SeojunCoin"][0] += random.randint(-600, -300)
    else:
        d["stocks"]["SeojunCoin"][0] += random.randint(-400, 400)
    pm_data.secrets_set(d)


def stocks_hbd(d):
    d["stocks"]["BirdMusic"][1] = d["stocks"]["BirdMusic"][0]
    if d["stocks"]["BirdMusic"][0] <= 1800:
        d["stocks"]["BirdMusic"][0] += random.randint(0, 1700)
    elif d["stocks"]["BirdMusic"][0] >= 12000:
        d["stocks"]["BirdMusic"][0] += random.randint(-2500, -1800)
    else:
        d["stocks"]["BirdMusic"][0] += random.randint(-1500, 1500)
    pm_data.secrets_set(d)


def stocks_msc(d):
    d["stocks"]["MarsCoin"][1] = d["stocks"]["MarsCoin"][0]
    if d["stocks"]["MarsCoin"][0] <= 300:
        d["stocks"]["MarsCoin"][0] += random.randint(0, 80)
    elif d["stocks"]["MarsCoin"][0] >= 800:
        d["stocks"]["MarsCoin"][0] += random.randint(-200, -100)
    else:
        d["stocks"]["MarsCoin"][0] += random.randint(-60, 85)
    pm_data.secrets_set(d)


@bot.event
async def on_ready():
    print(f'Gongone.Service: Pay Script Runned on [{bot.user}]')
    change_stocks.start()


@tasks.loop(seconds=1)
async def change_stocks():
    d = pm_data.secrets_get()
    x = d["stocks"]["seconds"]
    if x >= 15:
        x = 1
    else:
        x += 1
        if x == 15:
            stocks_sjc(d)
            stocks_hbd(d)
            stocks_msc(d)
    d["stocks"]["seconds"] = x
    pm_data.secrets_set(d)


def sjc_embed(ctx, data, embed):
    if data[f"User:{ctx.author.id}"]["stocks"]["SeojunCoin"][0] > 0:
        SJC = data[f"User:{ctx.author.id}"]["stocks"]["SeojunCoin"]
        s = pm_data.secrets_get()["stocks"]["SeojunCoin"][0]*SJC[0] - SJC[1]
        if s > 0:
            sonic = f"+ {conversion(s)}"
        elif s < 0:
            sonic = f"- {conversion(s)}"
        else:
            j = format(SJC[0], ",")
            embed.add_field(name="서준코인", value=f"> **{j}개**", inline=False)
            return
        j = format(SJC[0], ",")
        embed.add_field(
            name="서준코인", value=f"> **{j}개**\n```diff\n{sonic}```", inline=False)


def hbd_embed(ctx, data, embed):
    if data[f"User:{ctx.author.id}"]["stocks"]["BirdMusic"][0] > 0:
        HBD = data[f"User:{ctx.author.id}"]["stocks"]["BirdMusic"]
        s = pm_data.secrets_get()["stocks"]["BirdMusic"][0]*HBD[0] - HBD[1]
        if s > 0:
            sonic = f"+ {conversion(s)}"
        elif s < 0:
            sonic = f"- {conversion(s)}"
        else:
            j = format(HBD[0], ",")
            embed.add_field(name="버드뮤직", value=f"> **{j}개**", inline=False)
            return
        j = format(HBD[0], ",")
        embed.add_field(
            name="버드뮤직", value=f"> **{j}개**\n```diff\n{sonic}```", inline=False)


@bot.command(aliases=["계좌", "지갑", "돈", "ㄱㅈ", "ㅈㄱ", "ㄷ", "rw", "wr", "e"])
async def show_money(ctx, tag: str = "me"):
    await service_join(ctx.author.id)
    data = pm_data.data_get()
    embed = discord.Embed(title="Gongone Pay 지갑정보")
    d = conversion(data[f"User:{ctx.author.id}"]["money"])
    embed.add_field(name="소지금액", value=f"> **{d}**")
    embed.set_footer(text=f"{ctx.author} | {ctx.author.id}",
                     icon_url=ctx.author.avatar.url)
    sjc_embed(ctx, data, embed)
    hbd_embed(ctx, data, embed)
    await ctx.send(embed=embed, reference=ctx.message)


@bot.command(aliases=["주식", "코인", "ㅈㅅ", "ㅋㅇ", "wt", "zd"])
async def stocks(ctx, control: str = "None", stocks_name: str = "None", amount: str = "None"):
    if control == "ㄱㅁ" or control == "구매":
        await stocks_buy(ctx, stocks_name, amount)
        return
    elif control == "ㅍㅁ" or control == "판매":
        await stocks_sell(ctx, stocks_name, amount)
        return
    await service_join(ctx.author.id)
    data = pm_data.secrets_get()
    embed = discord.Embed(title="Gongone Pay 주식차트")
    #embed.add_field(name="춘배증권", value="```diff\n   None```", inline=False)
    embed.add_field(name="버드뮤직", value=inf_stocks("BirdMusic"), inline=True)
    #embed.add_field(name="쵝앙코인", value=inf_stocks("MarsCoin"), inline=True)
    embed.add_field(name="서준코인", value=inf_stocks("SeojunCoin"), inline=True)
    t = data["stocks"]["seconds"]
    if t == 15:
        embed.set_footer(text=f"지금 변동됨")
    else:
        embed.set_footer(text=f"다음 변동: {15-t}초 후")
    await ctx.send(embed=embed, reference=ctx.message)


async def stocks_buy(ctx, stocks_name: str, amount: str):
    if stocks_name == "서준코인":
        stocks_name = "SeojunCoin"
    if stocks_name == "버드뮤직":
        stocks_name = "BirdMusic"
    d = pm_data.data_get()
    s = pm_data.secrets_get()
    if amount == "다" or amount == "ek":
        amount = int(d[f"User:{ctx.author.id}"]["money"]//s["stocks"][stocks_name][0])
    else:
        amount = int(amount)
    if d[f"User:{ctx.author.id}"]["money"] < s["stocks"][stocks_name][0]*amount:
        await ctx.send("이런.. 너무 큰 금액을 원하시네요;;", reference=ctx.message)
        return
    d[f"User:{ctx.author.id}"]["money"] -= s["stocks"][stocks_name][0]*amount
    d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0] += amount
    d[f"User:{ctx.author.id}"]["stocks"][stocks_name][1] += s["stocks"][stocks_name][0]*amount
    pm_data.data_set(d)
    if stocks_name == "SeojunCoin":
        stn = "서준코인"
        am = format(amount, ",")
        await message_money(ctx, f"{stn} {am}개를 구매했어요!", s["stocks"][stocks_name][0]*amount*-1)
    if stocks_name == "BirdMusic":
        stn = "버드뮤직"
        am = format(amount, ",")
        await message_money(ctx, f"{stn} {am}주를 구매했어요!", s["stocks"][stocks_name][0]*amount*-1)


async def stocks_sell(ctx, stocks_name: str, amount: str):
    if stocks_name == "서준코인":
        stocks_name = "SeojunCoin"
    if stocks_name == "버드뮤직":
        stocks_name = "BirdMusic"
    d = pm_data.data_get()
    s = pm_data.secrets_get()
    if amount == "다" or amount == "ek":
        amount = int(d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0])
    else:
        amount = int(amount)
    if d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0] < amount:
        await ctx.send("너무 많은 수량을 입력했어요!", reference=ctx.message)
        return
    d[f"User:{ctx.author.id}"]["money"] += s["stocks"][stocks_name][0]*amount
    average = d[f"User:{ctx.author.id}"]["stocks"][stocks_name][1]//d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0]
    d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0] -= amount
    if d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0] == 0:
        d[f"User:{ctx.author.id}"]["stocks"][stocks_name][1] = 0
    else:
        d[f"User:{ctx.author.id}"]["stocks"][stocks_name][1] -= average*amount
    pm_data.data_set(d)
    if stocks_name == "SeojunCoin":
        stn = "서준코인"
        am = format(amount, ",")
        await message_money(ctx, f"{stn} {am}개를 판매했어요!", s["stocks"][stocks_name][0]*amount)
    if stocks_name == "BirdMusic":
        stn = "버드뮤직"
        am = format(amount, ",")
        await message_money(ctx, f"{stn} {am}주를 판매했어요!", s["stocks"][stocks_name][0]*amount)

bot.run(pm_data.secrets_get()["tokens"]["Gongone_pay"])
