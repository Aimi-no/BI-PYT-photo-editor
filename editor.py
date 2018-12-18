import numpy as np
from PIL import Image
from pathlib import Path
#import tkinter



#Saves the image
def save(image, filename):
    extension = filename.split('.')[1]
    newfile = filename.split('.')[0] + '_edited.' + extension
    print('Saving image as ' + newfile + ' and closing')
    if extension == 'jpg' or extension == 'jpeg':
        out = Image.fromarray(image, 'RGB')
        out.save(newfile, 'JPEG')

    elif extension == 'png':
        out = Image.fromarray(np.uint8(image), 'RGBA')
        out.save(newfile, 'PNG')



print('For help type in \'help\' or type \'help command\' to get detailed information about command')
#using intext to handle commands
intext = ''

filename = ''

while intext != 'end':
    try:
        intext = input()
    except ValueError:
        print('Input not valid')
        intext = ''
    except EOFError:
        print('EOF')
        intext = ''
    except KeyboardInterrupt:
        print('Interrupted')
        intext = ''

    #documentation
    if intext.startswith('help'):
        instructions = intext.split(' ')
        if len(instructions) == 1:
            print('Type \'end\' to exit the program\n'
                  'Type \'load filename\' to load a picture named filename, only jpeg supported\n'
                  'Type \'close\' to close the picture you have been editing\n'
                  'Type \'mirror x\' to mirror image around x-axis or \'mirror y\' to mirror image around y-axis\n'
                  'Type \'rotate X\', where X equals the rotation in degrees (multiple of 90) to rotate the picture\n'
                  'Type \'negative\' to inverse the image colours\n'
                  'Type \'grayscale\' to convert the image to grayscale\n'
                  'Type \'sepia\' to apply a sepia filter\n'
                  'Type \'brightness X\', where X is an int from -100 to 100, to increase/decrease the '
                  'brightness of the image\n'
                  'Type \'sharpen\' to sharpen the image\n'
                  'Type \'channels \'colour\' X\' where color is \'red/green/yellow\' and X is number from -10 to 10'
                  ' to increase/decrease chosen colour channel')
        elif instructions[1] == 'end':
            print('Type \'end\'. Exits the photo editor but does not save the image.')
        elif instructions[1] == 'load':
            print('Type \'load filename\' to load an image. This command loads the image to be edited. '
                  'Will not load an image when there is already one loaded. Only jpeg and png images supported')
        elif instructions[1] == 'close':
            print('Type \'close\'. Saves the picture as \'filename_edited\' and closes the picture. '
                  'Now you can load another one.')
        elif instructions[1] == 'mirror':
            print('Type \'mirror x\' to mirror image around x-axis or \'mirror y\' to mirror image around y-axis. '
                  'Flips the image horizontally for x-axis and vertically for y-axis.')
        elif instructions[1] == 'rotate':
            print('Type \'rotate X\', where X equals the rotation in degrees to rotate the picture. '
                  'The angle must be multiple of 90, can be negative. 90° rotation rotates the image to the left, '
                  '270° equals to right rotation. -90° equals to 270°')
        elif instructions[1] == 'negative':
            print('Type \'negative\' to invert colours of the image. Creates image with (255 - colorOfOriginal) colour.')
        elif instructions[1] == 'grayscale':
            print('Type \'grayscale\'. Converts the image colours to shades of gray.')
        elif instructions[1] == 'sepia':
            print('Type \'sepia\'. Applies a sepia filter on the image, making all the colours in shades of brown. '
                  'Creates vintage look.')
        elif instructions[1] == 'brightness':
            print('Type \'brightness X\'. X is a number from -100 to 100. Changes the brightness of the image. '
                  'If X is negative it darkens the image, if it\' positive it lightens it.')
        elif instructions[1] == 'sharpen':
            print('Type \'sharpen\'. Sharpens the image.')
        elif instructions[1] == 'channels':
            print('Type \'channels \'colour\' X\'. Colour represents the colour chanel you want to be modified, '
                  'can be \'red\', \'green\' or \'blue\'. X is a number from -10 to 10, indicates the amount '
                  'of increase/decrease of the colour channel.')

    #ends the editor, if there is image loaded, asks if user wants to save it
    elif intext == 'end':
        if filename != '':
            print('Your image is not saved, do you wish to save it? [yes/no]')
            try:
                response = input()
                if response == 'yes':
                    save(image, filename)
                    filename = ''
                    print('Done')
            except ValueError:
                print('Input not valid')
            except EOFError:
                print('EOF')
            except KeyboardInterrupt:
                print('Interrupted')

