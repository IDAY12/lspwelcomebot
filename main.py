import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from PIL import Image, ImageDraw, ImageSequence
import requests
from io import BytesIO
import tempfile
import sys
import traceback

# Bot setup with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def create_welcome_gif(member, input_gif_path):
    try:
        # Download avatar
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        avatar_response = requests.get(avatar_url)
        avatar_img = Image.open(BytesIO(avatar_response.content))
        
        # Resize avatar to circle
        size = (128, 128)  # Size of the avatar circle
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        avatar_img = avatar_img.resize(size)
        output = Image.new('RGBA', size, (0, 0, 0, 0))
        output.paste(avatar_img, (0, 0))
        output.putalpha(mask)
        
        # Create temporary file for the new GIF
        temp_gif = tempfile.NamedTemporaryFile(suffix='.gif', delete=False)
        
        # Open original GIF
        with Image.open(input_gif_path) as gif:
            # Get GIF frames
            frames = []
            for frame in ImageSequence.Iterator(gif):
                # Convert frame to RGBA
                frame = frame.convert('RGBA')
                
                # Calculate position to center the avatar
                pos = ((frame.width - size[0]) // 2, (frame.height - size[1]) // 2)
                
                # Create a new frame with the avatar
                new_frame = frame.copy()
                new_frame.paste(output, pos, output)
                
                frames.append(new_frame)
            
            # Save the new GIF
            frames[0].save(
                temp_gif.name,
                save_all=True,
                append_images=frames[1:],
                duration=gif.info.get('duration', 100),
                loop=0
            )
        
        return temp_gif.name
    except Exception as e:
        print(f"Error in create_welcome_gif: {str(e)}")
        traceback.print_exc()
        return None

# Event when bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} telah siap!')
    print(f'Bot berada di {len(bot.guilds)} server')
    print('Intents yang aktif:')
    print(f'- Members: {intents.members}')
    print(f'- Message Content: {intents.message_content}')
    print(f'- Presences: {intents.presences}')
    
    # Verify GIF file exists
    if not os.path.exists('lsp welcome.gif'):
        print("ERROR: File 'lsp welcome.gif' tidak ditemukan!")
        sys.exit(1)

# Event when new member joins
@bot.event
async def on_member_join(member):
    try:
        print(f'Member baru bergabung: {member.name}#{member.discriminator}')
        channel = member.guild.system_channel
        
        # Jika system channel tidak ada, coba cari channel welcome atau general
        if channel is None:
            for ch in member.guild.text_channels:
                if ch.name.lower() in ['welcome', 'general']:
                    channel = ch
                    break
        
        if channel is not None:
            try:
                # Create embed message
                embed = discord.Embed(
                    title=f"Selamat Datang di Server! 👋",
                    description=f"Hai {member.mention}, selamat bergabung di {member.guild.name}!\nSemoga betah ya! 🎉",
                    color=discord.Color.green()
                )
                
                # Tambahkan avatar member
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                
                # Create welcome GIF with avatar
                custom_gif_path = await create_welcome_gif(member, 'lsp welcome.gif')
                
                if custom_gif_path:
                    # Send GIF with embed
                    welcome_file = discord.File(custom_gif_path, filename='welcome.gif')
                    embed.set_image(url='attachment://welcome.gif')
                    await channel.send(file=welcome_file, embed=embed)
                    
                    # Delete temporary file
                    os.unlink(custom_gif_path)
                else:
                    # If GIF creation failed, send embed without GIF
                    await channel.send(embed=embed)
                
                print(f'Pesan welcome berhasil dikirim ke channel: {channel.name}')
                    
            except Exception as e:
                print(f'Error saat mengirim pesan welcome: {str(e)}')
                traceback.print_exc()
        else:
            print('Tidak dapat menemukan channel yang sesuai untuk mengirim pesan welcome')
    except Exception as e:
        print(f'Error in on_member_join: {str(e)}')
        traceback.print_exc()

# Test command
@bot.command()
async def testwelcome(ctx):
    print(f'Testing welcome message untuk {ctx.author}')
    await on_member_join(ctx.author)

# Error handler
@bot.event
async def on_error(event, *args, **kwargs):
    print(f'Error in {event}:')
    traceback.print_exc()

# Keep the bot running
keep_alive()

try:
    # Run the bot
    bot.run(os.environ['TOKEN'])
except Exception as e:
    print(f"Fatal error: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
