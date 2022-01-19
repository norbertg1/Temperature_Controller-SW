# -*- coding: utf-8 -*-
import base64


def pic2str(file, functionName):
    pic = open(file, 'rb')
    content = '{} = {}\n'.format(functionName, base64.b64encode(pic.read()))
    pic.close()

    with open('start_button_img.py', 'w') as f:
        f.write(content)


if __name__ == '__main__':
    pic2str('start_button.png', 'start_button_png')
