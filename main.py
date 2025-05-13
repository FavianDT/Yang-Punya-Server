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
    return ctx.channel.id == config.get("control_channel")

# ==================== EVENTS ====================

@bot.event
async def on_ready():
    print(f'✅ Bot aktif sebagai {bot.user}')

@bot.event
async def on_member_join(member):
    # Welcome Message
    channel = bot.get_channel(config.get("welcome_channel"))
    if channel:
        await channel.send(f"Selamat datang {member.mention} di server {member.guild.name}!")

@bot.event
async def on_member_remove(member):
    # Goodbye Message
    channel = bot.get_channel(config.get("goodbye_channel"))
    if channel:
        await channel.send(f"{member.name} telah meninggalkan server. Selamat tinggal!")

@bot.event
async def on_member_ban(guild, user):
    # Ban Message
    channel = bot.get_channel(config.get("ban_channel"))
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
    channel = bot.get_channel(config.get("welcome_channel"))
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
    channel = bot.get_channel(config.get("goodbye_channel"))
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
    channel = bot.get_channel(config.get("ban_channel"))
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

# ==================== RULES FEATURE ====================

# Command untuk mengatur isi rules
@bot.command()
async def set_rules(ctx, *, message):
    """Menyetel pesan aturan (rules) yang akan dikirim oleh bot"""
    if not is_staff(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    config["rules_message"] = message
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)
    await ctx.send("✅ Pesan rules berhasil disimpan!")

# Command untuk mengatur channel rules
@bot.command()
async def set_rules_channel(ctx, channel: discord.TextChannel):
    """Menyetel channel untuk mengirimkan rules"""
    if not is_staff(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    config["rules_channel"] = channel.id
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)
    await ctx.send(f"✅ Channel rules disetel ke {channel.mention}")

