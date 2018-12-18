# run with python3
import discord
import creds 
import pdb
from wand.image import Image
import tempfile
import math
import random
import logging
import os
import aiohttp
import glob
import shutil

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

def mkgif(filename, params):
    outfile = tempfile.mkstemp(prefix="deepfry", suffix=".gif")[1]
    logging.info("About to run mkgif(%s) -> %s", filename, outfile)
    outdir = outfile.split('.')[0]
    os.mkdir(outdir)
    with Image(filename=filename) as original:
        zeros = len(str(len(original.sequence)))
        framecount = 0
        for frame in original.sequence:
            with Image(frame) as mod_frame:
                mod_frame.modulate(params['brightness'], params['saturation'])
                mod_frame.evaluate(operator='gaussiannoise', value=0.05)
                if params['sine'] != None:
                    mod_frame.function('sinusoid', params['sine'])
                mod_frame.save(filename=(outdir + '/' + ('0' * (zeros - len(str(framecount)))) + str(framecount) + '.jpg'))
            framecount += 1
    frames = sorted(glob.glob(outdir + '/*.jpg'))
    with Image() as final:
        for frame in frames:
            with Image(filename=frame) as img:
                final.sequence.append(img)
        final.type='optimize'
        final.save(filename=outfile)
    response = format_params(params)
    return outfile, response

def deepfry(filename, params):
    outfile = tempfile.mkstemp(prefix="deepfry", suffix=".jpg")[1]
    logging.info("About to run deepfry(%s) -> %s", filename, outfile)
    with Image(filename=filename) as img:
        img.modulate(brightness=params['brightness'], saturation=params['saturation'])
        slope = math.tan((math.pi * (55/100.0+1.0)/4.0))
        if slope < 0.0:
          slope=0.0
        intercept = 15/100.0+((100-15)/200.0)*(1.0-slope)
        img.function("polynomial", [slope, intercept])
        img.evaluate(operator='gaussiannoise', value=0.05)
        if params['sine'] != None:
            img.function('sinusoid', params['sine'])
        img.save(filename=outfile)
    response = format_params(params)
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

def make_link(original_file):
    shutil.copy(original_file, creds.PATH)
    text = '\nThe image is located at '
    text += creds.URL + os.path.basename(original_file)
    return text

def format_params(params):
    response = ''
    if params['params'] and not params['chaos']:
        response += 'Parameters:\n'
        response += 'Brightness: ' + str(params['brightness']) + '\n'
        response += 'Saturation: ' + str(params['saturation']) + '\n'
        if params['sine'] != None:
            response += 'Frequency: {}\nPhase shift: {}\nAmplitude: {}\nBias: {}\n'.format(*params['sine'])
    return response

def get_colorschemes():
    random_bright = 0
    while random_bright < 100 and random_bright > -100:
        random_bright = random.randint(-1000, 800)
    # need to figure out how to best determine saturation relative to brightness for all ranges...
    random_sat = 0
    while random_sat < 100 and random_sat > -100:
        random_sat = random.randint(-1000, 1000)
    return {'flir': { 'brightness': 200, 'saturation': -800 }, 
            'dark': { 'brightness': -100, 'saturation': -200 },
            'classic': { 'brightness': 200, 'saturation': 300 },
            'galaxy': { 'brightness': -1000, 'saturation': -1000 },
            'random': { 'brightness': random_bright, 'saturation': random_sat },
            }

def parse_args(content):
    operations = {}
    # determine if link should be added to message body
    operations['link'] = True if 'link' in content else False
    operations['sine'] = create_params() if 'crispy' in content else None
    operations['params'] = True if 'params' in content else False
    operations['brightness'] = None
    operations['saturation'] = None
    bri_sat = get_colorschemes()
    for keyword in bri_sat.keys():
        if keyword in content:
            operations['brightness'] = bri_sat[keyword]['brightness']
            operations['saturation'] = bri_sat[keyword]['saturation']
    if not operations['brightness']:
        operations['brightness'] = bri_sat['random']['brightness']
        operations['saturation'] = bri_sat['random']['saturation']
        operations['sine'] = create_params()
    operations['chaos'] = True if 'chaos' in content else False
    return operations

