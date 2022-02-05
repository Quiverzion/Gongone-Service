import discord
from discord.ext import commands
from keep_alive import keep_alive
from replit import db
import random

def find_account_for_id(account_id):
  for key in db.keys():
    if key == account_id:
      return True
  return False


def find_account_for_user(user_id):
  values = []
  for key, value in db.items():
    if value[1] == user_id:
      values.append(key)
  return values


def security(id):
  managerId = [762202105451773965]
  for i in range(len(managerId)):
    if id == managerId[i]:
      return True
  return False


def conversion(m, p=0):
  if p == 1:
    buho = '+ '
  elif p == -1:
    buho = '- '
  else:
    buho = ''
  m = int(m)
  if m // 10000 != 0:
    if m % 10000 == 0:
      return f'{buho}{m // 10000}만 코인'
    else:
      return f'{buho}{m // 10000}만 {m % 10000} 코인'
  else:
    return f'{buho}{m} 코인'


bot = commands.Bot(command_prefix=';',
                   status=discord.Status.online, intents=discord.Intents.all())


@bot.event
async def on_ready():
  print(f'Gongone.Service: Pay Script Runned on [{bot.user}]')


@bot.command(aliases=["가입", "ㄱㅇ", "rd"])
async def sign_in(ctx):
  if find_account_for_user(ctx.author.id) != []:
    await ctx.send("이미 가입되어있어요!", reference=ctx.message)
  else:
    account_id = random.randint(1000, 9999)
    while find_account_for_id(f"GSOA:{account_id}"):
      account_id = random.randint(1000, 9999)
    db[f"GSOA:{account_id}"] = [100000, ctx.author.id]
    await ctx.send(f"가입되었어요, 선물이에요.\n`{conversion(100000, 1)}`", reference=ctx.message)


@bot.command(aliases=["계좌", "ㄱㅈ", "rw", "돈", "ㄷ", "e"])
async def pay(ctx, id: str = "me"):
  if id == "me":
    id = find_account_for_user(ctx.author.id)[0]
    target_value = db[id]
  elif find_account_for_id(id):
    target_value = db[id]
  else:
    await ctx.send("유효하지 않은 계좌아이디예요!", reference=ctx.message)
    return

  embed = discord.Embed(title="Gongone Pay 계좌정보")
  embed.add_field(name="금액", value=conversion(target_value[0]), inline=True)
  embed.add_field(name="소유자", value=str(
      bot.get_user(target_value[1])), inline=True)
  embed.add_field(name="아이디", value=str(id), inline=True)
  embed.set_footer(text=f"{ctx.author} | Made by Choi Kang",
                   icon_url=str(ctx.author.avatar_url))
  await ctx.send(embed=embed, reference=ctx.message)


@bot.command(aliases=["도박", "ㄷㅂ", "eq"])
async def gamble(ctx, value: int):
  if find_account_for_user(ctx.author.id) == []:
    await ctx.send("계좌를 생성해야해요, `;가입` 으로 계좌를 생성해주세요.", reference=ctx.message)
    return
  else:
    id = find_account_for_user(ctx.author.id)[0]
    if db[id][0] < value:
      await ctx.send("베팅할 금액이 너무 커요!", reference=ctx.message)
      return
    if value < 500:
      await ctx.send(f"베팅할 금액이 너무 작아요, 최소 베팅금액은 `{conversion(500)}` 입니다!", reference=ctx.message)
      return

  percent = random.randint(1, 20)
  if percent > 9:
    percent = random.randint(1, 10)
    if percent != 1:
      tasks = 4
    else:
      tasks = 5
  else:
    percent = random.randint(1, 10)
    if percent != 1:
      tasks = 1
    else:
      percent = random.randint(1, 4)
      if percent != 1:
        tasks = 2
      else:
        tasks = 3

  if tasks == 1:  # +베팅금액의 2배
    db[id][0] += value
    await ctx.send(f"축하해요, 2배로 성공했어요!\n`{conversion(value, 1)}`", reference=ctx.message)
  elif tasks == 2:  # +베팅금액의 3배
    value *= 2
    db[id][0] += value
    await ctx.send(f"부럽네요, 3배로 성공했어요!\n`{conversion(value, 1)}`", reference=ctx.message)
  elif tasks == 3:  # +베팅금액의 5배
    value *= 4
    db[id][0] += value
    if value >= 1000000:
      text = "어케했냐;;"
    else:
      text = "어..? 5배로 성공했어요!"
    await ctx.send(f"{text}\n`{conversion(value, 1)}`", reference=ctx.message)
  elif tasks == 4:  # -베팅금액
    db[id][0] -= value
    if value >= 100000:
      a = random.randint(1, 3)
      if a == 1:
        text = "음..! 정말 맛있네요.."
      if a == 2:
        text = "잘 먹었어요."
      if a == 3:
        text = "하하, 고마워요."
    else:
      a = random.randint(1, 3)
      if a == 1:
        text = "아쉽네요..!"
      if a == 2:
        text = "아앗.."
      if a == 3:
        text = "실패했네요.."
    await ctx.send(f"{text}\n`{conversion(value, -1)}`", reference=ctx.message)
  elif tasks == 5:  # -베팅금액의 반
    value //= 2
    db[id][0] -= value
    await ctx.send(f"실패..했지만 베팅금액의 반은 돌려드릴게요.\n`{conversion(value, -1)}`", reference=ctx.message)


