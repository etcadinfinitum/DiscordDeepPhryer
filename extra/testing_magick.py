import os
from wand.image import Image
from shutil import copyfile
import glob

if not os.path.isdir('generating_images_demo'):
    os.mkdir('generating_images_demo')
else:
    for filename in glob.glob('generating_images_demo/*.jpg'):
        os.remove(filename)

def test_modulate(sample):
    outfile = 'generating_images_demo/modulate.jpg'
    if os.path.isfile(outfile):
        os.remove(outfile)
    iWidth = None
    iHeight = None
    with Image(filename=sample) as get_size:
        iWidth = get_size.width
        iHeight = get_size.height
    for y in range(-1000, 1001, 100):
        for x in range(-1000, 1001, 100):
            copy = 'generating_images_demo/src_copy.jpg'
            copyfile(sample, copy)
            xval = str(int((x+1000)/100))
            # if len(xval) == 1:
            #     xval = '0' + xval
            yval = str(int((y+1000)/100))
            # if len(yval) == 1:
            #     yval = '0' + yval
            with Image(filename=copy) as modify:
                modify.modulate(x, y)
                modify.save(filename='generating_images_demo/modulate_%s_%s.jpg' % (xval, yval))
            os.remove(copy)
    
    files = sorted(glob.glob('generating_images_demo/*.jpg'))
    
    with Image(width=iWidth * 21, height=iHeight * 21) as final:
        for idx in range(len(files)):
            with Image(filename=files[idx]) as next_img:
                
                final.composite(image=next_img, top=(idx // 21), left=(idx % 21))
        final.save(filename=outfile)
    return 0

def main():
    test_modulate('stock_images/bce223b38aeed99d.jpeg')

main()
