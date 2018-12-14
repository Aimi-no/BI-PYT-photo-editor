import numpy as np
from PIL import Image
from pathlib import Path

#TODO png handling


print('For help type in \'help\'.')

intext = ''

filename = ''

while intext != 'end':
    try:
        intext = input()
    except ValueError:
        print('Input not valid')
    except EOFError:
        print('EOF')
    except KeyboardInterrupt:
        print('Interrupted')

    if intext == 'help':
        print('Type \'end\' to exit the program\n'
              'Type \'load filename\' to load a picture named filename\n'
              'Type \'close\' to close the picture you have been editing\n'
              'Type \'mirror x\' to mirror image around x-axis or \'mirror y\' to mirror image around y-axis\n'
              'Type \'rotate X\', where X equals the rotation in degrees (multiple of 90) to rotate the picture\n'
              'Type \'negative\' to inverse the image colours\n'
              'Type \'grayscale\' to convert the image to grayscale\n'
              'Type \'lightness X\', where X is an int from -100 to 100, to change the lightness/darkness of the image\n'
              'Type \'edges\' to sharpen edges')

    elif intext == 'end':
        pass
#-------------------LOAD----------------#
    elif intext.startswith('load'):
        if filename != '':
            print('There is already an image loaded, only one image can be edited at a time')
        else:
            filename = intext.split(' ')[1]
            if not Path(filename).exists():
                print('File does not exist')
            else:
                print('Loading file: ' + filename)
                im = Image.open(filename)
                image = np.asarray(im)
                #print(image)

    elif filename != '':
# -------------------CLOSE----------------#
        if intext == 'close':
            newfile = filename.split('.')[0] + '_edited.' + filename.split('.')[1]
            print('Saving image as ' + newfile + ' and closing')
            out = Image.fromarray(image, 'RGB')
            out.save(newfile)
            filename = ''

#-------------------MIRROR----------------#
        elif intext.startswith('mirror'):
            axis = intext.split(' ')[1]
            if axis != 'x' and axis != 'y':
                print('Invalid axis')
            else:
                print('Mirroring image around ' + axis + '-axis')

#-------------------ROTATE----------------#
        elif intext.startswith('rotate'):
            try:
                angle = int(intext.split(' ')[1])
            except:
                print('Invalid angle')
                angle = 0
            if angle != 0 and angle % 90 == 0:
                print('Rotating image, angle of rotation is: ' + str(angle))
            else:
                print('Invalid angle')

#-------------------NEGATIVE----------------#
        #pixel = 255 - pixel
        elif intext == 'negative':
            print('Making a negative of the image')
            image = 255 - image

#-------------------GRAYSCALE----------------#
        #′Y′601=0.299*R′+0.587*G′+0.114*B'
        elif intext == 'grayscale':
            print('Converting image to grayscale')


#-------------------LIGHTNESS----------------#
        elif intext.startswith('lightness'):
            try:
                light = int(intext.split(' ')[1])
            except:
                print('Invalid number')
                light = 0

            if light != 0 and light >= -100 and light <= 100:
                print('Changing lightness of image to ' + str(light) + '%')
                if light < 0:
                    image = image // abs(light)
                elif light > 0:
                    #light = light * 255 // 100
                    idx = (image > 255 // light)
                    image = image * light
                    image[idx] = 255


            else:
                print('Number does not meet expectations')

#-------------------EDGES----------------#
        elif intext.startswith('edges'):
            print('Sharpening edges')
        else:
            print('Unknown command, type \'help\' to see available commands')
    else:
        print('Unknown command or no loaded image, type \'help\' to see available commands')
