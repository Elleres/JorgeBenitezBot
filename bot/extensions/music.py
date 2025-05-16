import logging

import discord
from discord.ext import commands

from bot.utils.channel import connect_to_channel
from bot.utils.yt import extract_playlist_audio_urls
from bot.config import FFMPEG_OPTIONS


class Music(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
            self.status = None
            self.current_song = None
            self.queue = []
            self.current_index = 0
            self.voice = None
            self.manually_skipping = False

    @commands.command()
    async def play(self, ctx, *, query: str):
        if self.status != "Playing":
            await self.play_audio(ctx, query)
        else:
            await ctx.send(f"{ctx.author.mention} Already playing: **{self.current_song}**")

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.send(f"{ctx.author.mention} Stopped")

    @commands.command()
    async def skip(self, ctx):
        if self.current_index + 1 < len(self.queue):
            await self.play_index(ctx, self.current_index + 1)
            await ctx.send(f"{ctx.author.mention} Pulando para a próxima música.")
        else:
            await ctx.send("Não há mais músicas na playlist.")

    @commands.command()
    async def previous(self, ctx):
        if self.current_index > 0:
            await self.play_index(ctx, self.current_index - 1)
            await ctx.send(f"{ctx.author.mention} Voltando para a música anterior.")
        else:
            await ctx.send("Essa já é a primeira música da playlist.")

    @commands.command()
    async def current_song(self, ctx):
        await ctx.send(self.current_song)

    async def play_audio(self, ctx: commands.Context, query: str):
        voice_state = ctx.message.author.voice
        self.voice = ctx.voice_client

        if voice_state is None:
            await ctx.send(f"{ctx.author.mention} Você precisa estar em um canal de voz.")
            return

        channel = voice_state.channel
        self.voice = await connect_to_channel(channel, self.voice)

        self.queue = extract_playlist_audio_urls(query)
        self.current_index = 0

        await self.play_next(ctx)

    async def play_next(self, ctx):
        await self.play_index(ctx, self.current_index)

    async def play_index(self, ctx, index: int):
        if not (0 <= index < len(self.queue)):
            await ctx.send("Índice inválido na playlist.")
            return

        self.manually_skipping = True

        self.current_index = index
        url, title = self.queue[index]
        self.current_song = title
        self.status = "Playing"

        if self.voice.is_playing():
            self.voice.stop()

        while self.voice.is_playing():
            await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.timedelta(milliseconds=100))

        def after_playing(err):
            if err:
                logging.error(err)
            if not self.manually_skipping:
                self.current_index += 1
                self.bot.loop.create_task(self.play_index(ctx, self.current_index))

        self.voice.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=after_playing)
        self.manually_skipping = False
        await ctx.send(f"🎶 Tocando: **{title}**")

async def setup(bot):
    await bot.add_cog(Music(bot))