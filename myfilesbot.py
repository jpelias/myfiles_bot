import sys
from tgbot import methods
from tgbot import users
from ast import literal_eval
import threading
from datetime import datetime
import re


DEFAULT_FOLDER = {
    'mime_type':'folder',
    'icon':None,
    'content':{}}

DEFAULT_FOLDER_STRUCTURE = {
    'mime_type':'folder',
    'icon':None,
    'content':{
        'Audios':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Images':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Gifs':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Stickers':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Videos':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Documents':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Messages':{
            'mime_type':'folder',
            'icon':None,
            'content':{}}
    }
}

EMOJIS = (8419,  169,   174,   8194,  8195,  8197,  8252,  8265,
          8482,  8505,  8596,  8597,  8598,  8599,  8600,  8601,
          8617,  8618,  8986,  8987,  9194,  9195,  9196,  9200,
          9203,  9410,  9642,  9643,  9654,  9664,  9723,  9724,
          9725,  9726,  9728,  9729,  9742,  9745,  9748,  9749,
          9757,  9786,  9800,  9801,  9802,  9803,  9804,  9805,
          9806,  9807,  9808,  9809,  9810,  9811,  9824,  9827,
          9829,  9830,  9832,  9851,  9855,  9875,  9888,  9889,
          9898,  9899,  9917,  9918,  9924,  9925,  9934,  9940,
          9962,  9970,  9971,  9973,  9978,  9981,  9986,  9989,
          9992,  9993,  9994,  9995,  9996,  9999,  10002, 10004,
          10006, 10024, 10035, 10036, 10052, 10055, 10060,
          10062, 10067, 10068, 10069, 10071, 10084, 10133,
          10134, 10135, 10145, 10160, 10548, 10549, 11013,
          11014, 11015, 11035, 11036, 11088, 11093, 12336,
          12349, 12951, 12953)

DEFAULT_FULL_MIMETYPE_ICONS = {'application/epub+zip':'ðŸ“–',
                               'application/octet-stream':'â¬›',
                               'application/pdf':'ðŸ“•',
                               'audio/midi':'ðŸŽ¼',
                               'audio/x-midi':'ðŸŽ¼',
                               'application/certificate':'ðŸ“',
                               'application/dicom':'ðŸ”¬',
                               'application/javascript':'ðŸ”¨',
                               'application/pgp-encrypted':'ðŸ”’',
                               'application/pgp-keys':'ðŸ”',
                               'application/pgp-signature':'ðŸ”',
                               'application/pkcs7-mime':'ðŸ”’',
                               'application/pkcs7-signature':'ðŸ”',
                               'application/vnd.android.package-archive':'ðŸ“¦',
                               'application/vnd.ms-publisher':'ðŸ”‘',
                               'application/vnd.oasis.opendocument.spreadsheet':'ðŸ“Š',
                               'application/x-executable':'ðŸ’¡',
                               'application/x-java-archive':'â˜•ï¸',
                               'application/x-ms-dos-executable':'ðŸ’©',
                               'application/x-pem-key':'ðŸ”',
                               'application/x-php':'ðŸ”¨',
                               'application/x-sharedlib':'â¬›',
                               'application/x-shellscript':'ðŸ§',
                               'application/x-shockwave-flash':'ðŸŽ¬',
                               'application/x-trash':'â™»ï¸',
                               'application/x-compressed-tar':'ðŸ“¦',
                               'application/x-wine-extension-ini':'ðŸ·',
                               'application/zip':'ðŸ“¦',
                               'folder':'ðŸ“',
                               'image/gif':'ðŸŽ¡',
                               'image/jpeg':'ðŸŒ‡',
                               'image/png':'ðŸŒŒ',
                               'image/svg+xml':'âž°',
                               'image/x-xcf':'ðŸŒ ',
                               'image/webp':'ðŸ˜ƒ',
                               'telegram/audio':'ðŸ”ˆ',
                               'telegram/contact':'ðŸ“±',
                               'telegram/location':'ðŸ“',
                               'telegram/message':'ðŸ’¬',
                               'telegram/photo':'ðŸ“·',
                               'telegram/url-chat':'ðŸ‘¥',
                               'telegram/url-contact':'ðŸ‘¤',
                               'telegram/url-stickerpack':'ðŸŽ',
                               'text/css':'ðŸŽ¨',
                               'text/html':'ðŸŒ',
                               'text/x-c++src':'ðŸ‘¾',
                               'text/x-csrc':'ðŸ‘¾',
                               'text/x-makefile':'ðŸ”¨',
                               'text/x-markdown':'ðŸ““',
                               'text/x-python':'ðŸ'}

