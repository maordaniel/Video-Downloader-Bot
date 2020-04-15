from pyrogram import Client, Filters, ReplyKeyboardMarkup, ReplyKeyboardRemove
import wget
import requests as r
import re
from emoji import emojize
from datetime import datetime
import os
from pytube import YouTube
from subprocess import run
import threading
import asyncio
from requests_html import HTMLSession


async def facebook_download(url, quality, user, client):
    try:
        page = r.get(url)
        try:
            video_url = re.search(f'{quality}:"(.+?)"', page.text).group(1)
        except AttributeError:
            session = HTMLSession()
            res = session.get(url)
            video_url = str(res.html.find('[property="og:video"]')[0])[45:-2]
        tm = datetime.now()
        today = tm.strftime("%d%m%Y")
        now = tm.strftime('%H%M%S%f')
        file_path = fr'C:\Users\Administrator\Desktop\videoBot\videos\{str(user) + today + now}.mp4'
        wget.download(video_url, file_path)
        msg = await client.send_message(chat_id=user, text="Please wait a while")
        await client.send_video(chat_id=user, video=file_path, supports_streaming=True)
        await client.delete_messages(
            chat_id=user,
            message_ids=msg.message_id
        )
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        await client.send_message(chat_id=user, text=f"Video May Private or Invalid URL.")


async def youtube_download(url, quality, user, client):
    global video_file
    try:
        video = YouTube(url)
        tm = datetime.now()
        today = tm.strftime("%d%m%Y")
        now = tm.strftime('%H%M%S%f')
        file_path = r'C:\Users\Administrator\Desktop\videoBot\videos'
        file_name = str(user) + today + now
        if quality == 'hd quality':
            video_file = video.streams.order_by('resolution').filter(file_extension='mp4')[-1]
            audio_file = video.streams.filter(only_audio=True).filter(file_extension='mp4')[-1]
            video_file.download(file_path, file_name)
            audio_file.download(file_path, file_name + '1')
            run(["ffmpeg", "-i", f"{file_path}\{file_name}.mp4", "-i", f"{file_path}\{file_name}1.mp4",
                 "-c", "copy", f"{file_path}\{file_name}2.mp4"])
            msg = await client.send_message(chat_id=user, text="Please wait a while")
            await client.send_video(chat_id=user, video=f'{file_path}\{file_name}2.mp4',
                                    supports_streaming=True)
            await client.delete_messages(
                chat_id=user,
                message_ids=msg.message_id
            )
            if os.path.exists(f'{file_path}\{file_name}.mp4'):
                os.remove(f'{file_path}\{file_name}.mp4')
                os.remove(f'{file_path}\{file_name}1.mp4')
                os.remove(f'{file_path}\{file_name}2.mp4')
        elif quality == "hq quality":
            video_file = video.streams.get_highest_resolution()
            video_file.download(file_path, file_name)
            msg = await client.send_message(chat_id=user, text="Please wait a while")
            await client.send_video(chat_id=user, video=f'{file_path}\{file_name}.mp4',
                                    supports_streaming=True)
            await client.delete_messages(
                chat_id=user,
                message_ids=msg.message_id
            )
            if os.path.exists(f'{file_path}\{file_name}.mp4'):
                os.remove(f'{file_path}\{file_name}.mp4')
        elif quality == 'mp3 version':
            audio_file = video.streams.filter(only_audio=True).filter(file_extension='mp4')[-1]
            audio_file.download(file_path, file_name)
            os.rename(f'{file_path}\{file_name}.mp4', f'{file_path}\{file_name}.mp3')
            msg = await client.send_message(chat_id=user, text="Please wait a while")
            await client.send_audio(chat_id=user, audio=f'{file_path}\{file_name}.mp3')
            await client.delete_messages(
                chat_id=user,
                message_ids=msg.message_id
            )
            if os.path.exists(f'{file_path}\{file_name}.mp3'):
                os.remove(f'{file_path}\{file_name}.mp3')
    except:
        await client.send_message(chat_id=user, text=f"Sorry something get wrong, Maybe Invalid URL.")