@bot.command(aliases=["코인받기", "ㅋㅇㅂㄱ", "rdqr", "돈받기", "ㄷㅂㄱ", "eqr"])
async def get_coin(ctx):
  if find_account_for_user(ctx.author.id) == []:
    await ctx.send("계좌를 생성해야해요, `;가입` 으로 계좌를 생성해주세요.", reference=ctx.message)
    return

  id = find_account_for_user(ctx.author.id)[0]
  if db[id][0] > 10000:
    await ctx.send(f"`;코인받기` 는 보유금액이 `{conversion(10000)}`이하일때만 사용가능해요!", reference=ctx.message)
    return

  present_coin = random.randint(100, 250)*100
  db[id][0] += present_coin
  await ctx.send(f"선물이에요.\n`{conversion(present_coin, 1)}`", reference=ctx.message)


@bot.command(aliases=["올인", "ㅇㅇ", "dd"])
async def gamble_all_in(ctx):
  if find_account_for_user(ctx.author.id) == []:
    await ctx.send("계좌를 생성해야해요, `;가입` 으로 계좌를 생성해주세요.", reference=ctx.message)
    return
  id = find_account_for_user(ctx.author.id)[0]
  await gamble(ctx, db[id][0])


@bot.command(aliases=["하프", "ㅎㅍ", "gv"])
async def gamble_half(ctx):
  if find_account_for_user(ctx.author.id) == []:
    await ctx.send("계좌를 생성해야해요, `;가입` 으로 계좌를 생성해주세요.", reference=ctx.message)
    return
  id = find_account_for_user(ctx.author.id)[0]
  await gamble(ctx, db[id][0] // 2)


@bot.command(aliases=["돈복사", "ㄷㅂㅅ", "ㄷㅄ", "eqt"])
async def money_copy(ctx, amount: int):
  if find_account_for_user(ctx.author.id) == []:
    await ctx.send("계좌를 생성해야해요, `;가입` 으로 계좌를 생성해주세요.", reference=ctx.message)
    return
  if security(ctx.author.id) == False:
    await ctx.send("어..어라? 프린터기가 고장났네요..", reference=ctx.message)
    return

  id = find_account_for_user(ctx.author.id)[0]
  db[id][0] += amount
  embed = discord.Embed(title="복사한 돈을 전송했어요!", description="행복하시겠네요..")
  embed.add_field(name="복사한 금액", value=str(conversion(amount)))
  embed.add_field(name="전송계좌", value=str(id))
  embed.set_footer(text=f"{ctx.author} | Made by Choi Kang",
                   icon_url=str(ctx.author.avatar_url))
  await ctx.send(embed=embed, reference=ctx.message)


@bot.command()
async def data_show(ctx):
  if security(ctx.author.id) == False:
    return

  await ctx.send(str(list(db.keys())))


@bot.command()
async def data_delete(ctx, key: str):
    if security(ctx.author.id) == False:
        return

    del db[key]
    await ctx.send(f"Deleted data: key:{key}")


@bot.command()
async def data_set(ctx, key: str, amount: int):
  if security(ctx.author.id) == False:
    return

  db[key][0] = amount
  await ctx.send(f"Set data: [{key}] to [{amount}]")


@bot.command(aliases=["청소", "ㅊㅅㄴ", "cts"])
async def chat_clean(ctx, amount: int):
  if security(ctx.author.id) == False:
    return

  await ctx.message.delete()
  await ctx.channel.purge(limit=amount)

keep_alive()

def running(token):
  bot.run(token)