DEFAULT_MIMETYPE_ICONS = {'audio':'ðŸŽµ',
                          'text':'ðŸ“„',
                          'image':'ðŸŒ‡',
                          'video':'ðŸŽ¬',
                          'application':'ðŸ”´'}

DEFAULT_ICON = 'â”'


def position_to_path(position):
    path = '/'
    for folder in position:
        path += folder + '/'
    return path


def is_empty(storage):
    if len(storage.keys()) == 0:
        return True
    return False

def display_folder(chat_id,storage,position,selection = None):

    storage = get_element(storage,position)['content']
    elements = list(storage.keys())
    elements = sorted(elements, key=lambda s: s.lower())
    folder_elements = []
    file_elements = []

    for element in elements:
        if storage[element]['mime_type'] == 'folder':
            folder_elements.append(element)
        else:
            file_elements.append(element)
    elements = folder_elements + file_elements
    print(elements)
    message = position_to_path(position)

    if selection != None:
        keyboard = [['âœ–ï¸End selection','â–ª Select all','â–« Unselect all']]

        if len(selection) > 0:
            if len(selection) == 1:
                keyboard.append(['âœ Rename','ðŸ”µ Change icon','â„¹ Properties','âŒ Remove','ðŸ“‘ Copy','âœ‚ Cut'])
            else:
                keyboard.append(['âŒ Remove','ðŸ“‘ Copy','âœ‚ Cut'])
    else:
        keyboard = [['âž• Folder']]
        if not is_empty(storage):
            keyboard[0].append('â˜‘ Select')
        clipboard = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'clipboard', '{}'))
        if not clipboard == {}:
            keyboard[0].append('ðŸ“‹ Paste')

    if position == [] or selection != None:
        responses = {}
    else:
        keyboard.append(['â¬† ..'])
        responses = {'â¬† ..':'..'}

    for element in elements:
        icon = storage[element]['icon']
        if icon == None:
            try:
                icon = DEFAULT_FULL_MIMETYPE_ICONS[storage[element]['mime_type']]
            except KeyError:
                not_full_icons = set(literal_eval(users.get_conf_value('recolection', 'General', 'not-full-icons', '{}')))
                not_full_icons.add(storage[element]['mime_type'])
                users.update_conf('recolection', 'General', 'not-full-icons', not_full_icons)
                try:
                    icon = DEFAULT_MIMETYPE_ICONS[storage[element]['mime_type'].split('/')[0]]
                except KeyError:
                    not_icons = set(literal_eval(users.get_conf_value('recolection', 'General', 'not-icons', '{}')))
                    not_icons.add(storage[element]['mime_type'])
                    users.update_conf('recolection', 'General', 'not-icons', not_icons)
                    icon = DEFAULT_ICON

        if selection == None:
            line = icon + ' ' + element

        elif element in selection:
            line = 'ðŸ”³ ' + icon + ' ' + element
        else:
            line = 'â—» ' + icon + ' ' + element

        message += '\n' + line
        responses[line] = element
        keyboard.append([line])


    users.update_conf(chat_id, 'General', 'responses', responses)
    methods.send_message(chat_id,
                         message,
                         reply_markup = {'keyboard':keyboard,
                                         'resize_keyboard':True})

def has_emojis(string):
    for character in string:
        if (is_a_emoji(character)):
            return True
    return False

