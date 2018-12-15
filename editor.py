import numpy as np
from PIL import Image
from pathlib import Path
import tkinter
import matplotlib

#TODO png handling
def findneigbours(image,i,j):
    imgsize = image.shape
    neighbours = np.zeros((imgsize[2]), dtype = int)
    for x in range(i-1, i+2):
        for y in range(j-1,j+2):
            if x != i or y != j:
                neighbours = neighbours + image[x][y]

    return neighbours


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
              'Type \'sepia\' to apply a sepia filter\n'
              'Type \'brightness X\', where X is an int from -100 to 100, to increase/decrease the brightness of the image\n'
              'Type \'sharpen\' to sharpen edges')

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
                print('Done')
                #print(image)

    elif filename != '':
# -------------------CLOSE----------------#
        if intext == 'close':
            newfile = filename.split('.')[0] + '_edited.' + filename.split('.')[1]
            print('Saving image as ' + newfile + ' and closing')
            out = Image.fromarray(image, 'RGB')
            out.save(newfile)
            filename = ''
            print('Done')

#-------------------MIRROR----------------#
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
                    #image = np.rot90(image, k = 3, axes=(-2,-1))
                    #print(rotimage)
                    #image = rotimage
                    #print(image)
                print('Done')
            else:
                print('Invalid angle')

#-------------------NEGATIVE----------------#
        #pixel = 255 - pixel
        elif intext == 'negative':
            print('Making a negative of the image')
            image = 255 - image
            print('Done')

#-------------------GRAYSCALE----------------#
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
        #outputRed = (inputRed * .393) + (inputGreen *.769) + (inputBlue * .189)
        #outputGreen = (inputRed * .349) + (inputGreen *.686) + (inputBlue * .168)
        #outputBlue = (inputRed * .272) + (inputGreen *.534) + (inputBlue * .131)
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
        # pixel = 9*pixel - neighbours
        elif intext.startswith('sharpen'):
            print('Sharpening edges, this might take a few seconds')
            imgsize = image.shape
            sharpenimage = image.copy()
            for i in range(1, imgsize[0] - 1):
                for j in range(1, imgsize[1] - 1):
                    for k in range(imgsize[2]):
                        pixel = 9 * image[i][j][k] - image[i+1][j+1][k] - image[i+1][j][k] - image[i+1][j-1][k] - image[i][j+1][k] - image[i][j-1][k] - image[i-1][j+1][k] - image[i-1][j][k] - image[i-1][j-1][k]
                    #for col in range(imgsize[2]):
                        if pixel > 0:
                            sharpenimage[i][j][k] = pixel if pixel < 255 else 255
                        else:
                            sharpenimage[i][j][k] = 0

            image = sharpenimage
            print('Done')

#-------------------SHOW----------------#
 #       elif intext == 'show':
  #          matplotlib.use('Agg')
   #         print('Showing image')
    #        imgsize = image.shape
     #       root = tkinter.Tk()
      #      root.geometry(str(imgsize[0]) + "x" + str(imgsize[1]))
       #     root.title("Image: ")

            #canvas = tkinter.Canvas(root, width=imgsize[0], height=imgsize[1])

            #img = tkinter.PhotoImage(width = WIDTH, height = HEIGHT)

        #    panel = tkinter.Label(root, image=image)
         #   panel.pack(side="bottom", fill="both", expand="yes")

            #image = canvas.create_image((WIDTH, HEIGHT), image=img, anchor=tkinter.SE)
            #canvas.pack()

          #  root.mainloop()
        else:
            print('Unknown command, type \'help\' to see available commands')
    else:
        print('Unknown command or no loaded image, type \'help\' to see available commands')
