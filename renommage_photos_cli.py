import os
from sys import exit
from pathlib import Path
from os.path import basename, splitext, abspath
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

import re
import exifread

from constants import *

def reject_filter(file):
    """ directories to be rejected: 'lost+found' and any hidden ones"""
    try:
        file.index('lost+found')
        return False
    except ValueError:
        pass
    if file.startswith('./.'):
        return False
    
    return True

def select_directory():
    """select directory containing to-be-renamed pictures"""
    images_home = IMAGES_HOME
    dir_ok = 'N'
    while not dir_ok.upper() == 'O':
        os.chdir(images_home)
        images_path = prompt(
            "Répertoire : " + images_home,
            completer=PathCompleter(only_directories=True,file_filter=reject_filter)
        )
        if images_path:
            os.chdir(images_path)
        else:
            images_path = IMAGES_HOME
        print('\n\033[0;34m Le répertoire contient les fichiers suivants :\033[00m')
        print('-----------------------------------------------')
        all_files = os.listdir()
        all_files.sort()
        for file in all_files:
            print(file)
        print('-----------------------------------------------')
        dir_ok = input('Est-ce le bon répertoire O/N (par défaut, O) ? ')
        if dir_ok == '':
            dir_ok = 'O'
    return images_path

def create_ext_filters():
    """Creates filters for NEF and JP(E)G files. Returns a tuple of filters"""
    re_nef_ext = re.compile(r".*\.nef$", re.IGNORECASE)     # nef filter
    re_jpg_ext = re.compile(r".*\.jpe?g$", re.IGNORECASE)   # jpg filter
    return {NEF_EXT:re_nef_ext, JPG_EXT:re_jpg_ext}

def create_base_filters():
    """Creates filters for original from camera names (base names)"""
    re_nef_base = re.compile(r"(_?DSC_?\d{4})")     # Nikon
    re_jpg_base_iphone = re.compile(r"(IMG_\d{4})") # iphone (SE 2020)
    return {NEF_BASE: re_nef_base, JPG_BASE_IPHONE: re_jpg_base_iphone}

def process_nef():
    print('Traiter NEF')

def process_jpg():
    print('Traiter JPEG')

def do_processing(filters):
    processes = {NEF_EXT: process_nef, JPG_EXT: process_jpg}
    """Figure out which types of pictures are presents"""
    all_files = os.listdir('.')
    all_files.sort()
    flag = False
    for file in all_files:
        for index in range(len(filters)):
            if bool(filters[EXT_LIST[index]].match(file)):
                processes[EXT_LIST[index]]()
                flag = True
    if not flag:
        print('\033[0;31m Le répertoire ne contient pas de fichiers images\033[00m')
        exit(NO_PICTURE)

    return

def rename_pictures():
    """
    possible extensions are NEF and JPG/JPEG
    """
    select_directory()
    ext_filters = create_ext_filters()
    do_processing(ext_filters)

    # (_?DSC_?\d{4}.*)\.((NEF)|(nef))$

    return















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

    # 3. create destination directory in step 2 of the workflow
    #    (compressed date + modifier + name of the group of pictures)
    directory = basename(start_folder) + modifier # compressed date
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

def enter_modifier():
    return input('Lettre à ajouter (entrée si aucune) :')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # enter parameters
    # group_name = 'le_héron' #enter_group_name()
    # group_modifier = enter_modifier()
    # file_type =  enter_type()
    # move
    rename_pictures()

    exit(0)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
