import asyncio
import random
import os
import discord
import time
from discord import Member, Guild

client = discord.Client()
#########################################################################
antworten = ['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich',
             'Sehr unwahrscheinlich']


@client.event
async def on_ready():
    print('Wir sind eingeloggt als User {}'.format(client.user.name))
    client.loop.create_task(status_task())


async def status_task():
    colors = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(),
              discord.Colour.blue(), discord.Colour.purple()]
    while True:
        await client.change_presence(activity=discord.Game('Ersteller Canned Heat'), status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game('Mein cooler Bot!'), status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game('rainbow!help für Hilfe'), status=discord.Status.online)
        await asyncio.sleep(5)
        if client.get_guild(640618905030754338):
            guild: Guild = client.get_guild(640618905030754338)
            role = guild.get_role(677575400548859904)
            if role:
                if role.position < guild.get_member(client.user.id).top_role.position:
                    await role.edit(colour=random.choice(colors))


def is_not_pinned(mess):
    return not mess.pinned


@client.event
#WIll ich das haben?
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith ('rainbow!help'):
        await message.channel.send('**Hilfe zum PyBot**\r\n'
                                   '**rainbow!help** - Zeigt diese Hilfe an\r\n'
                                   '**rainbow!userinfo + Name des gewünschten Users** - Zeigt Infos zu dem User an\r\n'
                                   '**rainbow!8ball + Frage** - Der Bot antwortet zufällig auf deine Frage\r\n'
                                   '**rainbow!clear + Anzahl der Nachrichten, die gelöscht werden sollen** - Löscht die angegebene Anzahl von Nachrichten\r\n'
                                   '**rainbow!privatehelp** - Du bekommst die Hilfe per DM zugesendet\r\n'
                                   '**rainbow!ping + Nachricht** - Pingt die Nachricht, die du mit einem Leerzeichen nach rainbow!ping geschrieben hast\r\n'
                                   '**rainbow!tempping + Nachricht** - Pingt die Nachricht, die du mit einem Leerzeichen nach rainbow!ping geschrieben hast für 5 Sekunden\r\n'

                                   )
    if 'rainbow!privatehelp' in message.content:
        await message.channel.send ('Du hast die Hilfe per DM erhalten.:thumbsup:')
        await message.author.send('> **Hilfe zum PyBot**\r\n'
                                   '> **rainbow!help** - Zeigt diese Hilfe an\r\n'
                                   '> **rainbow!userinfo** + Name des gewünschten Users - Zeigt Infos zu dem User an\r\n'
                                   '> **rainbow!8ball + Frage** - Der Bot antwortet zufällig auf deine Frage\r\n'
                                   '> **rainbow!clear + Anzahl der Nachrichten, die gelöscht werden sollen** - Löscht die angegebene Anzahl von Nachrichten\r\n'
                                   '> **rainbow!privatehelp** - Du bekommst die Hilfe per DM zugesendet\r\n'
                                   '> **rainbow!ping + Nachricht** - Pingt die Nachricht, die du mit einem Leerzeichen nach rainbow!ping geschrieben hast\r\n'
                                   '> **rainbow!tempping + Nachricht** - Pingt die Nachricht, die du mit einem Leerzeichen nach rainbow!ping geschrieben hast für 5 Sekunden\r\n'

                                   )
    if message.content.startswith('rainbow!pin'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                Pin = str(args[1])
                Autor = message.author
                autormention = Autor.mention
                await message.author.send('{} Deine Nachricht: {} wurde angepinnt'.format(autormention, args[1]))
                message = await message.channel.send ('{}'.format(args [1]))
                await message.pin()
        if not message.author.permissions_in(message.channel).manage_messages:
            autormention = Autor.mention
            await message.channel.send ('{} Dir fehlen leider die Berechtigungen, um diesen Befehl auszuführen!'.format(autormention))
        if not len(args) == 2:
            aa = message.author.mention
            await message.channel.send('{} Fehler! Du hast keine Nachricht angegeben'.format(aa))
    if message.content.startswith('rainbow!temppin'):
        args = message.content.split(' ')
        if len(args) == 2:
            aa = message.author.mention
            await message.author.send('{} Deine Nachricht: {} wird für 10 Sekunden angepinnt'.format(aa, args[1]))
            message = await message.channel.send('{}'.format(args[1]))
            await message.pin()
            time.sleep(10)
            await message.unpin()
        if not len(args) == 2:
            aa = message.author.mention
            await message.channel.send('{} Fehler! Du hast keine Nachricht angegeben'.format(aa))
    if message.content.startswith('rainbow!userinfo'):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Userinfo für {}'.format(member.name),
                                      description='Dies ist eine Userinfo für den User {}'.format(member.mention),
                                      color=0x22a7f0)
                embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                rollen = ''
                for role in member.roles:
                    if not role.is_default():
                        rollen += '{} \r\n'.format(role.mention)
                if rollen:
                    embed.add_field(name='Rollen', value=rollen, inline=True)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text='Ich bin ein EmbedFooter.')
                mess = await message.channel.send(embed=embed)
                await mess.add_reaction(
                    '<img draggable="false" role="img" class="emoji" alt="🚍" src="https://s.w.org/images/core/emoji/12.0.0-1/svg/1f68d.svg">')
                await mess.add_reaction('a:hearts: 662606955520458754')
    if message.content.startswith('rainbow!clear'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send('{} Nachrichten gelöscht.'.format(len(deleted) - 1))
            if not len(args) == 2:
                await message.channel.send('Du hast leider keine oder zuviele Zahlen angegeben.')
        if not message.author.permissions_in(message.channel).manage_messages:
            await message.channel.send('{} Dir fehlen leider die Berechtigungen, um diesen Befehl auszuführen!'.format(member.mention))
    if message.content.startswith('rainbow!8ball'):
        args = message.content.split(' ')
        if len(args) >= 2:
            frage = ' '.join(args[1:])
            mess = await message.channel.send('Ich versuche deine Frage `{0}` zu beantworten.'.format(frage))
            await asyncio.sleep(2)
            await mess.edit(content='Ich kontaktiere das Orakel...')
            await asyncio.sleep(2)
            await mess.edit(content='Deine Antwort zur Frage `{0}` lautet: `{1}`'
                            .format(frage, random.choice(antworten)))
async def on_message_delete(self, message):
    channel = client.get_channel(640665358264565771)
    await channel.send("Gelöschte Nachricht " + message.content)
async def on_message_edit (self, before, after):
    channel = client.get_channel(640665358264565771)
    await channel.send("Geänderte Nachricht " + before.content + " zu " + after.content)

#später für heroku client.run(viel azhelen) rausnehmen komplett und den Token in secrets bei heroku eingeben. Davor noch das # vor client.run(os.getenv('Token')) wegmachen
client.run(os.getenv('Token'))

