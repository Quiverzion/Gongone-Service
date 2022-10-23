import discord
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix=';',
                   status=discord.Status.online, intents=discord.Intents.all())

intents = discord.Intents.all()

@bot.event
async def on_ready():
    print(f'Qhwhkrhks: Script Runned on [{bot.user}]')
    info_setting.start()

@tasks.loop(seconds=1)
async def info_setting():
    guild = bot.get_guild(1031900696632639488)
    await bot.get_channel(1032278211016527892).edit(name=f"🎈┃현 부대규모: {guild.member_count}명")


@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)

    if ctx.author.id == bot.user.id:
        return

    bot_banChannel = [1031918233525174334, 1031900697102385196]
    bot_Channel = 1031905167353860106
    for c in bot_banChannel:
        if ctx.channel.id == c:
            if ctx.content[0] == "!" and len(ctx.content) >= 2:
                await ctx.channel.send(f"군악대는 여기서 사용해주십시오. <#{bot_Channel}>", reference=ctx)
                return

@bot.command()
async def clean(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    if ctx.author.dm_channel is None:
        channel = await ctx.author.create_dm()
    else:
        channel = ctx.author.dm_channel
    await channel.send(f"{ctx.author.mention} 채팅 {amount}개가 삭제되었습니다.")

@bot.command()
async def levelup(ctx, target:int):
    await ctx.message.delete()
    report_channel = bot.get_channel(1033578409936310334)

    target_member = bot.get_guild(1031900696632639488).get_member(target)
    target_user = bot.get_user(target)

    role_trainee = bot.get_guild(1031900696632639488).get_role(1031921811035791381)
    role_b_one = bot.get_guild(1031900696632639488).get_role(1031920357948530740)
    role_b_two = bot.get_guild(1031900696632639488).get_role(1031920409198743634)
    role_b_three = bot.get_guild(1031900696632639488).get_role(1031920441427755038)
    role_b_four = bot.get_guild(1031900696632639488).get_role(1031919602889924608)

    if target_member.roles[1] == role_trainee:
        await target_member.remove_roles((role_trainee))
        await target_member.add_roles((role_b_one))
        if target_user.dm_channel is None:
            channel = await target_user.create_dm()
        else:
            channel = target_user.dm_channel
        await channel.send(f"{target_user.mention} 축하합니다. **'이병'**으로 승급하였습니다.")
        await report_channel.send(f"> {target_user.mention}이(가) **'훈련병'**에서 **'이병'**으로 승급하였습니다.")

    elif target_member.roles[1] == role_b_one:
        await target_member.remove_roles((role_b_one))
        await target_member.add_roles((role_b_two))
        if target_user.dm_channel is None:
            channel = await target_user.create_dm()
        else:
            channel = target_user.dm_channel
        await channel.send(f"{target_user.mention} 축하합니다. **'일병'**으로 승급하였습니다.")
        await report_channel.send(f"> {target_user.mention}이(가) **'이병'**에서 **'일병'**으로 승급하였습니다.")

@bot.command()
async def rts(ctx):
    await ctx.message.delete()
    await ctx.channel.send()

bot.run("MTAzMjYzNzc2MzY2MjY0NzM0Nw.GodkWN.V2caLHRpX3BM-REB2pWcFO_BU3F7az9biGYukg")