@client.event
async def on_message(message):
    # bot do not reply to bot, ya dig?
    if message.author==client.user:
        return
    
    # help messages are good ^^,
    if message.content.startswith('deepfriedHELP'):
        msg = 'Welcome to THE DEEP FRYER.\nUse your powers wisely.\n\n'
        msg += 'Invoking the bot: begin your message with `FryThis` (no backticks)\n'
        msg += 'If you forget to add an attachment, the bot will publicly shame you. If you add an attachment that is not an image, the bot will publicly shame you.\n\n'
        msg += 'Optional arguments:\n'
        msg += 'Color defaults: `classic`, `dark`, `galaxy`, `flir`\n'
        msg += 'Jump the shark: `crispy`\n'
        msg += 'Generate a link: `link`\n'
        msg += 'See the parameters used to generate the image: `params`\n\n'
        msg += 'BETA FEATURES:\n'
        msg += 'The Phryer supports GIFs! (Mostly.) Add a GIF as an attachment and invoke with the same commands.'
        # msg += 'For an extra serving of weird, add \'chaos\' to your command.```'
        await client.send_message(message.channel, msg)
    
    # FRY THIS
    if message.content.startswith('FryThis'):
        # react to triggering message
        emojis = {'robot': '🤖', 'camera': '📸'}
        for item in emojis.values():
            await client.add_reaction(message, item)
        # the sender sent an attachment! whoop whoop
        if len(message.attachments) > 0:
            print('only frying first image for the time being')
            if not os.path.isdir('/tmp/phryer'):
                os.mkdir('/tmp/phryer')
            result_file = '/tmp/phryer/{}'.format(message.attachments[0]['filename'])
            # retrieve the attachment
            is_gif = False
            is_valid = True
            # useful properties: resp.status, resp.headers['Content-Type'], etc
            with aiohttp.ClientSession() as session:
                async with session.get(message.attachments[0]['url']) as resp:
                    # check response for content-type attribute
                    if resp.headers['Content-Type'] == 'image/gif':
                        is_gif = True
                    elif resp.headers['Content-Type'] != 'image/png' and resp.headers['Content-Type'] != 'image/jpeg':
                        is_valid = False
                    # read response into file
                    if is_valid:
                        with open(result_file, 'wb') as the_file:
                            async for line in resp.content:
                                the_file.write(line)
            # deep fry the resulting attachment
            send_attachment = True
            operations = parse_args(message.content)
            if is_valid:
                if is_gif:
                    result_file, text = mkgif(result_file, operations)
                else:
                    result_file, text = deepfry(result_file, operations)
                if os.path.getsize(result_file) > 7800000:
                    send_attachment = False
                    text = '\nThe file is too large to attach; RIP. '
                if operations['link'] or not send_attachment:
                    if not creds.SUPPORT_LINKS:
                        text += 'Harass your admin to get image links supported.'
                    else:
                        text += make_link(result_file)
                if send_attachment:
                    await client.send_file(message.channel, result_file, content=text, filename='test' + os.path.splitext(result_file)[1])
                else:
                    await client.send_message(message.channel, text)
            else:
                # tell the user they're a dumbass for trying to fry a non-img file type
                result_file = None
                text = 'Send an image file, dumbass.'
                await client.send_message(message.channel, text)
        # the sender did not send an attachment; oops
        else:
            phrase = ['You forgot to take out the garbage, you ', 'You must construct additional memes, you ', 'Get your own dang meme, ', '?????, you ', 'I\'d give you a nasty look but you\'ve already got one, ', 'You are living proof that morons are a subatomic particle, ', 'You must be a cactus because you\'re a prick, you ', 'I was hoping for a battle of memes but you appear to be unarmed, you ', 'Cool story, ']
            insult = ['dongleberry.', 'dingbat.', 'troglodyte.', 'deadhead.', 'cockalorum.', 'ninnyhammer.', 'plebian.']
            print('no image attached; sending a stock image instead')
            msg = phrase[random.randint(0, len(phrase) - 1)] + insult[random.randint(0, len(insult) - 1)]
            # get a random picture
            operations = parse_args(message.content)
            if os.path.isdir('extra/stock_images'):
                files = glob.glob('extra/stock_images/*.*')
                filename = files[random.randint(0, len(files) - 1)]
                result_file, text = deepfry(filename, operations)
                big_result = tile(filename, result_file)
                msg += '\n' + text
                await client.send_file(message.channel, big_result, content=msg, filename='derp.jpg')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')

client.run(creds.TOKEN)