def is_a_emoji(string):
    if ord(string) >= 126980 or ord(string) in EMOJIS:
        return True
    else:
        return False


def get_element(storage,element_path):
    try:
        for folder in element_path:
            storage = storage['content'][folder]
        return storage
    except KeyError:
        return None


def set_element(storage,element_path,element,k=None):
    keys = ''
    for folder in element_path:
        keys += '[\'content\'][\'' + folder + '\']'
    for key in element.keys():
        if type(element[key]) == str:
            value = '\'' + element[key] + '\''
        else:
            value = str(element[key])
        if k:
            print('storage' + str(keys) + '[\'' + str(k) + '\'][\'' + str(key) + '\']=' + str(value))
            exec('storage' + keys + '[\'' + k + '\'][\'' + key + '\']=' + value)
        else:
            exec('storage' + keys + '[\'' + key + '\']=' + value)

    return storage


def del_element(storage,element_path):
    keys = ''
    for folder in element_path:
        keys += '[\'content\'][\'' + folder + '\']'
    exec('del storage' + keys )


def copy_elements(chat_id, storage, position, selected):
    clipboard = {}
    for element in selected:
        clipboard[element] = get_element(storage,position + [element])
    users.update_conf(chat_id, 'General',
                    'clipboard', clipboard)


def protect_string(string):
    return string.replace('\\','\\\\').replace('\'','\\\'').replace('\n','')


def open_element(chat_id,element_path):
    storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
    if element_path[-1] == '..':
        element_path = element_path[0:-2]
    element = get_element(storage,element_path)
    if element:
        if element['mime_type'] == 'folder':
            users.update_conf(chat_id, 'General', 'position', element_path)
            display_folder(chat_id,storage,element_path)
        elif element['mime_type'] == 'telegram/audio' or element['mime_type'] == 'audio/telegram':
            methods.send_audio(chat_id,
                               element['file_id'])
            display_folder(chat_id,storage,element_path[0:-1])
        elif element['mime_type'] == 'telegram/contact':
            profile_photo = methods.get_user_profile_photos(element['user_id'],limit = 1)
            methods.send_photo(chat_id,
                               profile_photo['result']['photos'][0][0]['file_id'],
                               element['first_name'] + ' ' + element['last_name'] + '\n' +\
                                    '+' + element['phone_number'],)
            methods.send_message(chat_id,
                                 element['first_name'] + ' ' + element['last_name'] + '\n' +\
                                    '+' + element['phone_number'] + '\n' +\
                                    str(element['user_id']))
            display_folder(chat_id,storage,element_path[0:-1])
        elif element['mime_type'] == 'telegram/location':
            methods.send_location(chat_id, element['latitude'], element['longitude'])
            display_folder(chat_id,storage,element_path[0:-1])
        elif element['mime_type'] == 'telegram/message':
            methods.forward_message(chat_id,
                                    chat_id,
                                    element['message_id'])
            display_folder(chat_id,storage,element_path[0:-1])
        elif element['mime_type'] == 'telegram/photo':
            methods.send_photo(chat_id,
                               element['file_id'])
            display_folder(chat_id,storage,element_path[0:-1])
        elif element['mime_type'] == 'telegram/url-stickerpack':
            methods.send_message(chat_id,
                                 'https://telegram.me/addstickers/' + element['stickerpack_name'])
            display_folder(chat_id,storage,element_path[0:-1])
        elif element['mime_type'] == 'telegram/url-chat':
            methods.send_message(chat_id,
                                 'https://telegram.me/joinchat/' + element['group_name'])
            display_folder(chat_id,storage,element_path[0:-1])
        elif element['mime_type'] == 'telegram/url-contact':
            methods.send_message(chat_id,
                                 'https://telegram.me/' + element['contact_name'])
            display_folder(chat_id,storage,element_path[0:-1])
        else:
            methods.send_document(chat_id,
                                  element['file_id'])
            display_folder(chat_id,storage,element_path[0:-1])
    else:
        methods.send_message(chat_id, 'âš  ' + position_to_path(element_path) + ' does not exists')
        display_folder(chat_id,
                       storage,
                       literal_eval(users.get_conf_value(chat_id, 'General',
                                                         'position', '[]')))


