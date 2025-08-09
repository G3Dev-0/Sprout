from uuid import uuid4
import os
import base64

# constants
"""
folder structure
main
    scripts (SCRIPTS_PATH)
        __pycache__
        gui.py
        io_utils.py
        tree.py
        utils.py
    sprout (SPROUT_PATH)
        images (IMAGES_PATH)
            resized (RESIZED_IMAGES_PATH)
        unknown.png (UNKNOWN_IMAGE_PATH)
    run.bat
    run.sh
"""

SCRIPTS_PATH = os.getcwd() # os.path.dirname(os.path.realpath(__file__)) # os.getcwd()

SPROUT_PATH = os.path.join(SCRIPTS_PATH, "sprout")

IMAGES_PATH = os.path.join(SPROUT_PATH, "images")

PREVIEW_PATH = os.path.join(IMAGES_PATH, "tmp.png") # used to set the tree preview label image, then it gets deleted as it gets stored in the label
RESIZED_IMAGES_PATH = os.path.join(IMAGES_PATH, "resized") # here are stored the resized images for the tree, they MUST stay there, otherwise the reference in the dot file doesn't work

UNKNOWN_IMAGE_PATH = os.path.join(IMAGES_PATH, "unknown.png") # used as a placeholder for nodes with wrong image path

# generate folders if they don't exist
if not os.path.exists(IMAGES_PATH): os.makedirs(RESIZED_IMAGES_PATH) # resized images folder

# encode image data to base64
# def image_to_base64(image_path:str) -> str:
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# decode image data from base64
def base64_to_image(base64_data, output_image_path):
    image_data = base64.b64decode(base64_data)
    with open(output_image_path, "wb") as file:
        file.write(image_data)

# obtained with image_to_base64(image_path:str)
unknown_image_data_base64 = "iVBORw0KGgoAAAANSUhEUgAAAJkAAAC6CAYAAAC9ZO8iAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAToSURBVHhe7dvbbtswEEVRp///z46ZhIUg0DIl8ZBz2Qsw2ofGicntoeQiX4/H4/l6ADL//v4EZP5PsueTgYaxvr5KXkwyTEBkkCMyyBEZ5IgMckQGOSKDHJFBjsggR2SQIzLIERnkiAxyRAY5IoMckUGOyCBHZJAjMsgRGeSIDHJEBjkigxy/dzlI/R3DlqxrW9eEyC44CuqdjOvLL/dedCWwonxdfWRDZJ1GBpItNCLroIiiRpshOCL7YEYE0UMrr44L/42VGx5tD+paMsn+lAVZPVGiTjQie7G0uRFDIzLIpY7MwhHZEm2apY3M+kZGCo3j0rAooaWMLNpxZB2TzLgIb4jyCtJ9GKvauJ41vPO9ve1Rfa2pIhsd19U1u/pzeI0szXE5MrCy2Xc2/OrXj36TzMI1Wacaxp249kY/n1UpIrszAWaEcOb5PU6z8JHdDcwib6FxXL5xN7ASQn30sBr0CETWcGXDt1Htw+oN7QzFc6oQ2U2tqFp6/l3UaUZkG2WTeza6BtMT117G0EJHdiaCM3Gp9YY242cZgUm2QE8ckUILG9noxbf+fJYxyV4+TQ1VEFlCI7IP1CEcPX+UmwAiC8D6RCSyA1mOMzUiMyB6zCEji7RpEa7LwkXGEWcPx2UA1qcdkR2I8hHCakQWAB9hOMc0u4/IXiLcLFh+DUTWQT3Njp4/whuAyP582kyOzeuIbLEM8YaL7M6mzZ5mn57v7FFp9Whlku3M2qhMxy+RLdAT2JXYrYZLZA3KaaYKzDIie6O10TM2P1pgBZEdKBu+fdw1+kLfCyKbJGtgBZFNYPWCfBYiEypxzbrQtxwykYn0bnrkY7IiMoHZgVmeYgWRDdZ7PGaYYFXIyCy/szPFVYWdZBZDUwRm/agsOC4nyRpYETqy2ZvgZdNnY5I55Sno8JExXdZjkg1yFHPGO8otInOmxOxtOhMZ5IhMLPtRWRCZI15vYogMckQGOSJzwvPnfUQGuRSReZ4Clee7VCYZ5IhskNak4TOyX0Q2UIlq+8CvNJFxXbYOk8wZj1MyVWRlmkWYaIWn2JhkznkILV1k3o6aHnWqWX1tqSKLGNiexdfIcRmQtdCILChLx2eayDIclS0WYivf/eeePsqt/d7MBd6vocWwZ+5zff1hJ9nsd3Br8yy+cVeEHzIyixPEkvoGnLVOoSKbuXBRzFizEJER133K9Utzd6nW2iRv4at+3vKsP1enHu8umV4ao1qo++N2khGYzui15bhEUwltVGwuI2OKzTNird1FRmD+uIqMwNa4u+7lq83eXRKVLWcbqftndpIRmD1lT67si7nIrr4QzHN2j0xFRly+9O6XicjOvjPgy/LIiMu3nv1bGhmBxfBpH81d+CMeIsMQR9NsWWQclfG821MmGYZqhUZkGG4f2pLIOCrj2+4xkwxyRAa56ZFxVObDJIMckUFuamQclTkxySBHZJAjMsgRGeSIDHJEBjkigxyRQY7IIEdkkCMyyBEZ5KZFxn+O58UkgxyRQW5KZByVuTHJIEdkkJNHxlEJJhnkiAxyRAY5IoOcNDIu+lEwySBHZJCTRcZRiYpJBjkigxyRQY7IIEdkkCMyyBEZ5CSR8RkZtphkkBseGVMMe0wyyA2NjCmGFiYZ5IgMckQGOSKD3LDIuOjHO6WM5+9fAQ2OS4g9Ht+kcxjBxmFPcgAAAABJRU5ErkJggg=="
base64_to_image(unknown_image_data_base64, UNKNOWN_IMAGE_PATH)

UNAVAILABLE_PREVIEW_LABEL_TEXT = "Preview is not available..."

# STYLE_SQUARES = 0
STYLE_CURVES = 0
STYLE_STRAIGHT = 1
STYLE_ROUNDED = 2
STYLES = {
    # STYLE_SQUARES: "Squares", # square nodes, ortho edges
    STYLE_CURVES: "Curves", # square nodes, curved edges
    STYLE_STRAIGHT: "Straight Edges", # rounded nodes, straight edges
    STYLE_ROUNDED: "Rounded" # rounded nodes, curved edges
}

NON_SELECTED_PERSON = "Select a person"
NON_SELECTED_MARRIAGE = "Select a marriage"
NON_SELECTED_GENDER = "Not given"

GENDER_MALE = 0
GENDER_FEMALE = 1
GENDER_UNKNOWN = 2
GENDERS = {
    GENDER_MALE : "Male",
    GENDER_FEMALE : "Female",
    GENDER_UNKNOWN : NON_SELECTED_GENDER
}

STAR_SYMBOL = "&#42;"
CROSS_SYMBOL = "&#8224;"

IMAGE_WIDTH = 200

def generate_uuid4():
    return f"\"{str(uuid4()).replace("-", "_")}\""