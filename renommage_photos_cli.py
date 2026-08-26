import os
from sys import exit
from pathlib import Path
from os.path import basename, splitext, abspath
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from typing import List

import re
import exifread

from constants import *
from set_colors import *

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
        print(PICTURE_LIST_MSG)
        print('-'*46)
        all_files = os.listdir()
        all_files.sort()
        for file in all_files:
            print(file)
        print('-----------------------------------------------')
        dir_ok = input(REP_OK_MSG)
        print('-----------------------------------------------')
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
    re_nef_base = re.compile(r".*(DSC_?\d{4}).*\.(NEF|nef)$")                  # Nikon
    re_jpg_base_iphone = re.compile(r".*(IMG_\d{4}).*\.(JPG|JPEG|jpg|jpeg)$")    # iphone (SE 2020)
    return {NEF_BASE: re_nef_base, JPG_BASE_IPHONE: re_jpg_base_iphone}

def get_choices(dir: str, upcase: bool) -> dict:
    """Return content of a dir as a dictionnary of choices"""
    files = os.listdir(dir)
    files.sort()
    choice_list = dict()
    id = 1
    for file in files:
        if upcase and not file.isupper():
            continue
        choice_list[str(id)] = file
        id += 1
    return choice_list

def display_choices(choices: dict):
    """Displays choices given in a dictionnary"""
    for key, choice in choices.items():
        print(key+':', choice)

def get_and_check_resp(valid_resp_list: list) -> str:
    """Asks for response (choice) and checks it against list of valid response
    """
    resp = input(set_blue(CAT_CHOICE_MSG))
    if not resp.upper() in valid_resp_list:
        print(set_red(CHOICE_ERROR_MSG))
        return ''
    return resp.upper()

def creates_valid_resp_list(length: int, new: List[str]) -> list:
    """Creates valid responses list
        length = number of numeric responses
        new = others non-numeric responses to add (presently, only one possible)
    """
    valid_resp_list = [str(x+1) for x in range(length)]
    valid_resp_list.append(new[0])  #TODO: allows for many additionnal non-numeric responses
    return valid_resp_list

def select_category() -> str:
    """Select category where to save pictures"""
    print(set_blue(EXISTING_CATEGORIES_MSG))
    categories = get_choices(IMAGES_HOME, True)
    valid_resp_list = creates_valid_resp_list(len(categories), ['N'])
    categories['N'] = CREATE_NEW_CAT_MSG    # add possibility to create a new category
    display_choices(categories)
    resp_ok = ''
    while True:
        resp = get_and_check_resp(valid_resp_list)
        if resp.upper() == 'N':
            while not resp_ok.upper() == 'O':
                msg = SELECT_CATEGORY_MESSAGES['INPUT_NEW_CAT_MSG']
                new_category = input(set_blue(msg)).upper()
                path_to_new_category = IMAGES_HOME+TEMP_DEV+new_category
                if new_category in categories.values():
                    msg = SELECT_CATEGORY_MESSAGES['CATEGORY_ALREADY_EXISTS_MSG']
                    print(set_yellow(msg))
                    return path_to_new_category
                msg = SELECT_CATEGORY_MESSAGES['CREATE_CATEGORY_OK_MSG']
                resp_ok_msg = msg + set_blue(IMAGES_HOME+new_category) +' ? '
                resp_ok = input(resp_ok_msg)
            # TODO: for development only, to be rewritten (no try/except stuff) in final version
            try:
                os.makedirs(path_to_new_category)
            except FileExistsError:
                pass
            return path_to_new_category
        else:
            path_to_category = IMAGES_HOME+TEMP_DEV+categories[resp]
            return (path_to_category)

def select_dest_dir():
    """Returns rep (within the proper category) to store renamed pictures"""
    path_to_category = select_category()
    choices = get_choices(path_to_category, False)
    choices['N'] = CREATE_NEW_DIR_MSG
    print(set_blue(SELECT_DEST_DIR_MSG))
    display_choices(choices)

def process_nef(file, base, ext):
    """Rename NEF (Nikon) picture file including .xmp file if present"""
    if not '_' in base:
        base = '_'+base
    exit()

def process_jpg_iphone(file, base, ext):
    """Rename JPEG picture file taken with an iphone (presently, SE 2020 model)"""
    pass

def do_processing(filters):
    """Figure out which types of pictures are presents"""
    processes = {NEF_BASE: process_nef, JPG_BASE_IPHONE: process_jpg_iphone}
    all_files = os.listdir('.')
    all_files.sort()
    flag = False
    for file in all_files:
        for index in range(len(filters)):
            temp = filters[PICTURES_BASENAME_LIST[index]].findall(file)
            if bool(temp):
                if not flag:
                    dest_rep = select_dest_dir()
                    flag = True
                base, ext = temp[0]
                processes[PICTURES_BASENAME_LIST[index]](file, base, ext)
    if not flag:
        print('\033[0;31m Le répertoire ne contient pas de fichiers images\033[00m')
        exit(NO_PICTURE)

    return

def rename_pictures():
    """
    possible extensions are NEF and JPG/JPEG
    """
    select_directory()
    base_filters = create_base_filters()
    do_processing(base_filters)

    return



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
