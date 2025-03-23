import os
from sys import exit
from os.path import basename, splitext, abspath

import re
import exifread

from constants import *

def rename_pictures(g_name, ext_type: int):
    # program should be called from the directory where to-be-renamed pictures lie

    # folders structures : .../STEP 1/decade/compressed date/pictures to be renamed
    # program must be started from the to-be-renamed pictures directory
    # possible extensions are NEF and JPG/JPEG

    searched_ext = ['NEF', 'JPG/JPEG'] [ext_type]

    # 1. check directory
    start_folder = abspath('.')
    all_files = os.listdir(start_folder)
    print('Le répertoire courant est :', start_folder)
    print('Le répertoire courant contient les fichiers suivants :')
    print(all_files)
    dir_ok = input('Est-ce le bon répertoire O/N (par défaut, O) ?')
    if dir_ok.upper() == 'N':
        exit(0)

    # find picture files using filters
    re_nef = re.compile(r".*\.nef$", re.IGNORECASE)     # nef filter
    re_jpg = re.compile(r".*\.jpe?g$", re.IGNORECASE)   # jpg filter
    filters = (re_nef, re_jpg)

    # store them
    pictures_file = []
    for file in all_files:
        if not bool(filters[ext_type].match(file)): # filtering
            continue
        pictures_file.append(file) # store
    if not pictures_file:
        print('Le répertoire ne contient aucun fichier', searched_ext, '!')
        print('Vérifier le répertoire ainsi que le type de fichier image (nef ou jpeg)')
        exit(NO_PICTURE) # no picture of type 'ext_type' in the folder -> exit

    # 2. create decade folder in STEP 2 of the workflow
    decade = start_folder.split('/')[-2]
    decade_step_2 = STEP_2 + '/' + decade
    os.makedirs(decade_step_2, exist_ok=True)

    # 3. create destination directory in step 2 of the workflow (compressed date + name of the group of pictures)
    directory = basename(start_folder) # compressed date
    new_directory = directory + '-' + g_name
    dest_folder = decade_step_2 + '/' + new_directory
    os.makedirs(dest_folder, exist_ok=True)

    # 4. create the fixed parts of the new name of the picture file
    # get the first file
    file1 = pictures_file[0]
    with open(file1, 'rb') as img_file:
        # leading fixed part : date between parenthesis
        tags = exifread.process_file(img_file)
        exif_date = str(tags['EXIF DateTimeOriginal'])
        year = exif_date[0:4]
        month = exif_date[5:7]
        day = exif_date[8:10]
        date = '-'.join([year, month, day])
        fixed_part_1 = '(' + date + ')_'
        # trailing fixed part : new directory (see point 3 above) + ext (nef or jpg/jpeg)
        original_ext = splitext(file1)[1].upper()
        fixed_part_2 = '_' + new_directory + original_ext

    # 5. move picture files
    count = 0
    for file in pictures_file:
        count += 1
        count_str = str("{:03d}".format(count)) # index, part of the new name of the file (see below)
        # original name
        original_name = splitext(file)[0] # e.g. _DSC6502
        # move files
        file_to_be_moved = original_name + original_ext
        # structure of the new name :
        # fixed part 1
        #       (yyyy-mm-dd)
        #       underscore
        # variable part
        #       index (3 digits)
        #       underscore
        #       [original name] (between brackets, from the camera)
        # fixed part 2
        #       underscore
        #       new directory (see above)
        #       original extension (nef or jpg/jpeg)
        new_name = fixed_part_1 + count_str + "_[" + original_name + "]" + fixed_part_2
        moved_file = dest_folder + "/" + new_name
        print( count_str+".", file_to_be_moved, "-->", moved_file)
        os.replace(file_to_be_moved, moved_file )

    # 6. cleaning
    os.chdir("../")
    if os.listdir(directory):
         print(os.listdir(directory))
         os.replace(directory, directory+"-autres")
    else:
        os.removedirs(directory)

    return

def suppress_spaces(string):
    while string[0] == ' ':  # get rid of leading spaces
        string = string[1:len(string)]

    while string[len(string) - 1] == ' ':  # get rid of trailing spaces
        string = string[0:len(string) - 1]

    while string.find('  ') > 0:
        string = string.replace("  ", " ")  # replace double spaces with single space

    return string

def enter_group_name():
    group_name = input("Nom du groupe de photos : ")
    group_name = suppress_spaces(group_name).replace(" ", "-").lower()
    return group_name

def enter_type():
        print("1. NEF")
        print("2. JPG/JPEG")
        f_type = " "
        while f_type not in ["", "1", "2"]:
            f_type = input("Type de fichiers [par défaut, 1] : ")
            if f_type == "":
                f_type = "1"

        return int(f_type)-1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # enter parameters
    group_name = enter_group_name()
    file_type =  enter_type()# ---> replace with a call to enter_type()
    # move
    rename_pictures(group_name, file_type)

    exit(0)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
