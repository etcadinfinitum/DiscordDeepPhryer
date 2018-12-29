import os
from wand.image import Image
from shutil import copyfile
import glob
import pdb

def generate_images(filename):
    outdir = './sine_tests'
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    else:
        for filename in glob.glob(outdir + '/*.*'):
            os.remove(filename)
    # four parameters for sinusoid transform: 
    #    name           current range   result?
    # 1. frequency      1 to 10         ?
    # 2. phase shift    -90 to -25      ?
    # 3. amplitude      0.1 to 0.9      best guess: gray filter
    # 4. bias           0.1 to 0.9      lighten/darken
    for frequency in range(1, 10):
        for phase_shift in range(-90, -30, 15):
            for amplitude in range(1, 9):
                for bias in range(1, 9):
                    params = [frequency, phase_shift, amplitude * 0.1, bias * 0.1]
                    with Image(filename=filename) as img:
                        img.modulate(200, 300)
                        img.function('sinusoid', params)
                        ampl = '%.1f' % params[2]
                        biases = '%.1f' % params[3]
                        img.save(filename= outdir + '/{}_{}_{}_{}.jpg'.format(params[0], params[1], ampl, biases))

def test_frequency_phase(filename):
    outdir = './sine_tests/freq_phase'
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    for frequency in range(1, 11):
        for phase_shift in range(-90, -15, 15):
            params = [frequency, phase_shift, 0.9, 0.5]
            with Image(filename=filename) as img:
                img.modulate(200, 300)
                img.function('sinusoid', params)
                img.save(filename= outdir + '/{}_{}.jpg'.format(frequency, phase_shift))

test_frequency_phase('./stock_images/bce223b38aeed99d.jpeg')

# generate_images('./stock_images/bce223b38aeed99d.jpeg')
