import argparse
import os
import sys
import json
import random
import shutil

__GLOBAL_KEY = 0

def __get_arguments():
    '''
    Register and return arguments.
    Argument:
        dir     Location of the folder.
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', required=True, type=str, help='Location of the directory.')
    args = parser.parse_args()
    return args

def __get_plain_address(link, base_dir):
    '''
    If a link starts with base address, remove the base address and return the link.
    '''

    modified_link = link
    if link.startswith(base_dir):
        modified_link = link.lstrip(base_dir)

    return modified_link

def __get_key():
    '''
    Get global key value incremented by 1.
    '''

    global __GLOBAL_KEY
    __GLOBAL_KEY += 1
    return __GLOBAL_KEY

def traverse_dir(dir, base_dir):
    '''
    Traverse the directory and sub directories.
    '''

    parent_data = {
        "title": os.path.split(dir)[1],
        "folder": os.path.isdir(dir),
        "children": [],
        "key": __get_key()
    }
    
    for item in os.scandir(dir):
        if item.is_dir():
            item_data = traverse_dir(item.path, base_dir)
            parent_data["children"].append(item_data)

        if item.is_file():
            child_data = {
                "title": item.name,
                "folder": False,
                "link": __get_plain_address(item.path, base_dir),
                "key": __get_key()
            }
            parent_data["children"].append(child_data)

    return parent_data

def __exit_app(error_msg):
    '''
    Exit the application with the error message.
    '''

    sys.stdout.writelines(error_msg)
    sys.stdout.writelines("\nProgram is exiting...")
    exit(-1)

def __get_metadata():
    '''
    Get metadata from metadata.json
    If metadata.json is not found, or a key is missing, the program will end.
    '''

    background_color = "aliceblue"
    folder_color = "#00b894"
    file_color = "#ff5252"
    heading = "Index"
    metadata_file = os.getcwd() + "\\metadata.json"

    try:
        with open(metadata_file, "r") as metadata:
            json_data = ""
            json_data = json_data.join(metadata.readlines())
            data = json.loads(json_data)
            if data["heading"] != "":
                heading = data["heading"]

            if data["background_color"] != "":
                background_color = data["background_color"]

            if data["folder_color"] != "":
                folder_color = data["folder_color"]

            if data["file_color"] != "":
                file_color = data["file_color"]
    
    except KeyError:
        __exit_app("There was an error accessing key value.")
        
    except FileNotFoundError:
        __exit_app("Metdata file doesn't exist.")

    finally:
        return background_color, folder_color, file_color, heading

def __generate_template(heading):
    '''
    Generates template - index.html page.
    Replaces the heading placeholder with the provided heading.
    '''

    template = ""

    try:
        with open("template.html", "r") as html:
            template = template.join(html.readlines())

    except FileNotFoundError:
        __exit_app("Template file doesn't exist.")
        
    template = template.replace("$$__HEADING__$$", heading)
    return template

def __generate_style(bg_color, folder_color, file_color):
    '''
    Generates required css file.
    Replaces background color, folder color and file color placeholders with the provided values.
    '''

    style = ""
    style_file = os.getcwd() + "\\website_resource\\css\\style.css"

    try:
        with open(style_file, "r") as css:
            style = style.join(css.readlines())

    except FileNotFoundError:
        __exit_app("Style file doesn't exist.")
        
    style = style.replace("$$__BG_COLOR__$$", bg_color)\
            .replace("$$__FOLDER_COLOR__$$", folder_color)\
            .replace("$$__FILE_COLOR__$$", file_color)

    return style

def __generate_files(base_dir):
    '''
    Generates template and css files and copies rest of the required directory structure.
    '''

    resource_dir = base_dir + "\\website_resource"
    template_file = base_dir + "\\index.html"
    style_file = resource_dir + "\\css\\style.css"
    current_dir = os.getcwd()
    current_resource = current_dir + "\\website_resource"

    bg_color, folder_color, file_color, heading = __get_metadata()
    template = __generate_template(heading)
    style = __generate_style(bg_color, folder_color, file_color)

    try:
        if os.path.exists(resource_dir):
            shutil.rmtree(resource_dir)
        
        shutil.copytree(current_resource, resource_dir)

        with open(template_file, "w") as index:
            index.write(template)
        
        with open(style_file, "w") as css:
            css.write(style)       

    except PermissionError:
        __exit_app("Permission to create directory is not granted.")

def __main():
    args = __get_arguments()

    if os.path.isdir(args.dir):      
        dir_list = traverse_dir(args.dir, args.dir)
        __generate_files(args.dir)

        with open(args.dir + "\\website_resource\\listing.json", "w") as jfile:
            jfile.writelines(json.dumps(dir_list))

        sys.stdout.writelines("Done.")

    else:
        __exit_app("No directory provided.")

     
        
if __name__ == "__main__":
    __main()