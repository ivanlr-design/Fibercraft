import discord
from discord.ext import commands
Support1 = 928325966600761376
Support2 = 960193798460297246
Support3 = 960193866554822736
Support4 = 1024761069610213496

In_channel_1 = []
In_channel_2 = []
In_channel_3 = []
In_channel_4 = []

async def GetAllMembers(bot : commands.Bot):
    for guild in bot.guilds:
        voice_channel = discord.utils.get(guild.voice_channels, id=Support1)
        Sup2 = discord.utils.get(guild.voice_channels, id=Support2)
        Sup3 = discord.utils.get(guild.voice_channels, id=Support3)
        Sup4 = discord.utils.get(guild.voice_channels, id=Support4)
        if voice_channel:
            members = voice_channel.members
            for member in members:
                if member.name not in In_channel_1:
                    In_channel_1.append(member.name)
                    for guild in bot.guilds:
                        role = discord.utils.get(guild.roles, name="Support 1")
                        member = discord.utils.get(guild.members, name=member.name)
                        if role and member:
                            await member.add_roles(role)

            for user in In_channel_1:
                if str(user) not in str(members):
                    role = discord.utils.get(guild.roles, name="Support 1")
                    member = discord.utils.get(guild.members, name=user)
                    if role and member:
                        await member.remove_roles(role)
                        In_channel_1.remove(user)
        if Sup2:
            members = Sup2.members
            for member in members:
                if member.name not in In_channel_2:
                    In_channel_2.append(member.name)
                    for guild in bot.guilds:
                        role = discord.utils.get(guild.roles, name="Support 2")
                        member = discord.utils.get(guild.members, name=member.name)
                        if role and member:
                            await member.add_roles(role)

            for user in In_channel_2:
                if str(user) not in str(members):
                    role = discord.utils.get(guild.roles, name="Support 2")
                    member = discord.utils.get(guild.members, name=user)
                    if role and member:
                        await member.remove_roles(role)
                        In_channel_2.remove(user)
        
        if Sup3:
            members = Sup3.members
            for member in members:
                if member.name not in In_channel_3:
                    In_channel_3.append(member.name)
                    for guild in bot.guilds:
                        role = discord.utils.get(guild.roles, name="Support 3")
                        member = discord.utils.get(guild.members, name=member.name)
                        if role and member:
                            await member.add_roles(role)

            for user in In_channel_3:
                if str(user) not in str(members):
                    role = discord.utils.get(guild.roles, name="Support 3")
                    member = discord.utils.get(guild.members, name=user)
                    if role and member:
                        await member.remove_roles(role)
                        In_channel_3.remove(user)
        
        if Sup4:
            members = Sup4.members
            for member in members:
                if member.name not in In_channel_4:
                    In_channel_4.append(member.name)
                    for guild in bot.guilds:
                        role = discord.utils.get(guild.roles, name="Support 4")
                        member = discord.utils.get(guild.members, name=member.name)
                        if role and member:
                            await member.add_roles(role)

            for user in In_channel_4:
                if str(user) not in str(members):
                    role = discord.utils.get(guild.roles, name="Support 4")
                    member = discord.utils.get(guild.members, name=user)
                    if role and member:
                        await member.remove_roles(role)
                        In_channel_4.remove(user)