import os

# manual configuration
WORK_DIRECTORY = ""
FILE_WITH_ITEMS = "words_input.txt"  # file with searched words are in the current WORK_DIRECTORY
LOG_FILE = os.path.join(WORK_DIRECTORY, "log.txt")
FILE_TYPES = [".html", ".htm"]

# auto configuration
with open(os.path.join(WORK_DIRECTORY, FILE_WITH_ITEMS), encoding='utf-8') as f:
    ITEMS_TO_FIND = f.readlines()
ITEMS_DICT = {x.strip(): [] for x in ITEMS_TO_FIND}


# recursive directory search
def search_dir(up_list: list, current_dir: str):
    for item in up_list:  # take item from directory
        check_path = os.path.join(current_dir, item)
        if os.path.isfile(check_path) and \
                any(check_path.endswith(typ) for typ in FILE_TYPES):  # check type oof item & file
            full_path = os.path.join(current_dir, item)
            with open(full_path) as file:  # open file to search
                content = file.readlines()
                content = " ".join(content).lower()
                for item_to_find in ITEMS_TO_FIND:  # search for all items and add to dict
                    item_to_find = item_to_find.strip()
                    item_to_add = current_dir.split('\\')[-1] + ": " + item  # getting file name
                    # add item if is in content and not in dict yet
                    if item_to_find.lower() in content and item_to_add not in ITEMS_DICT[item_to_find]:
                        ITEMS_DICT[item_to_find].append(item_to_add)
        elif os.path.isdir(check_path):  # it file type is dir call yourself
            new_path = os.path.join(current_dir, item)
            search_dir(os.listdir(new_path), new_path)
    return


# initialization of the main directory with files and FILE_WITH_ITEMS
items = os.listdir(WORK_DIRECTORY)
search_dir(items, WORK_DIRECTORY)

# printing result from dict to console and log file
with open(LOG_FILE, "w",  encoding='utf-8') as file_dict:
    for key, value in ITEMS_DICT.items():
        print(f"{key}:")
        file_dict.write(f"{key}:\n")
        if not value:
            print(f"\tBRAK..................")
            file_dict.write(f"\tBRAK..................\n")
        else:
            for val in value:
                print(f"\t{val}")
                file_dict.write(f"\t{val}\n")
