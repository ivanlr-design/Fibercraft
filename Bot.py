from dotenv import load_dotenv, dotenv_values
from Utils.Database.AddPunishment import AddPunishment
from Utils.Database.SearchForUID import SearchForUid
from Utils.Database.GetTribeName import searchforTribename
from Utils.Database.RemovePunishment import RemovePunishment
from Utils.Database.CheckIfAuth import SeeIfAuthorized
from Utils.Database.AddAuthUser import AddAuthUser
from Utils.Database.TotalWarnings import TotalWarnings
from Utils.Database.WipeSeasonalWarnings import WipeSeasonalWarnigs
from Utils.Database.AddTempBan import AddTempBan
from Utils.Database.DeleteTempBan import RemoveTempBan
from Utils.Database.CheckTempBan import CheckBans
from Utils.Logs.Log import Log
from Utils.AutoRol import GetAllMembers
from Utils.MakeUID import MakeUID
from Utils.GetTime import GetTime
import discord
import typing
import re
from discord import app_commands
from discord.ext import commands
import pymysql
import asyncio
import os
import pymysql.cursors
load_dotenv(".env")
MYSQL_CONNECT = os.getenv("MYSQL_CONNECTOR")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWD = os.getenv("MYSQL_PASSWD")
BOT = os.getenv("BOT")
compiler = re.compile(r"[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9] [0-6][0-9]:[0-6][0-9]")
table1 = "Punishments"

def db_connection():
    connection = pymysql.connect(host=MYSQL_CONNECT,
                                user=MYSQL_USER,
                                password=MYSQL_PASSWD,
                                db='s51219_punish',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    return connection

bot = commands.Bot(command_prefix=".",intents=discord.Intents.all())

async def start():
    while True:
        await GetAllMembers(bot)
        connect = db_connection()
        await CheckBans(connect, bot, 1073357812786282536)
        connect.close()
        await asyncio.sleep(0.2)

@bot.event
async def on_ready():
    await bot.tree.sync()
    await start()

@bot.command()
async def AddAuthorizedUser(ctx, username):
    if str(ctx.author) != "ivanlr._1_45557":
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    user = discord.utils.get(ctx.guild.members, name=str(username))
    connection = db_connection()
    if user:
        id = user.id
        result = AddAuthUser(connection, username, id)
        connection.close()
        if result != True:
            embed = discord.Embed(title="Add Authorized User function",color=discord.Color.orange())
            embed.add_field(name="USER",value=username)
            embed.add_field(name="Error",value=f"User {username} ({result}) is already authorized")
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="Add Authorized User function",color=discord.Color.green())
            embed.add_field(name="USER",value=username)
            embed.add_field(name="DATABASE STATUS",value=f"Succesfully added to database!")
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(title="Add Authorized User function",color=discord.Color.red())
        embed.add_field(name="USER",value=username)
        embed.add_field(name="Error",value=f"User {username} does not exist in discord server")
        await ctx.send(embed=embed)
        return

