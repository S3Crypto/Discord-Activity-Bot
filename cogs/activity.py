import platform

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, activityHelper

import csv
import io


# Here we name the cog and create a new class for the cog.
class Activity(commands.Cog, name="activity"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="checkactivity",
        description="This is a testing command that does nothing.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    @checks.is_owner()
    async def serverinfo(self, context: Context) -> None:
        """
        Get information about the server.

        :param context: The hybrid command context.
        """
        memDict = {}

        text_channels = activityHelper.filterChannels(context.guild.channels)
        all_messages = await activityHelper.getMessages(text_channels)

        # Create a CSV file in-memory
        csv_file = io.StringIO()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Name', 'Idle Time', 'Message Percentage'])

        for member in context.guild.members:
            memDict["Name"] = member.name
            user_last_message = activityHelper.getLastMessage(all_messages, member)
            time_idle = activityHelper.checkIdleTime(user_last_message.created_at.replace(tzinfo = None))
            idle_time = activityHelper.generateIdleMessage(time_idle)
            message_percentage = activityHelper.calculateUserMessagePercentage(all_messages,member) 
            # Write a row to the CSV file for each member
            csv_writer.writerow([member.name, idle_time, f"{message_percentage:.2f}%"])
        
        # Reset the file pointer to the beginning of the file
        csv_file.seek(0)

        embed = discord.Embed(
            title="**Server Name:**", description=f"{context.guild}", color=0x9C84EF
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", value=f"{len(context.guild.channels)}"
        )
        #embed.add_field(name="Members", value=memDict)

        await context.send(embed=embed, file=discord.File(csv_file, filename="members.csv"))


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Activity(bot))
