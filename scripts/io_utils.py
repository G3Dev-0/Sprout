import json

# contains all saving and loading functions

# data = {
#     "people": people,
#     "marriages": marriages,
#     "tree_settings": tree_settings
# }
def save_data(path:str, data:dict):
    """
    Saves the data to a json file.\
    
    Expects:
    data = {
        "people": people,
        "marriages": marriages,
        "tree_settings": tree_settings
    }
    """
    output = json.dumps(data, indent=4)
    with open(path, "w") as f:
        f.write(output)

def load_data(path:str):
    """
    Loads the data from a json file.\
    
    Expects:
    data = {
        "people": people,
        "marriages": marriages,
        "tree_settings": tree_settings
    }
    """
    with open(path, "r") as f:
        lines = f.readlines()
    return json.loads("".join(lines))