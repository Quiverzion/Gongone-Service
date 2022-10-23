import discord
from discord.ext import commands, tasks
import random
import Project_manager

bot = commands.Bot(command_prefix=';',
                   status=discord.Status.online, intents=discord.Intents.all())

pm_data = Project_manager.data()

danwi = ["만", "억", "조", "경", "해", "자", "양", "구", "간", "정", "재", "극", "항하사", "아승기", "나유타", "불가사의", "무량대수", "에딩턴", "구골", "긍갈라", "아가라", "스큐스", "팩술", "최승", "마바라", "아바라", "다바라", "계분", "구골톨", "마리오플렉스", "보마", "녜마", "아바검", "미가바", "구골공", "비라가", "비가바","승갈라마", "비살라", "마이크릴리언"]                                                   
def conversion(num: int, type="Coin"):
    if type == "Coin":
        y = "코인"
    if type == "None":
        y = ""
    num = abs(num)
    for i in range(len(danwi)-1, -1, -1):
        if i == 0:
            if num >= 10**(4*(i+1)):
                if num % 10**(4*(i+1)) == 0:
                    return f"{num//10**(4*(i+1))}{danwi[i]} {y}"
                else:
                    return f"{num//10**(4*(i+1))}{danwi[i]} {num%10**(4*(i+1))}{y}"
            else:
                return f"{num}{y}"
        else:
            if num >= 10**(4*(i+1)):
                if num % 10**(4*(i+1))//10**(i) == 0:
                    return f"{num//10**(4*(i+1))}{danwi[i]} {y}"
                else:
                    return f"{num//10**(4*(i+1))}{danwi[i]} {num%10**(4*(i+1))//10**(4*i)}{danwi[i-1]} {y}"
    return


async def service_join(user_id: int):
    d = pm_data.data_get()
    for key in d:
        if key == f"User:{user_id}":
            return False
    d[f"User:{user_id}"] = {"money": 1000000, "stocks": {"ChunbaeStock": [0, 0], "BirdMusic": [0, 0],
                                                   "MarsCoin": [0, 0], "SeojunCoin": [0, 0]}, "exp": 100, "is_smtm": False, "role": 0}
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
        return f"```diff\n+  {ats}  ▲ {round(att / d[0] * 100, 1)}%```"
    if d[0] - d[1] < 0:
        return f"```diff\n-  {ats}  ▼ {round(att / d[0] * 100, 1)}%```"
    if d[0] - d[1] == 0:
        return f"```diff\n   {ats}  ● 0%```"