@bot.tree.command(name="removetempban",description="remove temp ban")
async def removetempban(interaction : discord.Interaction, uid : str):
    connection = db_connection()
    name = interaction.user.name
    Userid = SeeIfAuthorized(connection, name)
    if Userid == False:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    elif Userid != interaction.user.id:
        embed = discord.Embed(title="Error",description="Your discord id does not match the database!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    
    dele = RemoveTempBan(connection, uid)
    if dele == False:
        embed = discord.Embed(title="Error",description=f"Can't find uid : {uid}",color=discord.Color.red())
        connection.close()
        await interaction.response.send_message(embed=embed)
        return
    else:
        embed = discord.Embed(title=dele[0]['TribeName'],description="",color=discord.Color.green())
        embed.add_field(name="Names",value=dele[0]['Names'],inline=False)
        embed.add_field(name="Ids",value=dele[0]['SteamIDs'],inline=False)
        embed.add_field(name="Reason",value=dele[0]['Reason'],inline=False)
        embed.add_field(name="Made",value=dele[0]['Made'],inline=False)
        embed.add_field(name="Author",value=dele[0]['Author'],inline=False)
        connection.close()
        await interaction.response.send_message(embed=embed)
        return

@bot.tree.command(name="tempban",description="add temp ban")
async def tempban(interaction : discord.Interaction, names : str, ids : str, tribename : str, reason : str, unbandate : str):
    connection = db_connection()
    name = interaction.user.name
    Userid = SeeIfAuthorized(connection, name)
    if Userid == False:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    elif Userid != interaction.user.id:
        embed = discord.Embed(title="Error",description="Your discord id does not match the database!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    
    if not re.match(compiler, unbandate):
        embed = discord.Embed(title="Date MUST be in the correct format, ex: 12/02/2024",description="The numbers must be in two numbers always, this : 12/2/2024 is INVALID, MUST be 12/02/2024",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return 
    name = interaction.user.name
    uid = MakeUID()
    result = AddTempBan(connection, names, ids, tribename, reason, unbandate, uid, name, GetTime())
    
    if result == True:
        embed = discord.Embed(title="TEMP BANNED!",description="",color=discord.Color.dark_magenta())
        embed.add_field(name="Tribe Name",value=tribename, inline=False)
        embed.add_field(name="IDs",value=ids, inline=False)
        embed.add_field(name="Names",value=names, inline=False)
        embed.add_field(name="Reason",value=reason, inline=False)
        embed.add_field(name="UnbanDate",value=unbandate, inline=False)
        embed.set_footer(text=f"UID : {uid}")
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    else:
        embed = discord.Embed(title="Error!",description="Please contact ivan and send screenshot so thi can be fixed!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return

@bot.tree.command(name="searchforpunishments",description="search for punishments by uid,Tribe name")
async def searchforpunishments(interaction : discord.Interaction, tribename_or_uid : str):
    connection = db_connection()
    name = interaction.user.name
    Userid = SeeIfAuthorized(connection, name)
    if Userid == False:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    elif Userid != interaction.user.id:
        embed = discord.Embed(title="Error",description="Your discord id does not match the database!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    
    resultuid = SearchForUid(connection, tribename_or_uid)

    if resultuid == False:
        resultname = searchforTribename(connection, tribename_or_uid)
        if resultname == False:
            embed = discord.Embed(title="not found",description=f"{tribename_or_uid} was not found!",color=discord.Color.red())
            connection.close()
            await interaction.response.send_message(embed=embed)
            connection.close()
            return
        warning = 1
        embed = discord.Embed(title=tribename_or_uid,color=discord.Color.orange())
        UIDS = []
        for result in resultname:   
            Names = result['Names']
            IDs = result['SteamIDS']
            Reason = result['Reason']
            Punishment = result['Punishment']
            Warning_type = result['Warning_type']
            Warnings = result['Warnings']
            UIDS.append(result['UID'])
            embed.add_field(name=f"Warning : {warning}",value="",inline=False)
            embed.add_field(name="Names",value=Names)
            embed.add_field(name="IDs",value=IDs)
            embed.add_field(name="Warning type",value=Warning_type)
            embed.add_field(name="Warnings",value=Warnings)
            embed.add_field(name="Punishment",value=Punishment)
            embed.add_field(name="Reason",value=Reason)
            warning += 1
        connection.close()
        UIDS = ', '.join(UIDS)
        embed.set_footer(text=f"UIDS : {UIDS}")
        await interaction.response.send_message(embed=embed)
        return
    else:
        warning = 1
        embed = discord.Embed(title=tribename_or_uid,color=discord.Color.orange())
        UIDS = []
        for result in resultuid:   
            Names = result['Names']
            TribeName = result['TribeName']
            IDs = result['SteamIDS']
            Reason = result['Reason']
            Punishment = result['Punishment']
            Warning_type = result['Warning_type']
            Warnings = result['Warnings']
            UIDS.append(result['UID'])
            embed.add_field(name=f"Warning : {warning}",value="",inline=False)
            embed.add_field(name="Names",value=Names)
            embed.add_field(name="Tribe Name",value=TribeName)
            embed.add_field(name="IDs",value=IDs)
            embed.add_field(name="Warning type",value=Warning_type)
            embed.add_field(name="Warnings",value=Warnings)
            embed.add_field(name="Punishment",value=Punishment)
            embed.add_field(name="Reason",value=Reason)
            warning += 1
        connection.close()
        UIDS = ', '.join(UIDS)
        embed.set_footer(text=f"UIDS : {UIDS}")
        await interaction.response.send_message(embed=embed)
        return

@bot.tree.command(name="wipeseasonalwarnings",description="perform a seasonal warning wipe")
async def wipeseasonalwarnings(interaction : discord.Interaction):
    connection = db_connection()
    name = interaction.user.name
    Userid = SeeIfAuthorized(connection, name)
    if Userid == False:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    elif Userid != interaction.user.id:
        embed = discord.Embed(title="Error",description="Your discord id does not match the database!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    Log(f"[{interaction.user.name}] - PERFORMED A WIPE SEASONAL WARNINGS!!!!!!")
    await interaction.response.defer()
    await WipeSeasonalWarnigs(connection, bot, interaction.channel_id)
    connection.close()

@bot.tree.command(name="removepunishment",description="Temp ban a user, date example 16/02/2024 15:24")
async def removepunishment(interaction : discord.Interaction, warning_uid : str):
    connection = db_connection()
    name = interaction.user.name
    Userid = SeeIfAuthorized(connection, name)
    if Userid == False:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    elif Userid != interaction.user.id:
        embed = discord.Embed(title="Error",description="Your discord id does not match the database!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    
    results = SearchForUid(connection, warning_uid)
    uid = RemovePunishment(connection, warning_uid)
    if uid == False:
        embed = discord.Embed(title="Invalid UID provided",description="Invalid UID was provided, if you think this was an error please contact ivanlr._1_45557 providing the UID so he can remove it manually!",color=discord.Color.red())
        connection.close()
        await interaction.response.send_message(embed=embed)
    else:
        TribeName = results[0]['TribeName']
        Reason = results[0]['Reason']
        Punishment = results[0]['Punishment']
        embed = discord.Embed(title=f"UID WAS REMOVED",description=f"UID : {warning_uid} was removed",color=discord.Color.green())
        embed.add_field(name="Tribe Name",value=TribeName,inline=False)
        embed.add_field(name="Reason",value=Reason,inline=False)
        embed.add_field(name="Punishment",value=Punishment,inline=False)
        Log(f"[{interaction.user.name}] - removed a punishment, uid : {warning_uid}")
        connection.close()
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="totalwarnigns",description="Temp ban a user, date example 16/02/2024 15:24")
async def totalwarnigns(interaction : discord.Interaction, tribename : str):
    connection = db_connection()
    name = interaction.user.name
    Userid = SeeIfAuthorized(connection, name)
    if Userid == False:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    elif Userid != interaction.user.id:
        embed = discord.Embed(title="Error",description="Your discord id does not match the database!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    
    Log(f"[{interaction.user.name}] - perform totalwarnings commands searching for : {tribename}")
    warnings = TotalWarnings(connection, tribename=tribename)
    if warnings != False:
        seasonals, permanent, verbal = warnings
        embed = discord.Embed(title=tribename, color=discord.Color.green())
        embed.add_field(name="Seasonal Warnings",value=seasonals,inline=True)
        embed.add_field(name="Permanent Warnings",value=permanent,inline=True)
        embed.add_field(name="Verbal Warnings",value=verbal,inline=True)
        connection.close()
        await interaction.response.send_message(embed=embed)
        return
    else:
        connection.close()
        embed = discord.Embed(title="Tribe does not have warnings!",color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
        return

@bot.tree.command(name="punishment",description="Temp ban a user, date example 16/02/2024 15:24")
async def punishment(interaction : discord.Interaction, names : str, ids : str, tribename : str, reason : str, punishment : str, warning_type : str, warnings : int, proof : str):
    name = interaction.user.name
    connection = db_connection()
    Userid = SeeIfAuthorized(connection, name)
    if Userid == False:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    elif Userid != interaction.user.id:
        embed = discord.Embed(title="Error",description="Your discord id does not match the database!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        connection.close()
        return
    
    while True:
        uid = MakeUID()
        search = SearchForUid(connection, uid)
        if search == False:
            break

    worked = AddPunishment(connection, names, ids, reason, tribename, punishment, warning_type, warnings, uid)

    if worked == True:
        embed = discord.Embed(title="PUNISH",color=discord.Color.orange())
        embed.add_field(name="Tribe Name",value=tribename,inline=False)
        embed.add_field(name="Names",value=names,inline=False)
        embed.add_field(name="Steam IDs",value=ids,inline=False)
        embed.add_field(name="Warning Type",value=warning_type,inline=False)
        embed.add_field(name="Warnings",value=warnings,inline=False)
        embed.add_field(name="Reason",value=reason,inline=False)
        embed.add_field(name="Punishment",value=punishment,inline=False)
        embed.add_field(name="Proof",value=proof,inline=False)
        embed.add_field(name="DATABASE STATUS",value="Succesfully added to database",inline=False)
        embed.set_thumbnail(url="https://th.bing.com/th/id/R.a1849d676a332b5516f3dd3cf3d90609?rik=XwaA15sdUDGrag&riu=http%3a%2f%2fwww.freepngimg.com%2fdownload%2fgreen_tick%2f27880-5-green-tick-clipart.png&ehk=23wDe1sjBvA6xbwbaYRnxtE0tnwNzqbafc3L5kmYcms%3d&risl=&pid=ImgRaw&r=0")
        embed.set_footer(text=f"UID : {uid}, coded by Ivan")
        Log(f"[{interaction.user.name}] - made a punishment under the uid : {uid}")
        connection.close()
        await interaction.response.send_message(embed=embed)
    else:
        embed =discord.Embed(title="FATAL ERROR IN DATABSE",description=f"Please contact ivanlr providing this message and time",color=discord.Color.red())
        connection.close()
        await interaction.response.send_message(embed=embed)
        return

@punishment.autocomplete("warning_type")
async def autocomplete(interaction : discord.Interaction, current : str) -> typing.List[app_commands.Choice[str]]:
    data = []
    for options in ["Seasonal Warning","Permanent Warning","Verbal Warning"]:
        data.append(app_commands.Choice(name=options,value=options)) 
    return data 

@punishment.autocomplete("warnings")
async def warn_autocomplete(interaction : discord.Interaction, current: int) -> typing.List[app_commands.Choice[int]]:
    data = []
    for number in [1,2,3,4,5]:
        data.append(app_commands.Choice(name=number,value=number))
    
    return data

if os.path.exists("Logs.txt"):
    pass
else:
    with open("Logs.txt","w") as file:
        file.close()

bot.run(BOT)