def perform(chat_id, text):
    position = literal_eval(users.get_conf_value(chat_id, 'General',
                                                 'position', '[]'))

    task = users.get_conf_value(chat_id, 'General',
                                'task', '')

    responses = literal_eval(users.get_conf_value(chat_id, 'General',
                                        'responses', '{}'))
    try:
        text = responses[text]
    except KeyError:
        pass

    if text == '/start':
        storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
        display_folder(chat_id,storage,position)
    elif task == 'â˜‘':
        selected = literal_eval(users.get_conf_value(chat_id, 'General',
                                                 'selected', '[]'))

        storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))

        responses =literal_eval(users.get_conf_value(chat_id, 'General',
                                         'responses', '{}'))
        try:
            text = responses[text]
        except KeyError:
            pass

        text = text.replace(chr(65039),'')

        if is_a_emoji(text[0]):
            code = text[0]
        else:
            code = None

        if code == 'âœ–':
            users.update_conf(chat_id, 'General',
                          'task', '')
            users.update_conf(chat_id, 'General',
                          'selected', '[]')
            display_folder(chat_id,storage,position)
        elif code == 'â–ª':
            selected = list(get_element(storage,position)['content'].keys())
            users.update_conf(chat_id, 'General',
                          'selected', str(selected))
            display_folder(chat_id,storage,position,selected)
        elif code == 'â–«':
            selected = []
            users.update_conf(chat_id, 'General',
                          'selected', '[]')
            display_folder(chat_id,storage,position,selected)
        elif code == 'âŒ':
            for element in selected:
                element = protect_string(element)
                del_element(storage,position + [element])

            users.update_conf(chat_id, 'General',
                              'storage', str(storage))
            users.update_conf(chat_id, 'General',
                          'task', '')
            users.update_conf(chat_id, 'General',
                          'selected', '[]')
            display_folder(chat_id,storage,position)

        elif code == 'ðŸ“‘':
            copy_elements(chat_id, storage, position, selected)
            users.update_conf(chat_id, 'General',
                          'task', '')
            users.update_conf(chat_id, 'General',
                          'selected', '[]')
            display_folder(chat_id,storage,position)

        elif code == 'âœ‚':
            copy_elements(chat_id, storage, position, selected)
            for element in selected:
                element = protect_string(element)
                del_element(storage,position + [element])
            users.update_conf(chat_id, 'General',
                              'storage', str(storage))
            users.update_conf(chat_id, 'General',
                          'task', '')
            users.update_conf(chat_id, 'General',
                          'selected', '[]')
            display_folder(chat_id,storage,position)

        elif code == 'âœ' and len(selected) == 1:
            users.update_conf(chat_id, 'General',
                            'task', 'âœ')
            methods.send_message(chat_id, 'Insert a new name:',reply_markup = {'keyboard': [['âœ– Cancel']],
                                            'resize_keyboard':True})
            users.update_conf(chat_id, 'General', 'position', position + selected)
        elif code == 'ðŸ”µ' and len(selected) == 1:
            users.update_conf(chat_id, 'General',
                            'task', 'ðŸ”µ')
            methods.send_message(chat_id, 'Send an emoji:',reply_markup = {'keyboard': [['ðŸ”µ Default','âœ– Cancel']],
                                            'resize_keyboard':True})
            users.update_conf(chat_id, 'General', 'position', position + selected)
        elif code == 'â„¹' and len(selected) == 1:
            users.update_conf(chat_id,
                              'General',
                              'position',
                              position + selected)



            methods.send_message(chat_id, 'â›” Not implemented')
        elif text in get_element(storage,position)['content']:
            if text in selected:
                selected.remove(text)
            else:
                selected.append(text)
            users.update_conf(chat_id, 'General',
                          'selected', selected)
            display_folder(chat_id,storage,position,selected)
        else:
            methods.send_message(chat_id, 'âš  ' + text + ' does not exists')
    elif task == 'âœ':
        if text[0] == 'âœ–':
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            users.update_conf(chat_id, 'General', 'position', position[0:-1])
            users.update_conf(chat_id, 'General', 'task', '')
            users.update_conf(chat_id, 'General', 'selected', '[]')
            display_folder(chat_id,storage,position[0:-1])
        elif text == '.' or text == '..':
            methods.send_message(chat_id, 'â›” Name can not be "." or ".."\nInsert another folder name:')
        elif has_emojis(text):
            methods.send_message(chat_id, 'â›” Name can not contain emojis\nInsert another folder name:')
        else:
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            element = get_element(storage,position)
            if text in get_element(storage,position[0:-1])['content'].keys():
                methods.send_message(chat_id, 'â›” There is already a folder named ' + text + '\nInsert another folder name:')
            else:
                print(storage,position[0:-1],{text:element})
                storage = set_element(storage,position[0:-1],{text:element},'content')
                del_element(storage,position)
                users.update_conf(chat_id, 'General', 'storage', str(storage))
                users.update_conf(chat_id, 'General', 'position', position[0:-1])
                users.update_conf(chat_id, 'General', 'task', '')
                users.update_conf(chat_id, 'General', 'selected', '[]')
                display_folder(chat_id,storage,position[0:-1])

    elif task == 'ðŸ”µ':
        if is_a_emoji(text[0]) and len(text) == 1:
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            storage = set_element(storage,position,{'icon':text})
            users.update_conf(chat_id, 'General', 'storage', str(storage))
            users.update_conf(chat_id, 'General', 'position', position[0:-1])
            users.update_conf(chat_id, 'General', 'task', '')
            users.update_conf(chat_id, 'General', 'selected', '[]')
            display_folder(chat_id,storage,position[0:-1])
        elif text == 'âœ– Cancel':
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            users.update_conf(chat_id, 'General', 'position', position[0:-1])
            users.update_conf(chat_id, 'General', 'task', '')
            users.update_conf(chat_id, 'General', 'selected', '[]')
            display_folder(chat_id,storage,position[0:-1])
        elif text == 'ðŸ”µ Default':
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            storage = set_element(storage,position,{'icon':None})
            users.update_conf(chat_id, 'General', 'storage', str(storage))
            users.update_conf(chat_id, 'General', 'position', position[0:-1])
            users.update_conf(chat_id, 'General', 'task', '')
            users.update_conf(chat_id, 'General', 'selected', '[]')
            display_folder(chat_id,storage,position[0:-1])
        else:
            methods.send_message(chat_id, 'â›” Icon must be an emoji')

    elif task == 'âž•':
        if text[0] == 'âœ–':
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            users.update_conf(chat_id, 'General',
                          'task', '')
            display_folder(chat_id,storage,position)
        elif text == '.' or text == '..':
            methods.send_message(chat_id, 'â›” Name can not be "." or ".."\nInsert another folder name:')
        elif has_emojis(text):
            methods.send_message(chat_id, 'â›” Name can not contain emojis\nInsert another folder name:')
        else:
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            text=protect_string(text)
            if text in get_element(storage,position)['content'].keys():
                methods.send_message(chat_id, 'â›” There is already a folder named ' + text + '\nInsert another folder name:')
            else:
                new_folder = {text:DEFAULT_FOLDER}
                storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                    'storage', str(DEFAULT_FOLDER_STRUCTURE)))
                storage = set_element(storage,position,new_folder,'content')
                users.update_conf(chat_id, 'General',
                            'task', '')
                users.update_conf(chat_id, 'General',
                            'storage', storage)
                display_folder(chat_id,storage,position)

    elif text[0] == 'âž•':
        users.update_conf(chat_id, 'General',
                          'task', 'âž•')
        methods.send_message(chat_id, 'Insert folder name:',reply_markup = {'keyboard': [['âœ– Cancel']],
                                         'resize_keyboard':True})
    elif text[0] == 'â˜‘':
        storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
        selected = literal_eval(users.get_conf_value(chat_id, 'General',
                                                 'selected', '[]'))
        users.update_conf(chat_id, 'General',
                          'task', 'â˜‘')
        display_folder(chat_id,storage,position,selected)
    elif text[0] == 'ðŸ“‹':
        clipboard = literal_eval(users.get_conf_value(chat_id, 'General',
                                                      'clipboard', '{}'))
        if clipboard == {}:
            methods.send_message(chat_id,'âš  There is nothing to paste in the clipboard')
        else:
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                        'storage', str(DEFAULT_FOLDER_STRUCTURE)))

            elements = get_element(storage,position)['content'].keys()

            name_error = False

            for clipboard_element in clipboard.keys():
                if clipboard_element in elements:
                    clipboard[correct(clipboard_element)] = clipboard[clipboard_element]
                    del clipboard[clipboard_element]

            if name_error:
                methods.send_message(chat_id, 'â›” There is already a file named ' + name_error + '\nRename the folder before paste')
            else:
                storage = set_element(storage,position,clipboard,'content')
                users.update_conf(chat_id, 'General',
                            'clipboard', '{}')
                users.update_conf(chat_id, 'General',
                            'storage', storage)
        display_folder(chat_id,storage,position)
    else:
        responses =literal_eval(users.get_conf_value(chat_id, 'General',
                                         'responses', '{}'))

        try:
            text = responses[text]
        except KeyError:
            pass

        open_element(chat_id,position + [text])