def stocks_sjc(d):
    d["stocks"]["SeojunCoin"][1] = d["stocks"]["SeojunCoin"][0]
    if d["stocks"]["SeojunCoin"][0] < 400:
        d["stocks"]["SeojunCoin"][0] += random.randint(0, d["stocks"]["SeojunCoin"][0]//4)
    else:
        d["stocks"]["SeojunCoin"][0] += random.randint(d["stocks"]["SeojunCoin"][0]//-10, d["stocks"]["SeojunCoin"][0]//10)
    pm_data.secrets_set(d)


def stocks_hbd(d):
    d["stocks"]["BirdMusic"][1] = d["stocks"]["BirdMusic"][0]
    if d["stocks"]["BirdMusic"][0] <= 5000:
        d["stocks"]["BirdMusic"][0] += random.randint(0, 2000)
    elif d["stocks"]["BirdMusic"][0] >= 1000000:
        d["stocks"]["BirdMusic"][0] += random.randint(-3000, -2000)
    else:
        d["stocks"]["BirdMusic"][0] += random.randint(-4000, 4000)
    pm_data.secrets_set(d)


def stocks_msc(d):
    d["stocks"]["MarsCoin"][1] = d["stocks"]["MarsCoin"][0]
    if d["stocks"]["MarsCoin"][0] < 80:
        d["stocks"]["MarsCoin"][0] += random.randint(0, d["stocks"]["MarsCoin"][0]*5)
    else:
        d["stocks"]["MarsCoin"][0] += random.randint(d["stocks"]["MarsCoin"][0]*3//-4, d["stocks"]["MarsCoin"][0]*3//4)
    pm_data.secrets_set(d)

def stocks_cbs(d):
    d["stocks"]["ChunbaeStock"][1] = d["stocks"]["ChunbaeStock"][0]
    if d["stocks"]["ChunbaeStock"][0] <= 15:
        d["stocks"]["ChunbaeStock"][0] += random.randint(1, 5)
    elif d["stocks"]["ChunbaeStock"][0] >= 30000:
        d["stocks"]["ChunbaeStock"][0] += random.randint(-30, -10)
    else:
        d["stocks"]["ChunbaeStock"][0] += random.randint(-12, 12)
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
            stocks_cbs(d)
    d["stocks"]["seconds"] = x
    pm_data.secrets_set(d)


def stocks_embed(author, data, embed, type):
    if type == "sjc":
        s_name = "SeojunCoin"
        r_name = "서준코인"
    if type == "hbd":
        s_name = "BirdMusic"
        r_name = "버드뮤직"
    if type == "msc":
        s_name = "MarsCoin"
        r_name = "화성코인"
    if type == "cbs":
        s_name = "ChunbaeStock"
        r_name = "춘배증권"
    if data[f"User:{author.id}"]["stocks"][s_name][0] > 0:
        SJC = data[f"User:{author.id}"]["stocks"][s_name]
        s = pm_data.secrets_get()["stocks"][s_name][0]*SJC[0] - SJC[1]
        if s > 0:
            sonic = f"+ {conversion(s)}"
        elif s < 0:
            sonic = f"- {conversion(s)}"
        else:
            j = conversion(SJC[0], "None")
            embed.add_field(name=r_name, value=f"> **{j}개**", inline=False)
            return
        j = conversion(SJC[0], "None")
        embed.add_field(
            name=r_name, value=f"> **{j}개**\n```diff\n{sonic}```", inline=False)


@bot.command(aliases=["계좌", "지갑", "돈", "ㄱㅈ", "ㅈㄱ", "ㄷ", "rw", "wr", "e"])
async def show_money(ctx, tag: str = "me"):
    await service_join(ctx.author.id)
    if tag == "me":
        author = ctx.author
    elif tag[:2] == "<@":
        author = bot.get_user(int(tag[2:20]))
    data = pm_data.data_get()
    try:
        embed = discord.Embed(title="혁명군 계좌정보")
        d = conversion(data[f"User:{author.id}"]["money"])
        embed.add_field(name="소지금액", value=f"> **{d}**")
        embed.set_footer(text=f"{author} | {author.id}",
                        icon_url=author.avatar.url)
        stocks_embed(author, data, embed, "sjc")
        stocks_embed(author, data, embed, "hbd")
        stocks_embed(author, data, embed, "msc")
        stocks_embed(author, data, embed, "cbs")
        await ctx.send(embed=embed, reference=ctx.message)
    except:
        await ctx.send("없는 계좌를 요청하였습니다.", reference=ctx.message)

@bot.command(aliases=["주식", "코인", "ㅈㅅ", "ㅋㅇ", "wt", "zd"])
async def stocks(ctx, control: str = "None", stocks_name: str = "None", amount: str = "None"):
    if control == "구매" or control == "ㄱㅁ" or control == "사기" or control == "ㅅㄱ":
        await stocks_buy(ctx, stocks_name, amount)
        return
    elif control == "판매" or control == "ㅍㅁ" or control == "팔기" or control == "ㅍㄱ":
        await stocks_sell(ctx, stocks_name, amount)
        return
    elif control == "보유" or control == "ㅂㅇ" or control == "나" or control == "ㄴ":
        if stocks_name == "None":
            await show_money(ctx)
        else:
            await show_money(ctx, stocks_name)
        return
    await service_join(ctx.author.id)
    data = pm_data.secrets_get()
    embed = discord.Embed(title="혁명군 주식차트")
    embed.add_field(name="버드뮤직", value=inf_stocks("BirdMusic"), inline=False)
    embed.add_field(name="화성코인", value=inf_stocks("MarsCoin"), inline=False)
    embed.add_field(name="서준코인", value=inf_stocks("SeojunCoin"), inline=False)
    embed.add_field(name="춘배증권", value=inf_stocks("ChunbaeStock"), inline=False)
    t = data["stocks"]["seconds"]
    if t == 15:
        embed.set_footer(text=f"지금 변동됨")
    else:
        embed.set_footer(text=f"다음 변동: {15-t}초 후")
    await ctx.send(embed=embed, reference=ctx.message)


async def stocks_buy(ctx, stocks_name: str, amount: str):
    if stocks_name == "버드뮤직" or stocks_name == "1" or stocks_name == "qjemabwlr":
        stocks_name = "BirdMusic"
        stn = "버드뮤직"
    if stocks_name == "화성코인" or stocks_name == "2" or stocks_name == "chlrkdzhdls":
        stocks_name = "MarsCoin"
        stn = "화성코인"
    if stocks_name == "서준코인" or stocks_name == "3" or stocks_name == "tjwnszhdls":
        stocks_name = "SeojunCoin"
        stn = "서준코인"
    if stocks_name == "춘배증권" or stocks_name == "4" or stocks_name == "cnsqowmdrnjs":
        stocks_name = "ChunbaeStock"
        stn = "춘배증권"
    d = pm_data.data_get()
    s = pm_data.secrets_get()
    if amount == "다" or amount == "ek":
        amount = int(d[f"User:{ctx.author.id}"]["money"]//s["stocks"][stocks_name][0])
    elif amount.isdigit():
        amount = int(amount)
    else:
        await ctx.send("올바르지 못한 수량을 입력하였습니다.", reference=ctx.message)
        return
    if d[f"User:{ctx.author.id}"]["money"] < s["stocks"][stocks_name][0]*amount:
        await ctx.send("소지하신 금액보다 큰 값을 요청했습니다.", reference=ctx.message)
        return
    if amount <= 0:
        await ctx.send("너무 작은 금액을 입력했습니다.", reference=ctx.message)
        return
    d[f"User:{ctx.author.id}"]["money"] -= s["stocks"][stocks_name][0]*amount
    d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0] += amount
    d[f"User:{ctx.author.id}"]["stocks"][stocks_name][1] += s["stocks"][stocks_name][0]*amount
    pm_data.data_set(d)
    if stocks_name == "SeojunCoin" or stocks_name == "MarsCoin":
        am = format(amount, ",")
        await message_money(ctx, f"{stn} **{am}개**를 구매를 구매하였습니다.", s["stocks"][stocks_name][0]*amount*-1)
    if stocks_name == "BirdMusic" or stocks_name == "ChunbaeStock":
        am = format(amount, ",")
        await message_money(ctx, f"{stn} **{am}주**를 구매하였습니다.", s["stocks"][stocks_name][0]*amount*-1)


async def stocks_sell(ctx, stocks_name: str, amount: str):
    if stocks_name == "버드뮤직" or stocks_name == "1" or stocks_name == "qjemabwlr":
        stocks_name = "BirdMusic"
        stn = "버드뮤직"
    if stocks_name == "화성코인" or stocks_name == "2" or stocks_name == "chlrkdzhdls":
        stocks_name = "MarsCoin"
        stn = "화성코인"
    if stocks_name == "서준코인" or stocks_name == "3" or stocks_name == "tjwnszhdls":
        stocks_name = "SeojunCoin"
        stn = "서준코인"
    if stocks_name == "춘배증권" or stocks_name == "4" or stocks_name == "cnsqowmdrnjs":
        stocks_name = "ChunbaeStock"
        stn = "춘배증권"
    d = pm_data.data_get()
    s = pm_data.secrets_get()
    if amount == "다" or amount == "ek":
        amount = int(d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0])
    elif amount.isdigit():
        amount = int(amount)
    else:
        await ctx.send("올바르지 못한 수량을 입력하였습니다.", reference=ctx.message)
        return
    if d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0] < amount:
        await ctx.send("소지하신 수량보다 더 큰 수량을 요청했습니다.", reference=ctx.message)
        return
    if d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0] <= 0:
        await ctx.send("해당 종목에서 보유햔 주식이 없습니다.", reference=ctx.message)
        return
    d[f"User:{ctx.author.id}"]["money"] += s["stocks"][stocks_name][0]*amount
    average = d[f"User:{ctx.author.id}"]["stocks"][stocks_name][1]//d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0]
    d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0] -= amount
    if d[f"User:{ctx.author.id}"]["stocks"][stocks_name][0] == 0:
        d[f"User:{ctx.author.id}"]["stocks"][stocks_name][1] = 0
    else:
        d[f"User:{ctx.author.id}"]["stocks"][stocks_name][1] -= average*amount
    pm_data.data_set(d)
    if stocks_name == "SeojunCoin" or stocks_name == "MarsCoin":
        am = format(amount, ",")
        await message_money(ctx, f"{stn} **{am}개**를 판매하였습니다.", s["stocks"][stocks_name][0]*amount)
    if stocks_name == "BirdMusic" or stocks_name == "ChunbaeStock":
        am = format(amount, ",")
        await message_money(ctx, f"{stn} **{am}주**를 판매하였습니다.", s["stocks"][stocks_name][0]*amount)

bot.run(pm_data.secrets_get()["tokens"]["Gongone_pay"])

