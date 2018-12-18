import os
from wand.image import Image
from shutil import copyfile
import glob
import pdb
import logging

modulate_presets_1 = { (-100, -200): 'dark'} 
modulate_presets_2 = { (200, 300): 'default', (-1000, -1000): 'galaxy', (200, -800): 'flir'} 
cwd = './defaults_test/'

def mkgif(filename):
    outfiles = ['testing_overlay/no_over.gif', 'testing_overlay/combine_prev_frame.gif']
    # outfile = tempfile.mkstemp(prefix="deepfry", suffix=".gif")[1]
    combine = False
    for outfile in outfiles:
        logging.info("About to run mkgif(%s) -> %s", filename, outfile)
        outdir = outfile.split('.')[0]
        tmpfile=outdir + '/tmp.jpg'
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        with Image(filename=filename) as original:
            zeros = len(str(len(original.sequence)))
            framecount = 0
            for frame in original.sequence:
                if not combine:
                    print('testing no composite call for result file %s' % outfile)
                    with Image(frame) as mod_frame:
                        mod_frame.modulate(200, -800)
                        mod_frame.evaluate(operator='gaussiannoise', value=0.05)
                        # mod_frame.function('sinusoid', params)
                        mod_frame.save(filename=(outdir + '/' + ('0' * (zeros - len(str(framecount)))) + str(framecount) + '.jpg'))
                    framecount += 1
                else:
                    print('TESTING COMPOSITE CALL for result file %s' % outfile)
                    do_prev = False
                    if framecount == 0:
                        print('frying first image')
                        with Image(frame) as mod_frame:
                            with Image(mod_frame) as img:
                                img.save(filename=tmpfile)
                            mod_frame.modulate(200, -800)
                            mod_frame.evaluate(operator='gaussiannoise', value=0.05)
                            # mod_frame.function('sinusoid', params)
                            mod_frame.save(filename=(outdir + '/' + ('0' * (zeros - len(str(framecount)))) + str(framecount) + '.jpg'))
                    else:
                        print('frying subsequent images: overlay with previous??')
                        with Image(tmpfile) as previous:
                            with Image(frame) as new:
                                previous.composite(new, left=0, top=0)
                                with Image(previous) as img:
                                    img.save(filename=tmpfile)
                                previous.modulate(200, -800)
                                previous.evaluate(operator='gaussiannoise', value=0.05)
                                # previous.function('sinusoid', params)
                                previous.save(filename=(outdir + '/' + ('0' * (zeros - len(str(framecount)))) + str(framecount) + '.jpg'))
                    framecount += 1
            os.remove(tmpfile)
        frames = sorted(glob.glob(outdir + '/*.jpg'))
        with Image() as final:
            for frame in frames:
                with Image(filename=frame) as img:
                    final.sequence.append(img)
            final.type='optimize'
            final.save(filename=outfile)
        combine = True
    return outfile, None

if not os.path.isdir(cwd):
    os.mkdir(cwd)
else:
    for filename in glob.glob(cwd + 'modulate*.jpg'):
        os.remove(filename)

def main():
    mkgif('./testing_overlay/signal-2018-12-15-201849.gif')

main()