#-------------------LOAD----------------#
    #loads the image to work with
    elif intext.startswith('load'):
        if filename != '':
            print('There is already an image loaded, only one image can be edited at a time')
        else:
            filename = intext.split(' ')[1]
            if not Path(filename).exists():
                print('File does not exist')
                filename = ''
            elif filename.split('.')[1] != 'jpg' and filename.split('.')[1] != 'jpeg' and filename.split('.')[1] != 'png':
                print('Wrong file time, only jpeg and png supported, sorry')
                filename = ''
            else:
                print('Loading file: ' + filename)
                im = Image.open(filename)
                image = np.asarray(im)
                print('Done')
                #np.set_printoptions(threshold=np.nan)
                #print(image)

    elif filename != '':
# -------------------CLOSE----------------#
    #Unloads the imag and saves it
        if intext == 'close':
            save(image, filename)
            filename = ''
            print('Done')

#-------------------MIRROR----------------#
        #Mirror around X or Y axis, done by flipping axis
        elif intext.startswith('mirror'):
            axis = intext.split(' ')[1]
            if axis != 'x' and axis != 'y':
                print('Invalid axis')
            else:
                print('Mirroring image around ' + axis + '-axis')
                mirrorimage = image.copy()
                imgsize = image.shape
                if axis == 'x':
                    image = image[::-1, ::, ::]
                else:
                    image = image[::, ::-1, ::]
                print('Done')


#-------------------ROTATE----------------#
        #Rotating image, done by a mix of flippping axis and transpositions
        elif intext.startswith('rotate'):
            try:
                angle = int(intext.split(' ')[1])
            except:
                print('Invalid angle')
                angle = 0
            if angle != 0 and angle % 90 == 0:
                print('Rotating image, angle of rotation is: ' + str(angle))
                imgsize = image.shape
                if angle % 360 == 0: # no rotation
                    pass
                elif (angle % 270 == 0 and angle > 0 ) or (angle < 0 and angle % 270 != 0 and angle % 180 != 0): #rotate right
                    image = np.transpose(image[::-1, ::, ::], axes=[1, 0, 2])
                elif angle % 180 == 0: #rotate upside down
                    image = image[::-1, ::-1, ::]
                else: #rotate left
                    image = np.transpose(image, axes=[1, 0, 2])[::-1, ::, ::]
                print('Done')
            else:
                print('Invalid angle')

#-------------------NEGATIVE----------------#
        #Makes a negative of the picture coloursS
        #pixel = 255 - pixel
        elif intext == 'negative':
            print('Making a negative of the image')
            if image.shape[2] == 4:
                image = np.absolute([255, 255, 255, 0] - image)
            else:
                image = np.uint8(255 - image)
            print('Done')

#-------------------GRAYSCALE----------------#
        #Makes image into grayscale using the following formula for each pixel
        #′Y′=0.2126*R′+0.7152*G′+0.0722*B'
        elif intext == 'grayscale':
            print('Converting image to grayscale')
            #print(image.shape)
            imgsize = image.shape
            grayimage = image.copy()
            for i in range(imgsize[0]):
                for j in range(imgsize[1]):
                    pixel = 0.2126 * image[i][j][0] + 0.7152 * image[i][j][1] + 0.0722 * image[i][j][2]
                    grayimage[i][j][0] = pixel
                    grayimage[i][j][1] = pixel
                    grayimage[i][j][2] = pixel
            image = grayimage
            print('Done')

