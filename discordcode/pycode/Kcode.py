import discord as d
from discord import app_commands as ac
from discord.ext import commands as c
import json as j
import datetime as dt
import os as os
import random as r
import aiohttp as ah
import asyncio as ai

i = d.Intents.default()
b = c.Bot(command_prefix="!", intents=d.Intents.all())
G = 1238043843476062209
cmd_enabled = True
admin_id = 1002132268736856136

@b.event
async def on_ready():
    print('ログインしました')
    await b.change_presence(activity=d.Game(name=" "))
    await b.tree.sync()

@b.tree.command(name='i', description='BOTの情報を表示します')
async def i_cmd(inter: d.Interaction):
    global cmd_enabled
    if cmd_enabled:
        await inter.response.send_message('開発者<:DEV:1267440009452064829><@1002132268736856136> 開発協力者<:ACCDEV:1267440500625903618> <@1032649313165258772> バージョン<:BE:1267439343882993734><:TA:1267439331069657119>v1', ephemeral=True)
    else:
        await inter.response.send_message('このコマンドは現在無効化されています。', ephemeral=True)

@b.tree.command(name='t', description='コマンドの有効/無効を切り替えます')
async def t_cmd(inter: d.Interaction):
    global cmd_enabled
    if inter.user.id == admin_id:
        cmd_enabled = not cmd_enabled
        s = "有効" if cmd_enabled else "無効"
        await inter.response.send_message(f"infoコマンドは現在{s}です。", ephemeral=True)
    else:
        await inter.response.send_message("このコマンドを実行する権限がありません。", ephemeral=True)

@b.tree.command(name='e', description='BOTに搭載されている絵文字をすべて表示します')
async def e_cmd(inter: d.Interaction):
    await inter.response.send_message('搭載絵文字 <:partner:1267440895037542471> <:ACCDEV:1267440500625903618> <:DEV:1267440009452064829> <:BE:1267439343882993734> <:TA:1267439331069657119> <:B_:1267438603718627378> <:mukou:1267467191142322216>', ephemeral=True)

FILE_PATH = "user_data.txt"
PRESET_PASSWORD = "MySecurePassword"
REQUIRED_ROLE_NAME = "Patron supporter"

def load_user_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            lines = f.readlines()
            return {line.split(",")[0].split(": ")[1]: line.split(",")[1].split(": ")[1].strip() for line in lines}
    return {}

def append_user_to_file(steam_id: str):
    with open(FILE_PATH, "a") as f:
        f.write(f"SteamID: {steam_id}\n")

def has_role(member: d.Member):
    return any(role.name == REQUIRED_ROLE_NAME for role in member.roles)

@b.tree.command(name="v", description="ゲーム内のバッチを獲得します")
@ac.describe(steam_id="SteamID", password="認証キー")
async def add_user(interaction: d.Interaction, steam_id: str, password: str):
    if not has_role(interaction.user):
        await interaction.response.send_message(f"認証できません必要なロール: {REQUIRED_ROLE_NAME}", ephemeral=True)
        return

    if password != PRESET_PASSWORD:
        await interaction.response.send_message("認証キーが正しくありません。", ephemeral=True)
        return

    user_data = load_user_data()
    if steam_id in user_data:
        await interaction.response.send_message("このSteamIDは既に登録されています。", ephemeral=True)
        return

    append_user_to_file(steam_id)
    await interaction.response.send_message(f"SteamID: {steam_id} が登録されました1時間以内に更新されます。", ephemeral=True)

ticket_owners = {}

@b.event
async def on_interaction(inter: d.Interaction):
    try:
        c_id = inter.data.get("custom_id")
        if c_id == "create_ticket":
            server = inter.guild
            if inter.user.id in ticket_owners.values():
                await inter.response.send_message("既にチケットが存在します。", ephemeral=True)
                return

            overwrites = {
                server.default_role: d.PermissionOverwrite(read_messages=False),
                server.me: d.PermissionOverwrite(read_messages=True),
                inter.user: d.PermissionOverwrite(read_messages=True)
            }
            c_name = f"チケット-{inter.user.name}"
            channel = await server.create_text_channel(name=c_name, overwrites=overwrites)

            ticket_owners[channel.id] = inter.user.id
            await channel.send(f"{inter.user.mention} チケットが作成されました!")
            await inter.response.send_message(f"チケットが作成されました！\n{channel.mention}", ephemeral=True)

            view = d.ui.View()
            button = d.ui.Button(style=d.ButtonStyle.danger, label="チケットを削除", custom_id="delete_ticket")
            view.add_item(button)
            await channel.send("", view=view)

        elif c_id == "delete_ticket":
            channel = inter.channel
            await channel.delete()
            if channel.id in ticket_owners:
                del ticket_owners[channel.id]

    except Exception as e:
        print(f"An error occurred: {e}")

if os.path.exists("lastcall.json"):
    with open("lastcall.json", "r") as f:
        lcall = j.load(f)
else:
    lcall = {"lastcall": 0}

@b.tree.command(name="c", description="募集します")
@ac.describe(内容="募集に表示するメッセージ")
async def c_cmd(interaction: d.Interaction, 内容: str = None):
    if interaction.guild.id != G:
        await interaction.response.send_message("このコマンドはこのサーバーでは使用できません。", ephemeral=True)
        return

    await interaction.response.defer()
    current_time = dt.datetime.now().timestamp()

    if lcall["lastcall"] < current_time - 3600:
        embed = d.Embed(title="募集", description="", color=d.Color.green())
        if 内容 is not None:
            embed.description = 内容
        embed.set_author(name="募集者", icon_url=interaction.user.avatar.url)
        await interaction.followup.send(
            allowed_mentions=d.AllowedMentions(roles=True),
            content=f"<@&1238062718825791590>",
            embed=embed
        )
        lcall["lastcall"] = current_time
        with open("lastcall.json", "w") as f:
            j.dump(lcall, f)
    else:
        remaining_time = 3600 - (current_time - lcall["lastcall"])
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        await interaction.followup.send(
            f"1時間に1回しか募集できません。あと {minutes} 分 {seconds} 秒 待ってください。",
            ephemeral=True
        )

gacha_items = {
    "⭐ 1つ星アイテム": {"xp": 10},
    "⭐⭐ 2つ星アイテム": {"xp": 20},
    "⭐⭐⭐ 3つ星アイテム": {"xp": 30},
    "⭐⭐⭐⭐ 4つ星アイテム": {"xp": 40},
    "⭐⭐⭐⭐⭐ 5つ星アイテム": {"xp": 50},
    "💎 特別アイテム": {"xp": 100},
}

user_data = {}
XP_THRESHOLD = 450

@b.tree.command(name="g", description="ガチャを引きます(alpha版)")
async def g_cmd(interaction: d.Interaction):
    selected_item = r.choice(list(gacha_items.keys()))
    if interaction.user.id not in user_data:
        user_data[interaction.user.id] = {"xp": 0}

    user_data[interaction.user.id]["xp"] += gacha_items[selected_item]["xp"]
    await interaction.response.send_message(f"{selected_item} を引きました！ 現在のXP: {user_data[interaction.user.id]['xp']}")

    if user_data[interaction.user.id]["xp"] >= XP_THRESHOLD:
        await interaction.user.send("おめでとう！レベルアップしました！")

if __name__ == "__main__":
    b.run("YO_UR_BOT_TOK_EN")
