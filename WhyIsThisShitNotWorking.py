from dotenv import load_dotenv, dotenv_values
from Utils.Database.AddPunishment import AddPunishment
from Utils.Database.SearchForUID import SearchForUid
from Utils.Database.GetTribeName import searchforTribename
from Utils.Database.RemovePunishment import RemovePunishment
from Utils.Database.CheckIfAuth import SeeIfAuthorized
from Utils.Database.AddAuthUser import AddAuthUser
from Utils.Database.TotalWarnings import TotalWarnings
from Utils.MakeUID import MakeUID
import discord
import typing
from discord import app_commands
from discord.ext import commands
import pymysql
import os
import pymysql.cursors
load_dotenv(".env")
MYSQL_CONNECT = os.getenv("MYSQL_CONNECTOR")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWD = os.getenv("MYSQL_PASSWD")
BOT = os.getenv("BOT")

table1 = "Punishments"
connection = pymysql.connect(host=MYSQL_CONNECT,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWD,
                             db='s51219_punish',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

bot = commands.Bot(command_prefix=".",intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.command()
async def AddAuthorizedUser(ctx, username):
    if str(ctx.author) != "ivanlr._1_45557":
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    user = discord.utils.get(ctx.guild.members, name=str(username))

    if user:
        id = user.id
        result = AddAuthUser(connection, username, id)
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

@bot.tree.command(name="removepunishment",description="Temp ban a user, date example 16/02/2024 15:24")
async def removepunishment(interaction : discord.Interaction, warning_uid : str):
    name = interaction.user.name
    Userid = SeeIfAuthorized(connection, name)
    if Userid == False:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    elif Userid != interaction.user.id:
        embed = discord.Embed(title="Error",description="Your discord id does not match the database!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    results = SearchForUid(connection, warning_uid)
    uid = RemovePunishment(connection, warning_uid)
    if uid == False:
        embed = discord.Embed(title="Invalid UID provided",description="Invalid UID was provided, if you think this was an error please contact ivanlr._1_45557 providing the UID so he can remove it manually!",color=discord.Color.red())

        await interaction.response.send_message(embed=embed)
    else:
        TribeName = results[0]['TribeName']
        Reason = results[0]['Reason']
        Punishment = results[0]['Punishment']
        embed = discord.Embed(title=f"UID WAS REMOVED",description=f"UID : {uid} was removed",color=discord.Color.green())
        embed.add_field(name="Tribe Name",value=TribeName,inline=False)
        embed.add_field(name="Reason",value=Reason,inline=False)
        embed.add_field(name="Punishment",value=Punishment,inline=False)

        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="totalwarnigns",description="Temp ban a user, date example 16/02/2024 15:24")
async def totalwarnigns(interaction : discord.Interaction, tribename : str):
    name = interaction.user.name
    Userid = SeeIfAuthorized(connection, name)
    if Userid == False:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    elif Userid != interaction.user.id:
        embed = discord.Embed(title="Error",description="Your discord id does not match the database!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    warnings = TotalWarnings(connection, tribename=tribename)
    if warnings != False:
        seasonals, permanent, verbal = warnings
        embed = discord.Embed(title=tribename, color=discord.Color.green())
        embed.add_field(name="Seasonal Warnings",value=seasonals,inline=True)
        embed.add_field(name="Permanent Warnings",value=permanent,inline=True)
        embed.add_field(name="Verbal Warnings",value=verbal,inline=True)
        await interaction.response.send_message(embed=embed)
        return
    else:
        embed = discord.Embed(title="Tribe does not have warnings!",color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
        return

@bot.tree.command(name="punishment",description="Temp ban a user, date example 16/02/2024 15:24")
async def punishment(interaction : discord.Interaction, names : str, ids : str, tribename : str, reason : str, punishment : str, warning_type : str, warnings : int, proof : str):
    name = interaction.user.name
    Userid = SeeIfAuthorized(connection, name)
    if Userid == False:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    elif Userid != interaction.user.id:
        embed = discord.Embed(title="Error",description="Your discord id does not match the database!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    while True:
        uid = MakeUID()
        search = SearchForUid(connection, uid)
        if search != False:
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
        await interaction.response.send_message(embed=embed)
    else:
        embed =discord.Embed(title="FATAL ERROR IN DATABSE",description=f"Please contact ivanlr providing this message and time",color=discord.Color.red())
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

bot.run(BOT)
