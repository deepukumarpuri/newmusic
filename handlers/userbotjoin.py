import asyncio
from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS
from helpers.decorators import authorized_users_only, sudo_users_only, errors
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["join", f"join@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def join_group(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "โข **I Have Not Permission:**\n\nยป โ __Add Users__",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"๐ Flood Wait Error ๐ \n\n**Userbot Couldn't Join Your Group Due To Heavy Join Requests For Userbot**"
            "\n\n**or Add Assistant Manually To Your Group And Try Again**\n Contact To For New Bot :- @DKBOTZHELP",
        )
        return
    await message.reply_text(
        f"โ **Userbot Succesfully Entered Chat**",
    )


@Client.on_message(
    command(["leave", f"leave@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def leave_group(client, message):
    try:
        await USER.send_message(message.chat.id, "โ Userbot Successfully Left Chat")
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "โ **Userbot Couldn't Leave Your Group, May Be Floodwaits.**\n\n**ยป Or Manually Kick Userbot From Your Group**"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("๐ **Userbot** Leaving All Chats !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"Userbot Leaving All Group...\n\nLeft: {left} chats.\nFailed: {failed} Chats."
            )
        except:
            failed += 1
            await lol.edit(
                f"Userbot leaving...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"โ Left from: {left} chats.\nโ Failed in: {failed} chats."
    )
