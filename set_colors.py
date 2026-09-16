#COLORS_NUM
WHITE_ID = 0
LIGHTGREEN_ID = 1
MEDIUMPURPLE_ID = 2
SANDYBROWN_ID = 3
LIGHTYELLOW_ID = 4
CORNFLOWERBLUE_ID = 5
FUCHSIA_ID = 6
SIENNA_ID = 7
DARKGREY_ID = 8
PRIMARY_COLOR_ID = CORNFLOWERBLUE_ID
SECONDARY_COLOR_ID = SANDYBROWN_ID
INFO_COLOR_ID = LIGHTGREEN_ID
WARNING_COLOR_ID = LIGHTYELLOW_ID
ERROR_COLOR_ID = FUCHSIA_ID


colors = [ '#ffffff',
           '#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0',
           '#f0027f', '#bf5b17', '#666666']

def set_blue(msg):
    msg = '\033[0;34m'+msg+'\033[00m'
    return msg

def set_red(msg):
    msg = '\033[0;31m'+msg+'\033[00m'
    return msg

def set_yellow(msg):
    msg = '\033[0;33m'+msg+'\033[00m'
    return msg
