# TODO: for development purpose only
TEMP_DEV = 'tmp/'
#TEMP_DEV = ''

IMAGES_HOME = '/home/camille/Images/'
NEF_EXT = 'NEF'
JPG_EXT = 'JPG'
EXT_LIST = [NEF_EXT, JPG_EXT]

NEF_BASE = 'NEF_BASE'
JPG_BASE_IPHONE = 'JPG_BASE_IPHONE'
PICTURES_BASENAME_LIST = [NEF_BASE, JPG_BASE_IPHONE]

REP_OK_MSG = 'Est-ce le bon répertoire O/N (par défaut, O) ? '
PICTURE_LIST_MSG = '\n\033[0;34m Le répertoire contient les fichiers suivants :\033[00m'
CAT_CHOICE_MSG = 'Choix : '
EXISTING_CATEGORIES_MSG = 'Catégories disponibles ou en créer une nouvelle'
CHOICE_ERROR_MSG = 'Ce choix n\'est pas autorisé'
SELECT_DEST_DIR_MSG = 'Choisir le répertoire de destination'
CREATE_NEW_DIR_MSG = 'Créer un nouveau répertoire'
CREATE_NEW_CAT_MSG = 'Créer une nouvelle catégorie'


INPUT_NEW_CAT_MSG = 'Entrez le nom de la catégorie à créer : '
CATEGORY_ALREADY_EXISTS_MSG = 'Avertissement. Cette catégorie existe déjà'
CREATE_CATEGORY_OK_MSG = 'Confirmez-vous la création de la catégorie '
SELECT_CATEGORY_MESSAGES = {'INPUT_NEW_CAT_MSG': INPUT_NEW_CAT_MSG,
                            'CATEGORY_ALREADY_EXISTS_MSG': CATEGORY_ALREADY_EXISTS_MSG,
                            'CREATE_CATEGORY_OK_MSG': CREATE_CATEGORY_OK_MSG}

NO_PICTURE = 1

CATEGORIES = {'1': 'EXERCICES', '2': 'BALADES'}