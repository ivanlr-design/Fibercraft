import pymysql
import pymysql.cursors
import discord
from discord.ext import commands
from ..GetTime import GetTime

async def CheckBans(connector : pymysql.connect, bot : commands.Bot, channel_id):
    try:
        cursor = connector.cursor()
        consulta = f"SELECT * FROM TempBans"

        cursor.execute(consulta)
        results = cursor.fetchall()
        for result in results:
            if str(result['UnbanDate']) == str(GetTime()):
                UID = result['UID']
                Author = result['Author']
                Made = result['Made']
                TribeName = result['TribeName']
                SteamIDs = result['SteamIDs']
                embed = discord.Embed(title=F"Hey, U need to UNBAN this tribe:{TribeName}, with IDs : {SteamIDs}. You made this ban {Made}",description="",color=discord.Color.gold())
                user = discord.utils.get(bot.users, name=str(Author))
                channel = bot.get_channel(channel_id)
                await channel.send(embed=embed)
                await channel.send(user.mention)
                consulta2 = "DELETE FROM TempBans WHERE UID = %s"
                VALORES = (UID,)
                cursor.execute(consulta2, VALORES)
                connector.commit()

    except Exception as e:
        print(e)
        pass