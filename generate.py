import os
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from shutil import copyfile
from PIL import Image

# creating photo page


def create_photo_page(root, name, array):
    path = os.path.join(root, name)
    print("creating photo page", path, array)
    # open file
    with open(path, 'r') as file:
        # creating object from markdown file
        parsed_md = markdown(file.read(), extras=['metadata'])
        obj = {
            'meta': parsed_md.metadata,
            'array': array
        }
        # creating and saving page
        create_save_result(root, name, parsed_md, obj)

# creating single page


def create_single_page(root, name):
    path = os.path.join(root, name)
    print("creating: ", name, "root: ", root)
    with open(path, 'r') as file:
        # creating the data
        parsed_md = markdown(file.read(), extras=['metadata'])
        obj = {
            'meta': parsed_md.metadata,
            'content': parsed_md
        }
        # creating and saving page
        create_save_result(root, name, parsed_md, obj)

# creating index page


def create_index(path, name, obj):

    # read the md file containing the data to be displayed
    with open(root+"/" + name, 'r') as file:
        parsed_md = markdown(file.read(), extras=['metadata'])

        # creating and saving page
        create_save_result(root, name, parsed_md, obj)


def create_save_result(root, name, parsed_md, obj):
    path = os.path.join(root, name)
    # create the environment variable
    e = Environment(loader=FileSystemLoader("./input/layout"))
    env = e.get_template(parsed_md.metadata["layout"])
    result = env.render(data=obj)
    # save page to html format
    save_path = root.replace("input/index", "output")
    # save page to html format
    print("saving path: -----------> ", save_path)
    # create folder if not exists
    Path(save_path).mkdir(parents=True, exist_ok=True)
    # saving result
    with open(save_path + "/index.html", "w+") as file:
        file.write(result)

# get the list of only the photos of that direcotory


def get_list_photos(files):
    array = [x for x in files if ".md" not in x]
    print("directory:", array)
    return array

# get all the files in sub the directory


def get_data_directory(dirs):
    array = []
    for name in dirs:
        path = os.path.join(root, name, name + ".md")
        list_all_photos = []
        # taking 3 photos to display in the strip-bar
        if("photography" in root):
            # taking 3 photos from each folder
            for files in os.walk(root+"/"+name, topdown=False):
                list_directory = []
                for file in files[2]:
                    if(".md" not in file):
                        list_all_photos.append(file)

        # read metadata of each file in the sub directory
        with open(path, 'r') as file:
            parsed_md = markdown(file.read(), extras=['metadata'])
            # creating object to append to the array
            obj = {
                "name": path,
                "mark": parsed_md,
                "meta": parsed_md.metadata,
                "photo_strip": list_all_photos[:4]
            }
            array.append(obj)
    # return the result as an array of object for each .md file
    return array

# copy the photo in the output directory


def copy_photo_big(root, name):
    save_path_big = "./output/images/big"
    # create directory if not exists
    Path(save_path_big).mkdir(parents=True, exist_ok=True)
    # copy file
    path = os.path.join(root, name)
    copyfile(path, save_path_big + "/" + name)

# create thumbnail and copy the image in the right place


def manipulate_photo_small(root, name):
    save_path_small = "./output/images/small"
    # creating the thumbnail
    image = Image.open(root + "/" + name)
    image.thumbnail((1000, 1000))
    width, height = image.size
    print(type(height))
    if(height != 562):
        print("ciao")
        result = image.crop((0, 0, 1000, 562))
        #size (1000, 562)
        image = result

    print(image.size)
    # saving photo small
    Path(save_path_small).mkdir(parents=True, exist_ok=True)
    image.save(save_path_small + "/" + name)


# walking in the subdirecories buttom-up
for root, dirs, files in os.walk("./input/index", topdown=False):
    for name in files:
        if(name[:name.index(".")] in root):
            if("photography/" in root):
                # creating single page for photos
                print("creating photo page", root)
                array = get_list_photos(files)
                create_photo_page(root, name, array)
            elif(name not in ["books.md", "photography.md", "poems.md", "index.md", "thoughts.md"]):
                # creating signle page
                print("creating single_page", root)
                create_single_page(root, name)
            else:
                # creating index
                print("creating index", root)
                array = get_data_directory(dirs)
                create_index(root, name, array)
        else:
            # creating thumbnail big and small for every photo
            print("creating thumbnail photo:", name, "in ", root)
            # if the image does not exist create it
            if(not os.path.exists("./output/images/small/" + name) and not os.path.exists("./output/images/big/" + name)):
                #copy_photo_big(root, name)
                manipulate_photo_small(root, name)
