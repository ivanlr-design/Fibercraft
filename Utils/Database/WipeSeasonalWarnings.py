import pymysql
import pymysql.cursors
import discord
import asyncio
import time
from discord.ext import commands
async def WipeSeasonalWarnigs(connection : pymysql.connect, bot : commands.Bot, channel_id):
    cursor = connection.cursor()
    channel = bot.get_channel(channel_id)
    consulta = "SELECT * FROM Punishments WHERE Warning_type = 'Seasonal Warning'"

    cursor.execute(consulta)
    resultados = cursor.fetchall()
    embed = discord.Embed(title="Wiping Seasonal Warnings...",description="```Obtaining results```",color=discord.Color.green())
    msj = await channel.send(embed=embed)
    delete = []
    start = time.time()
    for result in resultados:
        UID = result['UID']
        embed = discord.Embed(title="Wiping Seasonal Warnings...",description=f"```Fetched : {UID}```",color=discord.Color.orange())
        await msj.edit(embed=embed)
        delete.append(UID)
        await asyncio.sleep(0.5)
    
    embed = discord.Embed(title="Wiping Seasonal Warnings...",description=f"```Fetched all results, fetched : {len(delete)} in {round(time.time() - start,2)}s```",color=discord.Color.green())
    await msj.edit(embed=embed)

    for uid in delete:
        consulta = "DELETE FROM Punishments WHERE UID = %s"
        try:
            cursor.execute(consulta, (uid, ))
            connection.commit()
            embed = discord.Embed(title="Wiping Seasonal Warnings...",description=f"```{uid} was deleted sucessfully!```",color=discord.Color.green())
            await msj.edit(embed=embed)
        except:
            embed = discord.Embed(title="Wiping Seasonal Warnings...",description=f"```Error deleting: {uid}```",color=discord.Color.red())
            
            await msj.edit(embed=embed)
    
    await asyncio.sleep(1)

    embed = discord.Embed(title="Wiped seasonal warnings",description=f"```All seasonal warnings were deleted sucessfully!```",color=discord.Color.green())
    await msj.edit(embed=embed)