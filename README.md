# Sprout
Sprout is a tool you can use to speed up the process of organizing and creating a family tree.

---

**Table of Contents**
+ [Sprout](#sprout)
	+ [HOW TO USE IT](#how-to-use-it)
		+ [Add Edit  Remove](#add-edit--remove)
		+ [Show](#show)
		+ [Main person](#main-person)
		+ [Save  Load](#save--load)
		+ [Create Tree](#create-tree)
		+ [Clear](#clear)
		+ [Help](#help)
		+ [Quit](#quit)
	+ [WHO MADE IT](#who-made-it)
	+ [ABOUT](#about)
		+ [Attributions](#attributions)
		+ [Used Technologies](#used-technologies)
		+ [Version History](#version-history)

## HOW TO USE IT?
To use Sprout you have to choose an option to use. To select the option you can either type the full option name or the option name in its short form (Given between the square brackets in the option list).
Here is a table showing all the option names, short forms and description.

OPTION NAME|SHORT FORM|DESCRIPTION
-|-|-
[add data](#add-edit--remove)|a|lets you add a person or a marriage
[edit data](#add-edit--remove)|e|lets you edit a person or a marriage
[remove data](#add-edit--remove)|r|lets you edit a person or a marriage
[show people](#show)|p|shows you the list of registered people
[show marriages](#show)|m|shows you the list of registered marriages
[main person](#main-person)|g|lets you set the main person in the tree
[show data](#show)|d|shows you the full data set
[create tree](#create-tree)|c|lets you create the tree either from a file or from the data the program currently holds.
[save data](#save--load)|s|saves the current data to a `.sprout` file
[load data](#save--load)|l|loads data from a `.sprout` file
[clear data](#clear)|t|erases all the data the program currently holds after asking for user confirm
[help](#help)|h|shows either general help information or option specific help information
[quit](#quit)|q|closes the program after asking for user confirm (this does NOT automatically save data)

### Add, Edit & Remove
In order to make a family tree you need to first add the people to the database by using the `add data`>`p` option. You can always edit a field value (with the `edit data`>`p` option) or remove a person later (with the `remove data`>`p` option).
You can also add, edit and remove a marriage by using `add data`>`m`, `edit data`>`m`, `remove data`>`m` respectively.

_**Note:** In the tree, everything after `*` in the name and surname of a person won't be shown. This can be used to distinct people with the same name._

_**Note:** You should use marriages only to register a couple which doesn't have children._
### Show
Use the `show people`, `show marriages` and `show data` options to see the listed names, marriages and full database respectively.
### Main person
To set the main person use the `main person` option. This person will have a unique color in the tree graph. To set the main person to be no one, just set the main person to be `-1`.
### Save & Load
To save the current database you can use the `save` option, while the `load` option loads a database from a file.

_**Note:** the file must be inside the folder named `data` that the program will create at its first launch._
### Create Tree
Create the family tree by using the `create tree` option.
You'll need to specify the tree title and file name.
You'll find the tree as a `PDF` file inside of the `trees` folder that will be created by the program at the first runtime.

_**Note:** creating the tree won't save the current database. So always make sure you save your data before closing the program._
### Clear
You can rapidly erase all the data that the program is currently holding by using the `clear` option.
### Help
Finally, if you need help you can use the `help` option which will display helpful information about all the commands.
You can also use `help [OPTION]` which tells you everything you need to know about OPTION.
### Quit
Use the `quit` option to quit the program.

## WHO MADE IT?
Me, of course, G3Dev!
I made it in a week of March 2024.

## ABOUT

### Attributions
App icon: <a href="https://www.flaticon.com/free-icons/sprout" title="sprout icons">Sprout icons created by Umeicon - Flaticon</a>
	
### Used Technologies
+ Python 3.8 (www.python.org)
+ Graphviz (https://graphviz.org/)

### Version History
**CURRENT VERSION:** `v1.4 b05092024` (Official Release)

**OLDER VERSIONS:**
- `v1.0 b01042024` (Menu, tree graph creation and data organization implemented)
- `v1.1 b11042024` (Marriages implemented)
- `v1.2 b11052024` (Portraits)
- `v1.3 b19052024` (Tree graph visual improvements)

If you show this tool to a community, please make sure to give credits!
Thanks for using this tool, you're and amazing person! :D