#-------------------SEPIA----------------#
        #Makes image into shades of brown using following formula for each pixel
        #R = (R * 0.393) + (G * 0.769) + (B * 0.189)
        #G = (R * 0.349) + (G * 0.686) + (B * 0.168)
        #B = (R * 0.272) + (G * 0.534) + (B * 0.131)
        elif intext == 'sepia':
            print('Applying sepia filter')
            #print(image.shape)
            imgsize = image.shape
            sepiaimage = image.copy()
            for i in range(imgsize[0]):
                for j in range(imgsize[1]):
                    red = image[i][j][0]
                    green = image[i][j][1]
                    blue = image[i][j][2]
                    sepiared = 0.393 * red + 0.769 * green + 0.189 * blue
                    sepiagreen = 0.349 * red + 0.686 * green + 0.168 * blue
                    sepiablue = 0.272 * red + 0.534 * green + 0.131 * blue

                    sepiaimage[i][j][0] = sepiared if sepiared < 255 else 255
                    sepiaimage[i][j][1] = sepiagreen if sepiagreen < 255 else 255
                    sepiaimage[i][j][1] = sepiagreen if sepiagreen < 255 else 255
                    sepiaimage[i][j][2] = sepiablue if sepiablue < 255 else 255

            image = sepiaimage
            print('Done')


#-------------------BRIGHTNESS----------------#
        #Increases/decreases image brigthness by multiplying/dividing each pixel by a given value
        elif intext.startswith('brightness'):
            try:
                light = int(intext.split(' ')[1])
            except:
                print('Invalid number')
                light = 0

            if light != 0 and light >= -100 and light <= 100:
                print('Changing brightness of image to ' + str(light) + '%')
                if light < 0:
                    image = image // abs(light)
                elif light > 0:
                    #light = light * 255 // 100
                    idx = (image > 255 // light)
                    image = image * light
                    image[idx] = 255
                print('Done')
            else:
                print('Number does not meet expectations')

#-------------------SHARPEN----------------#
        #Sharpening the image using the formula bellow for each pixel except pixels at the very edge of the image
        # pixel = 9*pixel - neighbours
        elif intext.startswith('sharpen'):
            print('Sharpening edges, this might take a few seconds')
            imgsize = image.shape
            sharpenimage = image.copy()
            for i in range(1, imgsize[0] - 1):
                for j in range(1, imgsize[1] - 1):
                    for k in range(3):
                        pixel = 9 * image[i][j][k] - image[i+1][j+1][k] - image[i+1][j][k] - image[i+1][j-1][k] - image[i][j+1][k] - image[i][j-1][k] - image[i-1][j+1][k] - image[i-1][j][k] - image[i-1][j-1][k]
                    #for col in range(imgsize[2]):
                        if pixel > 0:
                            sharpenimage[i][j][k] = pixel if pixel < 255 else 255
                        else:
                            sharpenimage[i][j][k] = 0

            image = sharpenimage
            print('Done')

#-------------------COLOUR CHANNELS----------------#
        #Changes colours by multiplying/dividing given colour channel by a given value for each pixel
        elif intext.startswith('channels'):
            splittext = intext.split(' ')
            color = splittext[1]
            ratio = int(splittext[2])
            if color == 'red':
                idx = 0
            elif color == 'green':
                idx = 1
            elif color == 'blue':
                idx = 2
            else:
                print('Invalid colour')
                idx = -1
            if idx != -1:
                if ratio >= -10 and ratio != 0 and ratio <= 10:
                    print('Increasing ' + color + ' channel by ' + str(ratio))
                    imgsize = image.shape
                    channelimage = image.copy()
                    for i in range(imgsize[0]):
                        for j in range(imgsize[1]):
                            if(ratio > 0):
                               pixel = image[i][j][idx] * ratio
                               channelimage[i][j][idx] = pixel if pixel < 255 else 255
                            else:
                                ratio = abs(ratio)
                                channelimage[i][j][idx] = image[i][j][idx] // ratio
                    image = channelimage
                    print('Done')

                elif ratio != 0:
                    print('Invalid change ratio')

        else:
            print('Unknown command, type \'help\' to see available commands')
    else:
        print('Unknown command or no loaded image, type \'help\' to see available commands')
