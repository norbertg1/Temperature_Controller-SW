# -*- coding: utf-8 -*-
import base64


def pic2str(file, functionName):
    pic = open(file, 'rb')
    content = '{} = {}\n'.format(functionName, base64.b64encode(pic.read()))
    pic.close()

    with open('WhereToClick_buttons/output_imgtostring.py', 'w') as f:
        f.write(content)


if __name__ == '__main__':
    pic2str('WhereToClick_buttons/PX5_stop_button.bmp', 'PX5_Stop')
