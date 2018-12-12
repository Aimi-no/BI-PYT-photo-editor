import numpy as np
import PIL as p


print('For help type in \'help\'.')

intext = ''

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
        print('Type \'end\' to exit the program, type \'load filename\' to load a picture named filename, type \'close\' to close the picture you have been editing, TODO: MORE DOCUMENTATION')

    