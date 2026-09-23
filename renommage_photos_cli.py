import os, re, json, readline
from sys import exit
# from pathlib import Path
# from os.path import basename, splitext, abspath
# from prompt_toolkit import prompt
# from prompt_toolkit.completion import PathCompleter
from typing import List
# import exifread, string
# 
# import exifread

from constants import *
from set_colors import *

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
    valid_resp_list.append(new[1])
    return valid_resp_list

def process_response_loop(messages: dict, valid_resp_list: list, only_upper:bool, root_path: str, items: dict):
    resp_ok = ''
    while True:
        resp = get_and_check_resp(valid_resp_list)
        if not resp:
            continue
        elif resp.upper() == 'N':
            while not resp_ok.upper() == 'O':
                msg = 'INPUT_NEW_ITEM_MSG' if only_upper else 'INPUT_NEW_SUB_CAT_MSG' 
                msg = messages[msg]
                new_item = input(set_blue(msg))
                if only_upper:
                    new_item = new_item.upper()
                path_to_new_item = root_path+new_item
                if new_item in items.values():
                    msg = SELECT_DIRECTORY_MESSAGES['ITEM_ALREADY_EXISTS_MSG']
                    print(set_yellow(msg))
                    return path_to_new_item
                msg = SELECT_DIRECTORY_MESSAGES['CREATE_ITEM_OK_MSG']
                resp_ok_msg = msg+' '+set_blue(path_to_new_item) + ' (O/N, par défaut N) ? '
                resp_ok = input(resp_ok_msg)
            print('CRÉER '+ path_to_new_item)
            try:
                os.makedirs(path_to_new_item)
            except FileExistsError:
                print('FileExistsError')
            return path_to_new_item
        elif resp.upper() == 'D':
            return '@'
        else:
            path_to_item = root_path+items[resp]
            return path_to_item

def select_category(dir_:str, only_upper:bool) -> str:
    """Select category where to save pictures if only_upper (by convention, categories are upper case)
        Select subcategory where to save pictures if not only_upper
    """
    msg = EXISTING_CATEGORIES_MSG if only_upper else EXISTING_SUB_CATEGORIES_MSG
    print(set_blue(msg))
    categories = get_choices(dir_, only_upper)
    valid_resp_list = creates_valid_resp_list(len(categories), ['N', 'D'])
    if only_upper:
        categories['D'] = SORT_BY_DATE_MSG
    categories['N'] = CREATE_NEW_CAT_MSG if only_upper else CREATE_NEW_SUB_CAT_MSG
    display_choices(categories)
    path_ = process_response_loop(SELECT_CATEGORY_MESSAGES, valid_resp_list, only_upper, dir_ , categories)
    return path_+'/'

def unused():
# def select_dest_dir():
#     """Returns rep (within the proper category) to store renamed pictures"""
#     path_to_category = select_category()
#     choices = get_choices(path_to_category, False)
#     valid_resp_list = creates_valid_resp_list(len(choices), ['N'])
#     choices['N'] = CREATE_NEW_DIR_MSG
#     print(set_blue(SELECT_DEST_DIR_MSG))
#     display_choices(choices)
#     dest_dir = process_response_loop(SELECT_DIRECTORY_MESSAGES, valid_resp_list, False, path_to_category, choices)
#     return dest_dir

# def create_date_part_from_nef(file:str, modifier:str)->str:
#         months_as_letter = string.ascii_uppercase[0:12]
#         with open(file, 'rb') as img_file:
#             tags = exifread.process_file(img_file)
#             exif_date = str(tags['EXIF DateTimeOriginal'])
#             year = exif_date[0:4]
#             month = exif_date[5:7]
#             day = exif_date[8:10]
#             date = '-'.join([year, month, day])
#             i_month = int(month)
#             month_as_letter = months_as_letter[i_month-1:i_month]
#             compressed_date = year[-1]+month_as_letter+day
#             date_part = date+'_('+compressed_date+modifier+')'
#             return date_part
#
# def process_nef(file:str, base:str, modifier: str, file_num: int, description:str):
#     """Rename NEF (Nikon) picture file including .xmp file if present"""
#     # (2019-12-13)_001__DSC8376-9L13_neige_gache_et_terrasse_est.NEF
#     abbrev_month = [x for x in range(12)]
#     if not '_' in base:
#         base = '_'+base
#     os.chdir('/home/camille/Images/tmp_nef_map')
#     date_part = create_date_part_from_nef(file, modifier)
#     tmp, ext = os.path.splitext(file)
#   
#     new_name = date_part + '_' + f"{file_num:03}" + '_[' + base +']_' + description + ext
#     print('nwnwnw', new_name)
#   
# def process_jpg_iphone(file, base, ext):
#     """Rename JPEG picture file taken with an iphone (presently, SE 2020 model)"""
#     pass
# def process_noname(file, base, ext):
#     """Rename picture taken with an unknown camera"""
#     pass
# def create_ext_filters() -> dict:
#     """Creates filters for NEF and JP(E)G files. Returns a tuple of filters"""
#     re_nef_ext = re.compile(r".*\.nef$", re.IGNORECASE)     # nef filter
#     re_jpg_ext = re.compile(r".*\.jpe?g$", re.IGNORECASE)   # jpg filter
#     return {NEF_EXT:re_nef_ext, JPG_EXT:re_jpg_ext}
# def reject_filter(file: str) -> bool:
#     """ directories to be rejected: 'lost+found' and any hidden ones"""
#     try:
#         file.index('lost+found')
#         return False
#     except ValueError:
#         pass
#     if file.startswith('./.'):
#         return False

