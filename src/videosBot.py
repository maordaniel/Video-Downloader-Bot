from src.download_func import *

# put your api id+ api hash
api_id = "api_id"
api_hash = 'api_hash'

app = Client('Bot_token', api_id=api_id, api_hash=api_hash)

actions_user = {}


@app.on_message(Filters.command("start"))
async def start_command(client, message):
    wave = emojize(":wave:", use_aliases=True)
    smiley = emojize(":smiley:", use_aliases=True)
    first_name = message.from_user.last_name if message.from_user.last_name is not None else "User"
    last_name = message.from_user.last_name if message.from_user.last_name is not None else ""
    await client.send_message(chat_id=message.chat.id,
                              text=f"""Hello {first_name} {last_name}{wave}
I'm Videos Downloader Bot.
I can download videos from FaceBook and YouTube by links.
Enjoy! {smiley}""")


async def menu(client, chat_id, social):
    global custom_keyboard
    if 'facebook' in social:
        custom_keyboard = [['HD Quality'],
                           ['HQ Quality'],
                           ['Cancel']]
    elif 'youtube' in social:
        custom_keyboard = [['HD Quality'],
                           ['HQ Quality'],
                           ['Mp3 Version'],
                           ['Cancel']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
    await client.send_message(chat_id=chat_id,
                              text="Select Quality", reply_markup=reply_markup)




@app.on_message(Filters.text)
async def echo(client, message):
    like = emojize(":thumbsup:", use_aliases=True)
    sad = emojize(":confused:", use_aliases=True)
    text_message = message.text.lower()
    quality_list = ['hq quality', 'hd quality', 'mp3 version']
    social_links = ['https://www.facebook', "https://m.facebook", 'https://www.youtu',
                    "https://m.youtube", 'https://youtu.be']
    try:
        if any(text_message.startswith(i) for i in social_links):
            for i in social_links:
                if text_message.startswith(i):
                    if message.chat.id not in actions_user:
                        actions_user[message.chat.id] = {"action": False}
                    if not actions_user[message.chat.id]["action"]:
                        actions_user[message.chat.id] = {"action": True, "url": message.text}
                        await menu(client, message.chat.id, text_message)
                        break

        elif text_message in quality_list and actions_user[message.chat.id]["action"]:
            if "facebook" in actions_user[message.chat.id]["url"].lower():
                quality = "hd_src" if text_message == 'hd quality' else "sd_src"
                await client.send_message(chat_id=message.chat.id, text=f"{like}",
                                          reply_markup=ReplyKeyboardRemove())
                threading.Thread(target=asyncio.run, args=(
                    facebook_download(actions_user[message.chat.id]['url'], quality, message.chat.id, client),)).start()
                actions_user[message.chat.id] = {"action": False}
            elif "youtube" in actions_user[message.chat.id]["url"].lower():
                await client.send_message(chat_id=message.chat.id, text=f"{like}",
                                          reply_markup=ReplyKeyboardRemove())
                threading.Thread(target=asyncio.run, args=(youtube_download(actions_user[message.chat.id]['url'],
                                                                            text_message, message.chat.id,
                                                                            client),)).start()
                actions_user[message.chat.id] = {"action": False}
        elif text_message == "cancel" and actions_user[message.chat.id]["action"]:
            actions_user[message.chat.id] = {"action": False}
            await client.send_message(chat_id=message.chat.id, text="Action Canceled.",
                                      reply_markup=ReplyKeyboardRemove())
        else:
            await client.send_message(chat_id=message.chat.id,
                                      text=f"supports Only Facebook and Youtube links{sad}.")
    except:
        pass


app.run()
