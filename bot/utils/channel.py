import logging
from typing import Any

import discord


async def connect_to_channel(channel: discord.VoiceChannel, voice: discord.VoiceProtocol | Any):
    if voice is None:
        logging.info(f"Joining voice channel: {channel}")
        return await channel.connect()
    elif voice.channel != channel:
        await voice.move_to(channel)
    else:
        logging.info(f"Voice channel: {channel} already connected")

    return voice
