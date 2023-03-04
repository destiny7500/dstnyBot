import nextcord
import os
from nextcord.ext import commands
import wavelink

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = 'dt.', intents=intents)

@bot.event
async def on_ready():
  print("Ready")
  bot.loop.create_task(node_connect())

@bot.event
async def wavelink_node_ready(node: wavelink.Node):
  print(f"Node {node.identifier} is ready")
  
async def node_connect():
  await bot.wait_until_ready()
  await wavelink.NodePool.create_node(bot=bot, host='lavalink.mariliun.ml', port=443, password='lavaliun', https=True)  

@bot.event
async def on_track_end(player: wavelink.Player, track: wavelink.Track, reason):
  ctx = player.ctx
  vc: player = ctx.client
  if vc.loop:
    return await vc.play(track)
  
  next_song = vc.queue.get()
  await vc.play(next_song)
  await ctx.send(f"Now Playing - {next_song.title}")

@bot.command(name = "play")
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
  if not ctx.voice_client:
    vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.send("You haven't joined any voice channel") 
  else:
    vc: wavelink.Player = ctx.voice_client

  if vc.queue.is_empty and not vc.is_playing():
    await vc.play(search)
    await ctx.send(f"Now Playing - {search.title}")
  else:
    await vc.queue.put_wait(search)
    await ctx.send(f"Added {search.title} to queue")
  vc.ctx = ctx
  setattr(vc, "loop", False)

@bot.command(name = "pause")
async def pause(ctx: commands.Context):
  if not ctx.voice_client:
    return await ctx.send("No music played right now.")
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.send("You haven't joined any voice channel") 
  else:
    vc: wavelink.Player = ctx.voice_client
  
  await vc.pause()
  await ctx.send("Music paused.")

@bot.command(name = "resume")
async def resume(ctx: commands.Context):
  if not ctx.voice_client:
    return await ctx.send("No music played right now.")
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.send("You haven't joined any voice channel") 
  else:
    vc: wavelink.Player = ctx.voice_client
  
  await vc.resume()
  await ctx.send("Music resumed.")

@bot.command(name = "stop")
async def stop_music(ctx: commands.Context):
  if not ctx.voice_client:
    return await ctx.send("No music played right now.")
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.send("You haven't joined any voice channel") 
  else:
    vc: wavelink.Player = ctx.voice_client
  
  await vc.stop()
  await ctx.send("Music stopped.")

@bot.command(name = "dsc")
async def disconnect(ctx: commands.Context):
  if not ctx.voice_client:
    return await ctx.send("No music played right now.")
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.send("You haven't joined any voice channel") 
  else:
    vc: wavelink.Player = ctx.voice_client
  
  await vc.disconnect()
  await ctx.send("Disconnected.")

@bot.command(name = "loop")
async def loop_song(ctx: commands.Context):
  if not ctx.voice_client:
    return await ctx.send("No music played right now.")
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.send("You haven't joined any voice channel") 
  else:
    vc: wavelink.Player = ctx.voice_client
  
  try:
    vc.loop ^= True
  except Exception:
    setattr(vc, "loop", False)
  if vc.loop:
    return await ctx.send("Music is being looped")
  else:
    return await ctx.send("Music loop stopped")

@bot.command(name = "queue")
async def queue(ctx: commands.Context):
  if not ctx.voice_client:
    return await ctx.send("No music played right now.")
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.send("You haven't joined any voice channel") 
  else:
    vc: wavelink.Player = ctx.voice_client
  if vc.queue.is_empty:
    return await ctx.send("Queue is empty")
  
  em = nextcord.Embed(title="Queue")
  queue = vc.queue.copy()
  song_count = 0
  for song in queue:
    song_count += 1
    em.add_field(name = f"Song Num {song_count}", value= f"{song.title}")
   
  await ctx.send(embed=em)















bot.run("MTA3NTEyNDY4NjY3NTAwNTU3MQ.GqQh2E.3bcGlitPw89fxx5b-jXhFMX2du8Hp-T2Jf27pE")