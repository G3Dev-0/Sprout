# Sprout

A tool for visualising family trees.

## Table of contents
+ [How to use Sprout](#how-to-use-sprout)
+ [Editing the tree](#editing-the-tree)
    + [People](#people)
    + [Marriages](#marriages)
    + [Tree settings](#tree-settings)
+ [Saving and loading the tree in the Sprout app](#saving-and-loading-the-tree-in-the-sprout-app)
+ [Exporting your tree](#exporting-your-tree)
+ [Used technologies](#used-technologies)
+ [About](#about)

## How to use Sprout [#](#table-of-contents)
When opening the app you find yourself in front of two views: the tree **editing view** (light blue) and the tree **preview view** (light green).

### Editing the tree [#](#table-of-contents)
The editing view has three buttons named "People", "Marriages" and "Tree settings".\
Each of them shows a form where you can input information and save them.

#### People [#](#table-of-contents)
This form can be filled to add a person. You can input their name, surname, gender, birth date, death date and parents name.\
If you want you can also type an alias for that person and specify a path to a picture of them.

#### Marriages [#](#table-of-contents)
Marriages should only be used for couples who have no children.

That's because Sprout automatically figures out the families from people's parents, which means that without the marriage option, a couple with no children couldn't be taken into account for the tree.

If you first register a marriage and later add a children for that couple, the marriage will automatically be removed.

#### Tree settings [#](#table-of-contents)
In this form you can specify a title for the tree (optional), a style and a person to focus on (optional).

### Saving and loading the tree in the Sprout app [#](#table-of-contents)
You can save the tree data in the form of a JSON file and load it back in the Sprout app later.\
Just go in the `File` menu, then click `Save tree` or `Load tree`.

### Exporting your tree [#](#table-of-contents)
Once your family tree is ready, you can export it as a PDF file by choosing `File > Export tree` in the dropdown menu.

## Used technologies [#](#table-of-contents)
- **Python**\
Programming language\
Version: *3.13.5*\
Home page: https://www.python.org/

- **pydot**\
Python interface to Graphviz's Dot\
Version: *4.0.1*\
Home page: https://github.com/pydot/pydot

- **tkinter**\
Cross-platform graphical user interface toolkit\
Version: *8.6.15*\
Home page: https://docs.python.org/3/library/tkinter.html

## About [#](#table-of-contents)
Made by G3Dev\
v2.0 b06082025-0
