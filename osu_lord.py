#!./.venv/bin/python

import discord      # base discord module
import code         # code.interact
import os           # environment variables
import inspect      # call stack inspection
import random       # dumb random number generator

from discord import FFmpegPCMAudio
from discord.ext import commands    # Bot class and utils
from discord.channel import VoiceChannel

################################################################################
############################### HELPER FUNCTIONS ###############################
################################################################################

# log_msg - fancy print
#   @msg   : string to print
#   @level : log level from {'debug', 'info', 'warning', 'error'}
def log_msg(msg: str, level: str):
    # user selectable display config (prompt symbol, color)
    dsp_sel = {
        'debug'   : ('\033[34m', '-'),
        'info'    : ('\033[32m', '*'),
        'warning' : ('\033[33m', '?'),
        'error'   : ('\033[31m', '!'),
    }

    # internal ansi codes
    _extra_ansi = {
        'critical' : '\033[35m',
        'bold'     : '\033[1m',
        'unbold'   : '\033[2m',
        'clear'    : '\033[0m',
    }

    # get information about call site
    caller = inspect.stack()[1]

    # input sanity check
    if level not in dsp_sel:
        print('%s%s[@] %s:%d %sBad log level: "%s"%s' % \
            (_extra_ansi['critical'], _extra_ansi['bold'],
             caller.function, caller.lineno,
             _extra_ansi['unbold'], level, _extra_ansi['clear']))
        return

    # print the damn message already
    print('%s%s[%s] %s:%d %s%s%s' % \
        (_extra_ansi['bold'], *dsp_sel[level],
         caller.function, caller.lineno,
         _extra_ansi['unbold'], msg, _extra_ansi['clear']))

################################################################################
############################## BOT IMPLEMENTATION ##############################
################################################################################

playlist = {
	'Galaxy_Collapse.mp3' : '1'
}

# bot instantiation
bot = commands.Bot(command_prefix='!')

# on_ready - called after connection to server is established
@bot.event
async def on_ready():
    log_msg('logged on as <%s>' % bot.user, 'info')

# on_message - called when a new message is posted to the server
#   @msg : discord.message.Message
@bot.event
async def on_message(msg):
    # filter out our own messages
    if msg.author == bot.user:
        return
    
    log_msg('message from <%s>: "%s"' % (msg.author, msg.content), 'debug')

    # overriding the default on_message handler blocks commands from executing
    # manually call the bot's command processor on given message
    await bot.process_commands(msg)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.guild.voice_client is None: return 
    if len(member.guild.voice_client.channel.members) == 1:
        await member.guild.voice_client.disconnect()

@bot.command()
async def list(ctx):
    await ctx.send("These are my most hated beats:")
    for index in playlist:
        await ctx.send (playlist[index] + '.' + index)

@bot.command()
async def come(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Osu Lord sees no nerd around.".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        if not ctx.message.guild.voice_client:
        	await ctx.send("I'm here. You should get a life.")
        	await channel.connect()
        else:
        	await ctx.send("Do you even have eyes? I'm right here!")

#extra comment im adding cuz yes
@bot.command()
async def play(ctx, song_name):
    if not ctx.message.author.voice:
        await ctx.send("Osu Lord sees no nerd around.".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        if not ctx.message.guild.voice_client:
        	await ctx.send("I'm here. You should get a life.")
        	await channel.connect()
        try :
            voice_channel = ctx.message.guild.voice_client
            if song_name in playlist:
                voice_channel.play(discord.FFmpegPCMAudio(song_name))
                await ctx.send("Presenting you: " + song_name)
            else :
                await ctx.send("Do you see me as a full-time nerd to have this song?")
        except :
            await ctx.send("*Try to play a song, I'll see what I can do about it.*")

@bot.command()
async def scram(ctx):
    if ctx.message.guild.voice_client:
        await ctx.send("Damn you and see you next time.");
        await ctx.message.guild.voice_client.disconnect();
    else:
        await ctx.send("No u. I'm not even there.");

# roll - rng chat command
#   @ctx     : command invocation context
#   @max_val : upper bound for number generation (must be at least 1)
@bot.command(brief='Generate random number between 1 and <arg>')
async def roll(ctx, max_val: int):
    # argument sanity check
    if max_val < 1:
        raise Exception('argument <max_val> must be at least 1')

    await ctx.send(random.randint(1, max_val))

# roll_error - error handler for the <roll> command
#   @ctx     : command that crashed invocation context
#   @error   : ...
@roll.error
async def roll_error(ctx, error):
    await ctx.send(str(error))

################################################################################
############################# PROGRAM ENTRY POINT ##############################
################################################################################

if __name__ == '__main__':
    # check that token exists in environment
    if 'BOT_TOKEN' not in os.environ:
        log_msg('save your token in the BOT_TOKEN env variable!', 'error')
        exit(-1)

    # launch bot (blocking operation)
    bot.run(os.environ['BOT_TOKEN'])