# Command untuk mengirimkan rules ke channel yang telah diset
@bot.command()
async def send_rules(ctx):
    """Mengirimkan pesan rules ke channel rules"""
    if not is_staff(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    rules_channel_id = config.get("rules_channel")
    rules_message = config.get("rules_message")

    if not rules_channel_id or not rules_message:
        await ctx.send("❌ Channel rules atau pesan rules belum disetting.")
        return

    channel = bot.get_channel(rules_channel_id)
    if not channel:
        await ctx.send("❌ Channel rules tidak ditemukan.")
        return

    await channel.send(rules_message)
    await ctx.send("✅ Rules berhasil dikirim.")

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
    channel = bot.get_channel(config.get("announce_channel"))
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
async def set_role(ctx, channel: discord.TextChannel):
    """Mengatur channel untuk pengumuman"""
    if not is_admin(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    config["role_channel"] = channel.id
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
    await ctx.send(f"✅ Channel role berhasil diatur ke {channel.mention}.")

@bot.command()
async def verif_role(ctx, channel: discord.TextChannel):
    """Mengatur channel untuk pengumuman"""
    if not is_admin(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    config["verif_channel"] = channel.id
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
    await ctx.send(f"✅ Channel role berhasil diatur ke {channel.mention}.")

from discord.ui import Button, View


# ==================== BUTTON ROLE ====================

# Command untuk menambahkan tombol role
@bot.command()
async def add_button_role(ctx, label: str, color: str, role_name: str):
    """Menambahkan tombol untuk memberikan role tertentu"""
    if not is_staff(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    # Menentukan warna tombol
    button_color = discord.ButtonStyle.primary if color.lower() == "primary" else discord.ButtonStyle.secondary

    # Mencari role berdasarkan nama
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"❌ Role '{role_name}' tidak ditemukan.")
        return

    # Membuat tombol baru
    button = Button(label=label, style=button_color, custom_id=f"role_{role.id}")
    view = View(timeout=None)
    view.add_item(button)

    # Mendapatkan verif_channel_id dari file konfigurasi
    verif_channel_id = config.get("verif_channel")
    if not verif_channel_id:
        await ctx.send("❌ Channel verifikasi belum disetting.")
        return

    # Mendapatkan objek channel berdasarkan ID
    verif_channel = bot.get_channel(verif_channel_id)
    if not verif_channel:
        await ctx.send("❌ Channel verifikasi tidak ditemukan.")
        return

    # Mengirim pesan dengan tombol ke channel
    await verif_channel.send(f"Tombol role '{label}' telah ditambahkan!", view=view)

    # Fungsi untuk memberikan role saat tombol diklik
    async def button_callback(interaction):
        if interaction.custom_id == f"role_{role.id}":
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ Kamu mendapatkan role {role.name}!", ephemeral=True)

    # Menetapkan callback ke tombol
    button.callback = button_callback


# ==================== REACTION ROLE ====================
@bot.command()
async def add_reaction_roles(ctx, *, emoji_role_input: str):
    """
    Menambahkan beberapa reaction role sekaligus dalam satu pesan.
    Format input: emoji1, Role Name 1 | emoji2, Role Name 2 | ...
    """
    if not is_staff(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    role_channel_id = config.get("role_channel")
    if not role_channel_id:
        await ctx.send("❌ Channel role belum disetting.")
        return

    role_channel = bot.get_channel(role_channel_id)
    if not role_channel:
        await ctx.send("❌ Channel untuk role tidak ditemukan.")
        return

    emoji_role_pairs = emoji_role_input.split("|")
    pairs = []

    # Proses masing-masing pasangan
    for pair in emoji_role_pairs:
        try:
            emoji, role_name = pair.strip().split(",", 1)
            emoji = emoji.strip()
            role_name = role_name.strip()
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"❌ Role '{role_name}' tidak ditemukan.")
                return
            pairs.append((emoji, role))
        except ValueError:
            await ctx.send("❌ Format salah. Gunakan format: emoji, Role Name | emoji2, Role Name2 ...")
            return

    # Buat satu pesan untuk semua emoji-role
    description = "\n".join([f"{emoji} - {role.name}" for emoji, role in pairs])
    message = await role_channel.send(f"Reaksi dengan emoji berikut untuk mendapatkan role:\n{description}")

    for emoji, _ in pairs:
        await message.add_reaction(emoji)

    # Simpan ke config.json
    if "reaction_roles" not in config:
        config["reaction_roles"] = {}

    config["reaction_roles"][str(message.id)] = [
        {"emoji": emoji, "role_id": role.id} for emoji, role in pairs
    ]

    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

    await ctx.send("✅ Beberapa reaction role berhasil ditambahkan!")

# ==================== DROPDOWN ROLE ====================
@bot.command()
async def add_dropdown_role(ctx, *, roles_csv: str):
    """Menambahkan dropdown role. Format: role1, role2, role3"""
    if not is_staff(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    # Ambil channel dari config
    role_channel_id = config.get("role_channel")
    if not role_channel_id:
        await ctx.send("❌ Channel role belum disetting.")
        return

    role_channel = bot.get_channel(role_channel_id)
    if not role_channel:
        await ctx.send("❌ Channel tidak ditemukan.")
        return

    role_names = [r.strip() for r in roles_csv.split(",")]
    roles = [discord.utils.get(ctx.guild.roles, name=rn) for rn in role_names]
    roles = [r for r in roles if r]

    if not roles:
        await ctx.send("❌ Tidak ada role valid ditemukan.")
        return

    # Buat opsi dropdown
    options = [discord.SelectOption(label=r.name, value=str(r.id)) for r in roles]

    select = Select(
        placeholder="Pilih role kamu",
        min_values=1,
        max_values=1,
        options=options
    )

    async def callback(interaction: discord.Interaction):
        role_id = int(interaction.data['values'][0])
        role = discord.utils.get(interaction.guild.roles, id=role_id)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ Role {role.name} diberikan.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Role tidak ditemukan.", ephemeral=True)

    select.callback = callback

    view = View(timeout=None)
    view.add_item(select)

    # Kirim dropdown
    msg = await role_channel.send("Pilih role dari dropdown berikut:", view=view)

    # Simpan ke config
    config["dropdown_roles"].append(msg.id)
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    await ctx.send("✅ Dropdown role berhasil ditambahkan.")

# ==================== REMOVE DROPDOWN ROLE ====================

@bot.command()
async def remove_dropdown_role(ctx, message_id: int):
    """Menghapus dropdown role berdasarkan ID pesan"""
    if not is_staff(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    role_channel_id = config.get("role_channel")
    if not role_channel_id:
        await ctx.send("❌ Channel role belum disetting.")
        return

    role_channel = bot.get_channel(role_channel_id)
    if not role_channel:
        await ctx.send("❌ Channel tidak ditemukan.")
        return

    try:
        msg = await role_channel.fetch_message(message_id)
        await msg.delete()
        config["dropdown_roles"] = [mid for mid in config["dropdown_roles"] if mid != message_id]
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
        await ctx.send("✅ Dropdown role berhasil dihapus.")
    except discord.NotFound:
        await ctx.send("❌ Pesan tidak ditemukan.")
    except Exception as e:
        await ctx.send(f"❌ Terjadi kesalahan: {e}")


# ==================== LOG ====================
# Fungsi untuk mengirim log ke channel log
async def send_log(guild: discord.Guild, message: str):
    log_channel_id = config.get("log_channel")
    if log_channel_id:
        # Cari channel berdasarkan ID di dalam guild
        log_channel = guild.get_channel(log_channel_id) or bot.get_channel(log_channel_id)
        if log_channel:
            await log_channel.send(f"📝 {message}")

# Command untuk mengatur channel log
@bot.command()
async def set_log_channel(ctx, channel: discord.TextChannel):
    """Mengatur channel khusus untuk log"""
    if not is_staff(ctx):
        await ctx.send("❌ Kamu tidak memiliki izin.")
        return

    config["log_channel"] = channel.id
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    await ctx.send(f"✅ Channel log diset ke {channel.mention}")
    await send_log(ctx.guild, f"Channel log berhasil diatur oleh {ctx.author.mention} ke {channel.mention}.")

# Log saat memilih role (contoh: reaction role atau dropdown role)
async def log_role_selection(ctx, selected_role):
    await send_log(ctx.guild, f"{ctx.author.mention} memilih role {selected_role.name}.")

# Log saat rules diperbarui
async def log_rules_updated(ctx):
    await send_log(ctx.guild, f"📃 Rules diperbarui oleh {ctx.author.mention}.")

# Event ketika member baru bergabung
@bot.event
async def on_member_join(member):
    await send_log(member.guild, f"📥 {member.mention} bergabung ke server.")

# Event ketika member dikeluarkan
@bot.event
async def on_member_remove(member):
    await send_log(member.guild, f"📤 {member.mention} meninggalkan server.")

# ==================== JALANKAN BOT ====================

bot.run(os.getenv("DISCORD_TOKEN"))