def document_sended(chat_id, document):
    task = users.get_conf_value(chat_id, 'General',
                                'task', '')
    if task == '':
        storage = literal_eval(users.get_conf_value(chat_id,
                                                    'General',
                                                    'storage',
                                                    str(DEFAULT_FOLDER_STRUCTURE)))
        position = literal_eval(users.get_conf_value(chat_id, 'General',
                                                 'position', '[]'))

        file_name = document['file_name'].replace('\'','\\\'')
        document['icon'] = None

        if file_name in get_element(storage,position)['content'].keys():
            file_name = correct(file_name)


        storage = set_element(storage,position,{file_name:document},'content')
        users.update_conf(chat_id, 'General',
                            'storage', storage)
        display_folder(chat_id,storage,position)


def correct(file_name):
    file_name = file_name.split('.')
    #print(file_name)
    if len(file_name) == 1:
        matches = re.findall('\((\d+)\)$',file_name[0])
        #print(matches)
        if matches == []:
            file_name = file_name[0] + '(1)'
        else:
            file_name = re.findall('(.*)\(\d+\)$',file_name[0])[0] + '(' + str(int(matches[0])+1) + ')'
    else:
        matches = re.findall('\((\d+)\)$',file_name[0])
        #print(matches)
        if matches == []:
            file_name = file_name[0] + '(1).' + file_name[1]
        else:
            file_name = re.findall('(.*)\(\d+\)$',file_name[0])[0] + '(' + str( int(matches[0]) + 1 ) + ').' + file_name[1]
    return file_name


