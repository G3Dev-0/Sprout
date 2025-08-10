# Sprout

A tool for visualising family trees.\
You can run Sprout on Unix systems with the `run.sh` file and on Windows by using `run.bat`.\
The app was also built for Linux and can be used by running `Sprout_Linux`.

Known bugs:
- Editing a person, doesn't update the focused person combobox
- When exporting a tree, if you only save the pdf and not the dot file too, the preview is reset and you have to update it to make it show up again

## Table of contents
+ [How to use Sprout](#how-to-use-sprout)
+ [Editing the tree](#editing-the-tree)
    + [People](#people)
    + [Marriages](#marriages)
    + [Tree Settings](#tree-settings)
+ [Saving and loading the tree in the Sprout app](#saving-and-loading-the-tree-in-the-sprout-app)
+ [Exporting your tree](#exporting-your-tree)
+ [Used technologies](#used-technologies)
+ [About](#about)

## How to use Sprout [#](#table-of-contents)
When opening the app you find yourself in front of two views: the tree **editing view** (light blue) and the tree **preview view** (light green).

### Editing the tree [#](#table-of-contents)
The editing view has three buttons named "People", "Marriages" and "Tree Settings".\
Each of them shows a form where you can input information and save them.

#### People [#](#table-of-contents)
This form can be filled to add a person. You can input their name, surname, gender, birth date, death date and parents name.\
If you want you can also type an alias for that person and specify a path to a picture of them.

#### Marriages [#](#table-of-contents)
Marriages should only be used for couples who have no children.

That's because Sprout automatically figures out the families from people's parents, which means that without the marriage option, a couple with no children couldn't be taken into account for the tree.

If you first register a marriage and later add a children for that couple, the marriage will automatically be removed.

#### Tree Settings [#](#table-of-contents)
In this form you can specify a title for the tree (optional), a style and a person to focus on (optional).

### Saving and loading the tree in the Sprout app [#](#table-of-contents)
You can save the tree data in the form of a JSON file and load it back in the Sprout app later.\
Just go in the `File` menu, then click `Save Tree` or `Load Tree`.

### Exporting your tree [#](#table-of-contents)
Once your family tree is ready, you can export it as a PDF file by choosing `File > Export Tree` in the dropdown menu.

## Used technologies [#](#table-of-contents)
- **Python**\
Programming language\
Version: *3.13.5*\
Home page: https://www.python.org/

- **tkinter**\
Cross-platform graphical user interface toolkit\
Version: *8.6.15*\
Home page: https://docs.python.org/3/library/tkinter.html

- **pydot**\
Python interface to Graphviz's Dot\
Version: *4.0.1*\
Home page: https://github.com/pydot/pydot

- **pillow**\
Python Imaging Library (Fork)\
Version: *11.3.0*\
Home page: https://python-pillow.github.io

## About [#](#table-of-contents)
Made by G3Dev\
v2.0 b10082025-0
