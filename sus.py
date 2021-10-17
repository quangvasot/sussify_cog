import discord
import aiohttp
from redbot.core import commands
from redbot.core import Config
from redbot.core import checks
from PIL import Image, ImageEnhance
from random import randint
from io import BytesIO
import functools
import asyncio
import urllib
from PIL import Image
import numpy as np
import subprocess
import os

class ImageFindError(Exception):
        """Error shows up whenever _get_image busts or fail or sth idk refer to _deepfry in main bot folder"""
        pass
        
class sussy(commands.Cog):
        """make sussy images"""
        def __init__(self, bot):
                self.config = Config.get_conf(self, identifier=18011999)
                self.bot = bot
                self.imagetypes = ['png, jpg']

#source/refer to img_sussifier in main folder
#https://github.com/LinesGuy/img_sussifier reclone here in case shit breaks
        @staticmethod
        def _sus(foodget):
                output_width = 32  # Width of output gif, measured in sussy crewmates
                nearest_neighbour = False  # Enable this for flags
                twerk_frame_count = 6  # 0.png to 5.png

                # Load twerk frames 🥵
                twerk_frames = []
                twerk_frames_data = []  # Image as numpy array, pre-calculated for performance
                for i in range(6):
                    try:
                        img = Image.open(f"twerk_imgs/{i}.png").convert("RGBA")
                    except Exception as e:
                        print(f"Error loading twerk frames! Filename = {i}.png")
                        print("Probably you renamed the twerk_imgs folder or forgot to set twerk_frame_count. baka")
                        print(e)
                        exit()
                    twerk_frames.append(img)
                    twerk_frames_data.append(np.array(img))
                # Get dimensions of first twerk frame. Assume all frames have same dimensions
                twerk_width, twerk_height = twerk_frames[0].size

                # Get image to sussify!
                input_image = foodget.convert("RGB")
                input_width, input_height = input_image.size

                # Height of output gif (in crewmates)
                output_height = int(output_width * (input_height / input_width) * (twerk_width / twerk_height))

                # Width, height of output in pixels
                output_px = (int(output_width * twerk_width), int(output_height * twerk_height))

                # Scale image to number of crewmates, so each crewmate gets one color
                if nearest_neighbour:
                    input_image_scaled = input_image.resize((output_width, output_height), Image.NEAREST)
                else:
                    input_image_scaled = input_image.resize((output_width, output_height))

                for frame_number in range(twerk_frame_count):
                    print("Sussying frame #", frame_number)

                    # Create blank canvas
                    background = Image.new(mode="RGBA", size=output_px)
                    for y in range(output_height):
                        for x in range(output_width):
                            r, g, b = input_image_scaled.getpixel((x, y))

                            # Grab that twerk data we calculated earlier
                            # (x - y + frame_number) is the animation frame index,
                            # we use the position and frame number as offsets to produce the wave-like effect
                            sussified_frame_data = np.copy(twerk_frames_data[(x - y + frame_number) % len(twerk_frames)])
                            red, green, blue, alpha = sussified_frame_data.T
                            # Replace all pixels with colour (214,224,240) with the input image colour at that location
                            color_1 = (red == 214) & (green == 224) & (blue == 240)
                            sussified_frame_data[..., :-1][color_1.T] = (r, g, b)  # thx stackoverflow
                            # Repeat with colour (131,148,191) but use two thirds of the input image colour to get a darker colour
                            color_2 = (red == 131) & (green == 148) & (blue == 191)
                            sussified_frame_data[..., :-1][color_2.T] = (int(r*2/3), int(g*2/3), int(b*2/3))

                            # Convert sussy frame data back to sussy frame
                            sussified_frame = Image.fromarray(sussified_frame_data)

                            # Slap said frame onto the background 
                            background.paste(sussified_frame, (x * twerk_width, y * twerk_height))
                    background.save(f"sussified_{frame_number}.png")

                print("Converting sussy frames to sussy gif")
                # Convert sussied frames to gif. PIL has a built-in method to save gifs but
                # it has dithering which looks sus, so we use ffmpeg with dither=none
                subprocess.call('ffmpeg -f image2 -i sussified_%d.png -filter_complex "[0:v] scale=sws_dither=none:,split [a][b];[a] palettegen=max_colors=255:stats_mode=single [p];[b][p] paletteuse=dither=none" -r 20 -y -hide_banner -loglevel error sussified.gif')

                # Remove temp files
                for frame_number in range(twerk_frame_count):
                    os.remove(f"sussified_{frame_number}.png")
                return
                    

        async def _get_image(self, ctx):
                """Helper function to find an image."""
                if ctx.guild:
                        allowAllTypes = await self.config.guild(ctx.message.guild).allowAllTypes()
                        filesize_limit = ctx.guild.filesize_limit
                else:
                        allowAllTypes = False
                        path = urllib.parse.urlparse(ctx.message.attachments[0].url).path
                        if any(path.lower().endswith(x) for x in self.imagetypes):
                                isgif = False
                        else:
                                raise ImageFindError(f'Filetype not supported')
                        food = BytesIO()
                        await ctx.message.attachments[0].save(food)
                        food.seek(0)
                        foodget = Image.open(food)
                        foodget = img.convert('RGB')
                return foodget

        @commands.command(aliases=['sus'])
        @commands.bot_has_permissions(attach_files=True)
        async def sussify(self, ctx, link: str=None):
                """
                Sussify images.
                
                """
                async with ctx.typing():
                        try:
                                food = await self._get_image(ctx)
                        except ImageFindError as e:     
                                return await ctx.send(e)
                        task = functools.partial(self._sus, foodget)
                        task = self.bot.loop.run_in_executor(None, task)
                        try:
                                image = await asyncio.wait_for(task, timeout=60)
                        except asyncio.TimeoutError:
                                return await ctx.send('The image took too long to process.')
                        try:
                                await ctx.send(file=discord.File(sussified.gif))
                        except discord.errors.HTTPException:
                                return await ctx.send('Image is too large')


# lamkas a cute
