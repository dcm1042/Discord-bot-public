"""
This cog defines the on_member_join function to allow people to go through a registration processg
"""

from discord.ext import commands
from collections.abc import Sequence
import discord
import requests
import json

def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)


def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)

    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True

    return check


class OnJoinCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def ask_purpose(self,member ):
        """
        Request member/nonmember
        """
        await member.send("Are you a student or faculty who intends to be an active part of the club? (Y/N) (Answer No "
                          "if you are here to collaborate with the club on events, and are not a faculty member. "
                          "Otherwise answer yes)")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        response = response.content
        response.upper()
        if "Y" in response:
            return True
        if "N" in response:
            role = discord.utils.get(member.guild.roles, name="non-member")
            await member.add_roles(role)
            return False
        else:
            await member.send(
                "Are you a student who intends to be a member, or faculty who intends to be an active part of the club? (Y/N) (Answer No"
                "if you are here to collaborate with the club on events, or some other non-member position, and are not a faculty member. Otherwise"
                "answer yes)")
            await self.ask_purpose(member)

    async def ask_faculty(self, member):
        """
        Request faculty info
        """
        await member.send("Are you a faculty member? (Y/N)")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        response = response.content
        response.upper()
        if 'Y' in response:
            role = discord.utils.get(member.guild.roles, name="Faculty")
            await member.add_roles(role)
            return "faculty"
        if 'N' in response:
            role = discord.utils.get(member.guild.roles, name="Club Member")
            await member.add_roles(role)
            return "Member"
        else:
            await member.send("invalid response")
            await self.ask_faculty(member)

    async def ask_github(self, member):
        """
        Request github username
        """
        await member.send("Please respond with your github username!")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        return response.content

    async def ask_name(self, member):
        """
        Request Name Info
        """
        await member.send("Please respond with your first name as you would like it to appear on the server!")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        await member.edit(nick=response.content)
        return response.content

    async def ask_campus(self, member):
        """
        request campus info
        """
        await member.send("Are you a UNH Manchester, or UNH Durham student? (UNHM/UNHD)")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        response = response.content
        response.upper()
        if "UNHM" in response:
            role = discord.utils.get(member.guild.roles, name="UNHM students")
            await member.add_roles(role)
            return "UNHM"
        if "UNHD" in response:
            return "UNHD"
        else:
            await member.send("Invalid response!")
            await self.ask_campus(member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Runs on member join, asks them various questions about their position in the club
        """
        await member.send("Welcome to the UNHM programming club! I need to ask you a few questions to assign your"
                          "discord roles first!") # send welcoming message
        purpose = await self.ask_purpose(member) #ask their purpose, non-member/member
        name = await self.ask_name(member) # ask for name
        if purpose: # if they are a member
            mem_or_fac = await self.ask_faculty(member) # are they faculty or student?
            if mem_or_fac != "faculty": # if their not faculty
                campus = await self.ask_campus(member) # get their campus
            else:
                campus = "N/A" # if their faculty campus is not applicable
            github = await self.ask_github(member) # ask for github
            with open('members.txt', 'a') as file: # save this info to a text file
                file.write(f"Name: {name} Github: {github} , {mem_or_fac}, Campus: {campus}\n")
            embed = { # create an embed message as json
                "description": f"Name: {name}\nRole: {mem_or_fac}\nCampus: {campus}\nGithub: {github}",
                "title": "New Member"
            }

            data = { # form the rest of the message and define bot name as json
                "content": f"New Member!",
                "username": "New Member Bot",
                "embeds": [
                    embed
                ],
            }

            result = requests.post("https://discord.com/api/webhooks/826631969701625906/vfIcKFbeLnBdJD1hFS6tsuPrCWArDb4sv38O8piWgccRLqIxdovE6rsUyDn5Rw4JRsJE", json=data) # send webhook request
            try: # all of this is for debugging
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Payload delivered successfully, code {}.".format(result.status_code))
        else: # if their a non- member
            # form the discord embed message as json
            embed = {
                "description": f"Name: {name}",
                "title": "New Non-Member"
            }

            data = {
                "content": f"New Non-Member Info",
                "username": "New Non-Member Bot",
                "embeds": [
                    embed
                ],
            }
            # send discord message
            result = requests.post("https://discord.com/api/webhooks/826631969701625906/vfIcKFbeLnBdJD1hFS6tsuPrCWArDb4sv38O8piWgccRLqIxdovE6rsUyDn5Rw4JRsJE", json=data)
            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Payload delivered successfully, code {}.".format(result.status_code))
        await member.send("Thank you for completing registration!") # tell them registration is complete

    @commands.command(pass_context=True)
    async def manual_reg(self, ctx):
        """
        Manually start registration in case of bot error
        """
        user = ctx.message.author
        print(user)
        await self.on_member_join(user)

    @commands.command(pass_context=True)
    async def get_registered(self, ctx):
        """
        return all registered members from text file
        """
        with open('members.txt', 'r') as file:
            lines = file.readlines()
        message_str = ""
        for line in lines:
            message_str += f"{line}\n"
        await ctx.send(f"```{message_str}"
                       f"```")


def setup(client):
    client.add_cog(OnJoinCog(client))