#     return True
# def create_base_filters() -> dict:
#     """Creates filters for original from camera names (base names)"""
#     re_nef_base = re.compile(r".*(DSC_?\d{4}).*\.(NEF|nef)$")                       # Nikon
#     re_jpg_base_iphone = re.compile(r".*(IMG_\d{4}).*\.(JPG|JPEG|jpg|jpeg)$")       # iphone (SE 2020)
#     re_noname_base = re.compile(r".*(XXX-\d{4}).*\.(JPG|JPEG|jpg|jpeg|NEF|nef)$")   # no known name
#     return {NEF_BASE: re_nef_base, JPG_BASE_IPHONE: re_jpg_base_iphone, NONAME_BASE: re_noname_base}

# def enter_type():
#         print("1. NEF")
#         print("2. JPG/JPEG")
#         f_type = " "
#         while f_type not in ["", "1", "2"]:
#             f_type = input("Type de fichiers [par défaut, 1] : ")
#             if f_type == "":
#                 f_type = "1"

#         return int(f_type)-1

# def enter_modifier():
#     return input('Lettre à ajouter (entrée si aucune) :')

    pass

def get_description() -> str:
    print(set_blue(PICTURE_DESCRIPTION_MSG))
    description = input('> ')
    if not description:
        description = 'pas de description'
    description = format_description(description)
    return description

def walk_through():
    dirs_to_visit = list()
    walk_return_lst = list(os.walk(os.getcwd()))
    for f in walk_return_lst:
        if f[2]:
            dirs_to_visit.append(f[0])
    dirs_to_visit.sort()
    del dirs_to_visit[0]    # 1st dir contains with_info dict, no pictures
    return dirs_to_visit
        

def do_processing():
    """Figure out which types of pictures are presents"""
    # processes = {NEF_BASE: process_nef, JPG_BASE_IPHONE: process_jpg_iphone, NONAME_BASE: process_noname}
    with_info = get_with_info_file()    # created by renommage_photos_ui (from PictureWithInfo object)
    dirs_to_visit = walk_through()
    for dir_index in range(len(dirs_to_visit)):
        print(dirs_to_visit[dir_index])
        os.chdir(dirs_to_visit[dir_index])
        dir_content = os.listdir()
        print('dircont', dir_content)
        dir_content.sort()
        file_info = get_fileinfo(with_info, dir_content)
        description = get_description()
        new_names = get_newnames(file_info, len(dir_content), description)
        path_to_category = select_category(DEST_DIR_ABS, True)
        if path_to_category == "@/":
            print('CLASSER PAR DATE')
        else:
            path_to_subcategory = select_category(path_to_category, False)
            for new_name in new_names:
                file_to_move = file_info[0][5]
                to_go = path_to_subcategory+new_name
                print('...', file_to_move, to_go)
        print('-'*70)

def get_newnames(file_info, length, description):
        new_names = list()
        for index in range(length):
            file_root = file_info[index]
            new_name = file_root[0]+'('+file_root[1]+')_['+file_root[2]+']-'+description
            counter = file_root[3]
            num_part = f'_{counter:03d}'
            ext_ = file_root[4]            
            new_name = new_name + ('' if length == 1 else num_part) + ext_
            new_names.append(new_name)
        return new_names



def get_with_info_file():
    with_info = dict()
    with open(PRE_SORT_DIR_ABS+WITH_INFO_FILE, 'r') as file:
        with_info = json.load(file)
    return with_info

def get_fileinfo(with_info, dir_content):
    file_info = list()
    counter = 0
    for file in dir_content:
        print('    Fichier : ', file)
        counter += 1
        base, ext_ = os.path.splitext(file)
        date = with_info[base][1]
        compressed_date = with_info[base][3]
        print('Commentaire : ', with_info[base][0])
        num_part = f'_{counter:03d}'
        # file_info = info needed in the following
        # 0:date, 
        # 1:compressed date, 
        # 2:filename (no extension), 
        # 3:count of pictures in the dir,
        # 4:extention
        # 5:filename (full)
        file_info.append((date, compressed_date, base, counter, ext_, file))
    return file_info


def rename_pictures():
    os.chdir(PRE_SORT_DIR_ABS)
    do_processing()
    return

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

def format_description(string: str) -> str:
    while string[0] == ' ':  # get rid of leading spaces
        string = string[1:len(string)]
    while string[len(string) - 1] == ' ':  # get rid of trailing spaces
        string = string[0:len(string) - 1]
    while string.find('  ') > 0:
        string = string.replace("  ", " ")  # replace double spaces with single space
    while string.find(' ') > 0:
        string = string.replace(' ', '_')   # replace spaces with underlines
    while string.find('\'') > 0:
        string = string.replace('\'', '_')  # replace apostrophes whith underlines
    return string

if __name__ == '__main__':
        # process_nef('(2019-12-13)_001__DSC8376-9L13_neige_gache_et_terrasse_est.NEF','_DSC8376','NEF')
        # exit()
    rename_pictures()

    exit(0)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