def run():
    running = True
    while running:
        try:
            updates = methods.get_last_updates()
        except KeyboardInterrupt:
            print('\nout')
            quit()
        except:
            pass
        for update in updates['result']:
            try:
                print(update)
                if 'audio' in update['message'].keys():
                    audio = update['message']['audio']
                    audio['file_name'] =  format(datetime.now(),'audio_%Y-%m-%d_%H-%M-%S.ogg')
                    audio['mime_type'] = 'telegram/audio'
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            audio)
                        ).start()
                elif 'document' in update['message'].keys():
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            update['message']['document'])
                        ).start()
                elif 'photo' in update['message'].keys():
                    photo = update['message']['photo'][0]
                    photo['file_name'] =  format(datetime.now(),'photo_%Y-%m-%d_%H-%M-%S.jpg')
                    photo['mime_type'] = 'telegram/photo'
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            photo)
                        ).start()
                    #chat_id = int(update['message']['chat']['id'])
                    #methods.send_message(chat_id, 'â›” To save an image attach it as a file (uncompressed), not as a photo')
                    #display_folder(chat_id,
                                #literal_eval(users.get_conf_value(chat_id,
                                                        #'General',
                                                        #'storage',
                                                        #str(DEFAULT_FOLDER_STRUCTURE))),
                                #literal_eval(users.get_conf_value(chat_id, 'General',
                                                    #'position', '[]')))
                elif 'sticker' in update['message'].keys():
                    sticker = update['message']['sticker']
                    sticker['file_name'] = format(datetime.now(),'sticker_%Y-%m-%d_%H-%M-%S.webp')
                    sticker['mime_type'] = 'image/webp'
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            sticker)
                        ).start()
                elif 'contact' in update['message'].keys():
                    contact = update['message']['contact']
                    contact['file_name'] = contact['first_name'] + ' ' + contact['last_name']
                    contact['mime_type'] = 'telegram/contact'
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            contact)
                        ).start()
                elif 'location' in update['message'].keys():
                    location = update['message']['location']
                    location['file_name'] = str(location['longitude']) + ',' +\
                        str(location['latitude'])
                    location['mime_type'] = 'telegram/location'
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            location)
                        ).start()
                elif 'forward_from' in update['message'].keys():
                    message = {'file_name': 'message from ' + update['message']['forward_from']['first_name'],
                               'mime_type': 'telegram/message',
                               'message_id': update['message']['message_id'],
                               'forward_from': update['message']['forward_from'],
                               'forward_date': update['message']['forward_date']}
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            message)
                        ).start()
                elif 'text' in update['message'].keys():
                    text = update['message']['text']
                    if text.startswith('https://telegram.me/addstickers/'):
                        stickerpack = {'file_name': re.findall('https://telegram.me/addstickers/(.*)',text)[0],
                                       'mime_type': 'telegram/url-stickerpack',
                                       'stickerpack_name': re.findall('https://telegram.me/addstickers/(.*)',text)[0]}
                        threading.Thread(
                            target=document_sended(
                                int(update['message']['chat']['id']),
                                stickerpack)
                            ).start()
                    
                    elif text.startswith('https://telegram.me/joinchat/'):
                        group = {'file_name': re.findall('https://telegram.me/joinchat/(.*)',text)[0],
                                 'mime_type': 'telegram/url-chat',
                                 'group_name': re.findall('https://telegram.me/joinchat/(.*)',text)[0]}
                        threading.Thread(
                            target=document_sended(
                                int(update['message']['chat']['id']),
                                group)
                            ).start() 
                    
                    elif text.startswith('https://telegram.me/'):
                        group = {'file_name': re.findall('https://telegram.me/(.*)',text)[0],
                                 'mime_type': 'telegram/url-contact',
                                 'contact_name': re.findall('https://telegram.me/(.*)',text)[0]}
                        threading.Thread(
                            target=document_sended(
                                int(update['message']['chat']['id']),
                                group)
                            ).start() 
                    else:
                        threading.Thread(
                            target=perform(
                                int(update['message']['chat']['id']),
                                update['message']['text'])
                            ).start()
                else:
                    chat_id = int(update['message']['chat']['id'])
                    methods.send_message(chat_id, 'â›” Unsuported media')
                    display_folder(chat_id,
                                literal_eval(users.get_conf_value(chat_id,
                                                        'General',
                                                        'storage',
                                                        str(DEFAULT_FOLDER_STRUCTURE))),
                                literal_eval(users.get_conf_value(chat_id, 'General',
                                                    'position', '[]')))

            except:
                methods.send_message(int(update['message']['chat']['id']),
                                     'Unexpected ERROR, send this message to @RJornetC to report:\n' + xstr(sys.exc_info()))



if __name__ == '__main__':
    run()
