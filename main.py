import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import os
import json

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="^", intents=intents)

# ==================== LOAD CONFIG ====================
# Memuat konfigurasi dari file JSON untuk menyimpan data persist
def load_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as file:
            return json.load(file)
    return {}

config = load_config()

# ==================== ID KONFIGURASI AWAL ====================
WELCOME_CHANNEL_ID = config.get("welcome_channel")
GOODBYE_CHANNEL_ID = config.get("goodbye_channel")
BAN_CHANNEL_ID = config.get("ban_channel")
ANNOUNCE_CHANNEL_ID = config.get("announce_channel")
CONTROL_CHANNEL_ID = config.get("control_channel")

# Role ID
admin_role_id = 123456789012345678  # Ganti dengan ID role Admin
staff_role_id = 987654321098765432  # Ganti dengan ID role Staff

# ==================== CEK IZIN ====================

# Cek apakah user adalah admin
def is_admin(ctx):
    return ctx.author.guild_permissions.manage_guild

# Cek apakah user adalah staff
def is_staff(ctx):
    admin_role = discord.utils.get(ctx.guild.roles, id=admin_role_id)
    staff_role = discord.utils.get(ctx.guild.roles, id=staff_role_id)
    return admin_role in ctx.author.roles or staff_role in ctx.author.roles

# Cek apakah command dikirim di channel staff
def is_control_channel(ctx):
    return ctx.channel.id == CONTROL_CHANNEL_ID

# ==================== EVENTS ====================

@bot.event
async def on_ready():
    print(f'✅ Bot aktif sebagai {bot.user}')

@bot.event
async def on_member_join(member):
    # Welcome Message
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"Selamat datang {member.mention} di server {member.guild.name}!")

@bot.event
async def on_member_remove(member):
    # Goodbye Message
    channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if channel:
        await channel.send(f"{member.name} telah meninggalkan server. Selamat tinggal!")

@bot.event
async def on_member_ban(guild, user):
    # Ban Message
    channel = bot.get_channel(BAN_CHANNEL_ID)
    if channel:
        await channel.send(f"🔨 {user.name} telah dibanned dari server.")

# ==================== TEST MESSAGE COMMANDS ====================

@bot.command()
async def test_welcome(ctx):
    """Mengirim pesan welcome sebagai tes"""
    if not is_admin(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    member = ctx.author  # Gunakan user yang memanggil command
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        await ctx.send("❌ Channel welcome belum disetting.")
        return

    message = config.get("welcome_message", "Selamat datang {member}!").replace("{member}", member.mention)
    image_url = config.get("welcome_image")

    embed = discord.Embed(description=message, color=discord.Color.green())
    if image_url:
        embed.set_image(url=image_url)

    await channel.send(embed=embed)
    await ctx.send("✅ Pesan welcome berhasil diuji.")

@bot.command()
async def test_goodbye(ctx):
    """Mengirim pesan goodbye sebagai tes"""
    if not is_admin(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    member = ctx.author
    channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if not channel:
        await ctx.send("❌ Channel goodbye belum disetting.")
        return

    message = config.get("goodbye_message", "{member} telah keluar.").replace("{member}", member.name)
    image_url = config.get("goodbye_image")

    embed = discord.Embed(description=message, color=discord.Color.red())
    if image_url:
        embed.set_image(url=image_url)

    await channel.send(embed=embed)
    await ctx.send("✅ Pesan goodbye berhasil diuji.")

@bot.command()
async def test_ban(ctx):
    """Mengirim pesan ban sebagai tes"""
    if not is_admin(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    member = ctx.author
    channel = bot.get_channel(BAN_CHANNEL_ID)
    if not channel:
        await ctx.send("❌ Channel ban belum disetting.")
        return

    message = config.get("ban_message", "{member} telah dibanned.").replace("{member}", member.name)
    image_url = config.get("ban_image")

    embed = discord.Embed(description=message, color=discord.Color.dark_red())
    if image_url:
        embed.set_image(url=image_url)

    await channel.send(embed=embed)
    await ctx.send("✅ Pesan ban berhasil diuji.")

# ==================== ANNOUNCE COMMANDS ====================

@bot.command()
async def announce(ctx, *, arg):
    """Mengirim pengumuman di channel pengumuman"""
    if not is_admin(ctx) or not is_control_channel(ctx):
        return
    if "|" not in arg:
        await ctx.send("Format salah. Gunakan: `!announce Judul | Pesan`")
        return

    title, message = map(str.strip, arg.split("|", 1))
    channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(title=title, description=message, color=discord.Color.blue())
        await channel.send(embed=embed)
        await ctx.send("✅ Pengumuman dikirim.")

# ==================== SET CHANNEL COMMANDS ====================

@bot.command()
async def set_welcome(ctx, channel: discord.TextChannel):
    """Mengatur channel untuk pesan welcome saat user join"""
    if not is_admin(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    config["welcome_channel"] = channel.id
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
    await ctx.send(f"✅ Channel welcome berhasil diatur ke {channel.mention}.")

@bot.command()
async def set_goodbye(ctx, channel: discord.TextChannel):
    """Mengatur channel untuk pesan goodbye saat user keluar"""
    if not is_admin(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    config["goodbye_channel"] = channel.id
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
    await ctx.send(f"✅ Channel goodbye berhasil diatur ke {channel.mention}.")

@bot.command()
async def set_ban(ctx, channel: discord.TextChannel):
    """Mengatur channel untuk pesan ban saat user keluar"""
    if not is_admin(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return
            
    config["ban_channel"] = channel.id
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
    await ctx.send(f"✅ Channel ban berhasil diatur ke {channel.mention}.")

@bot.command()
async def set_announce(ctx, channel: discord.TextChannel):
    """Mengatur channel untuk pengumuman"""
    if not is_admin(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    config["announce_channel"] = channel.id
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
    await ctx.send(f"✅ Channel pengumuman berhasil diatur ke {channel.mention}.")

@bot.command()
async def set_control(ctx, channel: discord.TextChannel):
    """Mengatur channel khusus untuk command staff/admin"""
    if not is_admin(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    config["control_channel"] = channel.id
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
    await ctx.send(f"✅ Channel kontrol berhasil diatur ke {channel.mention}.")

@bot.command()
async def set_roles(ctx):
    """Mengirim pesan tombol role"""
    if not is_staff(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    button = Button(label="Member", style=discord.ButtonStyle.primary, custom_id="role_member")
    view = View(timeout=None)
    view.add_item(button)

    # Kirim pesan dengan tombol
    await ctx.send("Pilih role yang kamu inginkan:", view=view)

    # Fungsi untuk memberikan role saat tombol diklik
    async def button_callback(interaction):
        if interaction.custom_id == "role_member":
            role = discord.utils.get(ctx.guild.roles, name="Member")  # Ganti dengan role yang diinginkan
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ Kamu mendapatkan role {role.name}!", ephemeral=True)

    button.callback = button_callback

# ==================== JALANKAN BOT ====================

bot.run(os.getenv("DISCORD_TOKEN"))
