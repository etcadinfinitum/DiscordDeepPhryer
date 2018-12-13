# run with python3
import discord
import creds 
import pdb
from wand.image import Image
import tempfile
import math
import random
import logging
from urllib.request import urlretrieve
import os
import aiohttp
import requests
import glob

client = discord.Client()

def create_params():
    frequency = random.randint(1, 10) # 3
    phase_shift = random.randint(-90, -25)  #-90
    amplitude = random.randint(1, 9) * 0.1 # 0.2
    bias = random.randint(1, 9) * 0.1 # 0.7
    params = [frequency, phase_shift, amplitude, bias]
    return params

def heckin_rainbows(img):
    params = create_params()
    img.function('sinusoid', params)
    return params

def mkgif(filename):
    outfile = tempfile.mkstemp(prefix="deepfry", suffix=".gif")[1]
    logging.info("About to run mkgif(%s) -> %s", filename, outfile)
    with Image() as final:
        with Image(filename=filename) as img:
            params = create_params()
            for frame in img.sequence:
                with Image(frame).convert('jpeg') as mod_frame:
                    mod_frame.modulate(brightness=150, saturation=200)
                    slope = math.tan((math.pi * (55/100.0+1.0)/4.0))
                    if slope < 0.0:
                        slope=0.0
                    intercept = 15/100.0+((100-15)/200.0)*(1.0-slope)
                    mod_frame.function("polynomial", [slope, intercept])
                    mod_frame.evaluate(operator='gaussiannoise', value=0.05)
                    mod_frame.function('sinusoid', params)
                    with mod_frame.convert('gif') as new_frame:
                        mod_frame.delay = 3
                        final.sequence.append(new_frame)
        final.type = 'optimize'
        final.save(filename=outfile)
    return outfile, None

def deepfry(filename):
    outfile = tempfile.mkstemp(prefix="deepfry", suffix=".jpg")[1]
    logging.info("About to run deepfry(%s) -> %s", filename, outfile)
    with Image(filename=filename) as img:
        img.modulate(brightness=150, saturation=200)
        slope = math.tan((math.pi * (55/100.0+1.0)/4.0))
        if slope < 0.0:
          slope=0.0
        intercept = 15/100.0+((100-15)/200.0)*(1.0-slope)
        img.function("polynomial", [slope, intercept])
        img.evaluate(operator='gaussiannoise', value=0.05)
        params = heckin_rainbows(img)
        img.save(filename=outfile)
    response = ""
    response += "Parameters:\nFrequency: {}\nPhase shift: {}\nAmplitude: {}\nBias: {}\n".format(*params)
    return outfile, response

def tile(lhs, rhs):
    outfile = tempfile.mkstemp(prefix='tiled', suffix='.jpg')[1]
    logging.info('Tiling %s and %s' % (lhs, rhs))
    with Image(filename=lhs) as lImg:
        with Image(filename=rhs) as rImg:
            with Image(width = lImg.width + rImg.width, height = lImg.height) as result:
                result.composite(image=lImg, left=0, top=0)
                result.composite(image=rImg, left=lImg.width, top=0)
                result.save(filename=outfile)
    return outfile

@client.event
async def on_message(message):
    # bot do not reply to bot, ya dig?
    if message.author==client.user:
        return
    
    # help messages are good ^^,
    if message.content.startswith('deepfriedHELP'):
        msg = 'Welcome to THE DEEP FRYER.\nUse your powers wisely.\n\n'
        msg += 'Commands:\tAttachment:\tResult:\nFryThis\t\t\tjpg, png\t\t\tHecking FRIED\n'
        msg += 'FryThis\t\t\tNone\t\t\t\tTry it!\n\n'
        msg += 'BETA FEATURES:\n'
        await client.send_message(message.channel, msg)
    
    # FRY THIS
    if message.content.startswith('FryThis'):
        # the sender sent an attachment! whoop whoop
        if len(message.attachments) > 0:
            print('only frying first image for the time being')
            if not os.path.isdir('/tmp/phryer'):
                os.mkdir('/tmp/phryer')
            filename = '/tmp/phryer/{}'.format(message.attachments[0]['filename'] + '.jpg')
            # retrieve the attachment
            img_data = requests.get(message.attachments[0]['url'], stream=True)
            with open(filename, 'wb') as f:
                for chunk in img_data.iter_content(chunk_size=128):
                    f.write(chunk)
            # block comment is for aiohttp which is the discord.py recommendation but I can't figure out how to get bytestreams of the content from the request response
            '''
            with aiohttp.ClientSession() as session:
                async with session.get(message.attachments[0]['url']) as resp:
                    pdb.set_trace()
                    # useful properties: resp.status, resp.headers['Content-Type'], etc
                    with open(filename, 'wb') as the_file:
                        the_file.write(resp.read())
            pdb.set_trace()
            '''
            # deep fry the resulting attachment
            result_file, text = deepfry(filename)
            
            await client.send_file(message.channel, result_file, content=text, filename="test.jpg")
        # the sender did not send an attachment; oops
        else:
            phrase = ['You forgot to take out the garbage, you ', 'You must construct additional memes, you ', 'Get your own dang meme, ', '?????, you ', 'I\'d give you a nasty look but you\'ve already got one, ', 'You are living proof that morons are a subatomic particle, ', 'You must be a cactus because you\'re a prick, you ', 'I was hoping for a battle of memes but you appear to be unarmed, you ', 'Cool story, ']
            insult = ['dongleberry.', 'dingbat.', 'troglodyte.', 'deadhead.', 'cockalorum.', 'ninnyhammer.', 'plebian.']
            print('no image attached; sending a stock image instead')
            msg = phrase[random.randint(0, len(phrase) - 1)] + insult[random.randint(0, len(insult) - 1)]
            # get a random picture
            if os.path.isdir('extra/stock_images'):
                files = glob.glob('extra/stock_images/*.*')
                filename = files[random.randint(0, len(files) - 1)]
                result_file, text = deepfry(filename)
                big_result = tile(filename, result_file)
                await client.send_file(message.channel, big_result, content=msg, filename='derp.jpg')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')

client.run(creds.TOKEN)
