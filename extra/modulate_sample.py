import os
from wand.image import Image
from shutil import copyfile
import glob
import pdb

modulate_presets_1 = { (-100, -200): 'dark'} 
modulate_presets_2 = { (200, 300): 'default', (-1000, -1000): 'galaxy', (200, -800): 'flir'} 
cwd = './defaults_test/'

def get_images(directory):
    inv_dict_1 = {val: key for key, val in modulate_presets_1.items()}
    inv_dict_2 = {val: key for key, val in modulate_presets_2.items()}
    pdb.set_trace()
    count = 0
    for sample in glob.glob(directory + '*.*'):
        for word in sorted(inv_dict_1.keys()):
            copy = cwd + 'src_copy.jpg'
            copyfile(sample, copy)
            copyfile(copy, cwd + 'modulate_%s_original_1.jpg' % str(count))
            with Image(filename=copy) as modify:
                modify.modulate(inv_dict_1[word][0], inv_dict_1[word][1])
                modify.save(filename = cwd + 'modulate_%s_%s_1.jpg' % (str(count), word))
        for word in sorted(inv_dict_2.keys()):
            copy = cwd + 'src_copy.jpg'
            copyfile(sample, copy)
            copyfile(copy, cwd + 'modulate_%s_original_2.jpg' % str(count))
            with Image(filename=copy) as modify:
                modify.modulate(inv_dict_2[word][0], inv_dict_2[word][1])
                modify.save(filename = cwd + 'modulate_%s_%s_2.jpg' % (str(count), word))
        count += 1

if not os.path.isdir(cwd):
    os.mkdir(cwd)
else:
    for filename in glob.glob(cwd + 'modulate*.jpg'):
        os.remove(filename)

def main():
    get_images('./stock_images/')

main()
