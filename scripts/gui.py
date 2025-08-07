import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
import webbrowser
import os
import shutil

import tree
from utils import *
import io_utils

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# CREATE WINDOW
window = tk.Tk()
window.title("Sprout")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

def on_destroy(event=None):
    """
    Deletes the __pycache__ folder.\\
    Call this when closing the program.
    """
    pycache_folder_path = os.path.join(SCRIPTS_PATH, "__pycache__").rstrip("/")
    if os.path.exists(pycache_folder_path):
        shutil.rmtree(pycache_folder_path)

window.bind("<Destroy>", on_destroy)

# DEFINE UI VARIABLES

# important
tree_style = 0
people = dict() # id -> (name, alias, surname, gender, birth_date, death_date, parent_1_id, parent_2_id, picture_path)
marriages = dict() # id -> (person_1_id, person_2_id, marriage_date)

people_ids = dict() # Name Surname (birth_date) -> id
marriages_ids = dict() # Person 1 ~ Person 2 (marriage_date) -> id

editing_person_id = None
editing_marriage_id = None

# people
selected_person_var = tk.StringVar(window)
person_name_var = tk.StringVar(window)
person_surname_var = tk.StringVar(window)
person_gender_var = tk.StringVar(window)
person_alias_var = tk.StringVar(window)
person_birth_date_var = tk.StringVar(window)
person_death_date_var = tk.StringVar(window)
person_parent_1_var = tk.StringVar(window)
person_parent_2_var = tk.StringVar(window)
person_picture_path_var = tk.StringVar(window)
# marriages
selected_marriage_var = tk.StringVar(window)
marriage_person1_var = tk.StringVar(window)
marriage_person2_var = tk.StringVar(window)
marriage_date_var = tk.StringVar(window)
# divorce_date_var = tk.StringVar(window)
# tree settings
tree_title_var = tk.StringVar(window)
tree_style_var = tk.StringVar(window)
focused_person_var = tk.StringVar(window)

# DEFINE UI FUNCTIONS

# generic ones
def toggle_button(button, enabled:bool):
    button.config(state=tk.NORMAL if enabled else tk.DISABLED)

def is_data_empty():
    return len(people) == 0 and len(marriages) == 0 and len(tree_title_var.get().strip()) == 0

def should_erase_data():
    return messagebox.askyesno("Erase Data", "Do you want to erase all the unsaved data?", icon="warning", default="no")

def erase_data():
    people.clear()
    marriages.clear()
    tree_title_var.set("")
    tree_style_var.set(STYLES.get(0))
    focused_person_var.set(NON_SELECTED_PERSON)

    reload_tree_preview()

def optional_data_erasement():
    """
    Returns True if data was erased or if there is no data to erase
    Returns False if data was not to be erased
    """

    # if there is data registered
    if not is_data_empty():
        # and the user wants to erase the data
        if should_erase_data():
            # erase data
            erase_data()
            return True
        else:
            return False
    return True

def empty_fields():
    """
    Empties all fields in the person form, marriage form and tree settings form
    """
    global editing_person_id, editing_marriage_id

    # fields
    # people
    person_selector_combobox.set(NON_SELECTED_PERSON)
    person_name_var.set("")
    person_surname_var.set("")
    person_gender_var.set(NON_SELECTED_GENDER)
    person_alias_var.set("")
    person_birth_date_var.set("")
    person_death_date_var.set("")
    parent_1_combobox.set(NON_SELECTED_PERSON)
    parent_2_combobox.set(NON_SELECTED_PERSON)
    person_picture_path_var.set("")
    # marriages
    marriage_selector_combobox.set(NON_SELECTED_MARRIAGE)
    marriage_person1_combobox.set(NON_SELECTED_PERSON)
    marriage_person2_combobox.set(NON_SELECTED_PERSON)
    marriage_date_var.set("")

    update_tree_style_id()

    # reset the editing ids
    editing_person_id = None
    editing_marriage_id = None

    # empty calendars
    # empty_birth_date_value()
    # empty_death_date_value()
    # empty_marriage_date_value()

def update_people_comboboxes():
    people_combobox_data = (NON_SELECTED_PERSON,)
    people_ids.clear()
    for person_id, person_data in people.items():
        query = get_person_query_data(person_data)
        person_to_add = (query,)
        people_combobox_data += person_to_add
        people_ids[query] = person_id

    person_selector_combobox["values"] = people_combobox_data
    parent_1_combobox["values"] = people_combobox_data
    parent_2_combobox["values"] = people_combobox_data
    marriage_person1_combobox["values"] = people_combobox_data
    marriage_person2_combobox["values"] = people_combobox_data
    focused_person_combobox["values"] = people_combobox_data

def update_marriages_comboboxes():
    marriages_combobox_data = (NON_SELECTED_MARRIAGE,)
    marriages_ids.clear()
    for marriage_id, marriage_data in marriages.items():
        query = get_marriage_query_data(marriage_data)
        marriage_to_add = (query,)
        marriages_combobox_data += marriage_to_add
        marriages_ids[query] = marriage_id

    marriage_selector_combobox["values"] = marriages_combobox_data

def reset_preview():
    preview_label.configure(text=UNAVAILABLE_PREVIEW_LABEL_TEXT)
    preview_label.config(image="")

def reload_tree_preview(event=None):
    if is_data_empty():
        reset_preview()
        return

    dot_source = tree.generate_dot_source(people, marriages, tree_title_var.get(), tree_style_id, people_ids.get(focused_person_var.get()))
    
    compile_status = tree.compile_dot(PREVIEW_PATH, dot_source, tree.FILE_PNG, False, None)

    if compile_status:
        image = tk.PhotoImage(file=PREVIEW_PATH)
        image = image.subsample(image.width() // (WINDOW_WIDTH // 2))
        preview_label.configure(text="", image=image)
    else:
        reset_preview()
    
    # delete temporary preview tree PNG
    if os.path.exists(PREVIEW_PATH):
        os.remove(PREVIEW_PATH)

# drop down menu functions
def new_tree():
    optional_data_erasement()

    update_people_comboboxes()
    update_marriages_comboboxes()
    empty_fields()

def load_tree():
    path = filedialog.askopenfilename(
        title="Open Tree Data",
        initialdir=SPROUT_PATH,
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    
    if path == None or len(path) == 0: return

    data = io_utils.load_data(path)

    # erase data if needed else return (False means don't erase data)
    if not optional_data_erasement(): return

    for person_id, person_data in data["people"].items():
        people.update({person_id : tuple(person_data)})

    for marriage_id, marriage_data in data["marriages"].items():
        marriages.update({marriage_id : tuple(marriage_data)})

    tree_settings = data["tree_settings"]
    tree_title_var.set(tree_settings["title"])
    tree_style_var.set(STYLES.get(tree_settings["style"]))
    
    focused_person_id = tree_settings["focused_person_id"]
    focused_person_data = people.get(focused_person_id)
    focused_person_query = get_person_query_data(focused_person_data)
    focused_person_var.set(focused_person_query)

    # update ui
    update_people_comboboxes()
    update_marriages_comboboxes()
    update_tree_style_id()

    reload_tree_preview()

def save_tree():
    data = {
        "people": people,
        "marriages": marriages,
        "tree_settings": {
            "title": tree_title_var.get(),
            "style": tree_style_id,
            "focused_person_id": people_ids.get(focused_person_var.get())
        }
    }

    path = filedialog.asksaveasfilename(
        title="Save Tree Data",
        initialdir=SPROUT_PATH,
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    if path != None:
        io_utils.save_data(path, data)

def export_tree():
    dot_source = tree.generate_dot_source(people, marriages, tree_title_var.get(), tree_style_id, people_ids.get(focused_person_var.get()))
    
    path = filedialog.asksaveasfilename(
        title="Export Tree",
        initialdir=SPROUT_PATH,
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )

    if path == None or len(path) == 0: return

    save_dot_source = messagebox.askyesno("Save DOT Source", "Do you want to save the DOT source?", default="no")

    dot_path = None
    if save_dot_source:
        dot_path = filedialog.asksaveasfilename(
            title="Save DOT Tree Source",
            initialdir=SPROUT_PATH,
            filetypes=[("DOT files", "*.dot"), ("All files", "*.*")]
        )
    
    # compile
    compile_status = tree.compile_dot(path, dot_source, tree.FILE_PDF, save_dot_source, dot_path)

    if compile_status:
        dot_file_message = ""
        if save_dot_source:
            dot_file_message = f"\nThe DOT tree source file can was saved at \"{dot_path}\"."
        messagebox.showinfo(title="Successfully compiled tree", message=f"The tree was successfully compiled and can be found at \"{path}\".{dot_file_message}")
    else:
        messagebox.showerror(title="Tree compilation error", message=f"An error arose when compiling the tree PDF file.\nPlease try again.")

def documentation():
    webbrowser.open("https://github.com/G3Dev-0/Sprout/blob/3f80fc5302acebfcacfe34c81f79b75f76fcbee8/README.md")

def close_app():
    window.destroy()

# show panels
def show_people_panel():
    # panels
    people_panel.pack()
    marriages_panel.pack_forget()
    tree_settings_panel.pack_forget()
    # buttons
    toggle_button(people_btn, False)
    toggle_button(marriages_btn, True)
    toggle_button(tree_settings_btn, True)

    empty_fields()

def show_marriages_panel():
    # panels
    people_panel.pack_forget()
    marriages_panel.pack()
    tree_settings_panel.pack_forget()
    # buttons
    toggle_button(people_btn, True)
    toggle_button(marriages_btn, False)
    toggle_button(tree_settings_btn, True)

    empty_fields()

def show_tree_settings_panel():
    # panels
    people_panel.pack_forget()
    marriages_panel.pack_forget()
    tree_settings_panel.pack()
    # buttons
    toggle_button(people_btn, True)
    toggle_button(marriages_btn, True)
    toggle_button(tree_settings_btn, False)

    empty_fields()

def get_person_query_data(person_data:tuple[str]) -> str:
    return get_person_query_params(person_data[0], person_data[1], person_data[2], person_data[4])

def get_person_query_params(name:str, alias:str, surname:str, birth_date:str) -> str:
    alias_str = f" \"{alias}\"" if len(alias.strip()) else ""
    return f"{name}{alias_str} {surname}" + (f" ({birth_date})" if len(birth_date.strip()) > 0 else "")

def get_marriage_query_data(marriage_data:tuple[str]) -> str:
    return get_marriage_query_params(marriage_data[0], marriage_data[1], marriage_data[2])

def get_marriage_query_params(person_1_id:str, person_2_id:str, date:str) -> str:
    person_1 = get_person_query_data(people.get(person_1_id))
    person_2 = get_person_query_data(people.get(person_2_id))
    return f"{person_1} ~ {person_2}" + (f" | ({date})" if len(date.strip()) > 0 else "")

# people form functions
def get_gender_id(person_gender_name):
    person_gender_id = GENDERS.get(NON_SELECTED_GENDER)
    for gender_id, gender_name in GENDERS.items():
        if gender_name == person_gender_name:
            person_gender_id = gender_id
            break
    return person_gender_id

def load_person_for_edit(event=None):
    global editing_person_id

    # get person
    editing_person_id = people_ids.get(selected_person_var.get())
    if editing_person_id == None:
        empty_fields()
        return

    # set widgets values
    editing_person = people.get(editing_person_id)

    person_name_var.set(editing_person[0])
    person_alias_var.set(editing_person[1])
    person_surname_var.set(editing_person[2])
    person_gender_var.set(GENDERS.get(editing_person[3])) #* gender id to gender name when loading
    person_birth_date_var.set(editing_person[4])
    person_death_date_var.set(editing_person[5])

    parent_1_person = people.get(editing_person[6])
    if (parent_1_person != None): parent_1_id = get_person_query_data(parent_1_person)
    else: parent_1_id = NON_SELECTED_PERSON
    person_parent_1_var.set(parent_1_id)
    
    parent_2_person = people.get(editing_person[7])
    if (parent_2_person != None): parent_2_id = get_person_query_data(parent_2_person)
    else: parent_2_id = NON_SELECTED_PERSON
    person_parent_2_var.set(parent_2_id)
    
    person_picture_path_var.set(editing_person[8])

def select_person_picture():
    path = filedialog.askopenfilename(
        title="Select Photo",
        initialdir=SPROUT_PATH,
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]
    )

    if path == None or len(path) == 0: return

    if not os.path.exists(path):
        messagebox.showerror(title="Image loading error", message=f"The given image (\"{path}\") doesn't exist.\nTry loading the image again.")
        return
    resized_image_path = os.path.join(RESIZED_IMAGES_PATH, path.split("/")[-1].replace(".png", "_resized.png")) # f"{path.replace('.png', '_resized.png')}"
    try:
        im = Image.open(path)
        ow = im.width
        oh = im.height
        aspect_ratio = oh / ow
        nw = IMAGE_WIDTH
        nh = int(aspect_ratio * nw)
        imr = im.resize((nw, nh), resample=Image.LANCZOS)
        imr.save(resized_image_path, "png")
    except:
        messagebox.showerror(title="Image loading error", message=f"There was an error while loading the image at \"{path}\". Try again.")
        return

    person_picture_path_var.set(resized_image_path)

# def empty_birth_date_value():
#     birth_date_cal.delete(0, 'end')

# def empty_death_date_value():
#     death_date_cal.delete(0, 'end')

def save_person():
    global editing_person_id

    # get field values
    name = person_name_var.get().strip()
    surname = person_surname_var.get().strip()

    # check for empty
    if len(name.strip()) * len(surname.strip()) == 0:
        messagebox.showinfo("Can't save this person", "A person must have at least a name and a surname")
        return

    gender = get_gender_id(person_gender_var.get()) #* gender name to gender id when saving
    alias = person_alias_var.get().strip()
    birth_date = person_birth_date_var.get()
    death_date = person_death_date_var.get()
    picture_path = person_picture_path_var.get()

    #name_alias_surname = name + (f" \"{alias}\" " if len(alias.strip()) > 0 else " ") + surname
    parent_1_id = people_ids.get(person_parent_1_var.get())
    parent_2_id = people_ids.get(person_parent_2_var.get())

    # check for having the same person as parent_1 and parent_2
    if parent_1_id == parent_2_id and parent_1_id != None:
        messagebox.showinfo("Can't save this person", "A person parent_1 and parent_2 should be two different people")
        return

    # creating a new person
    if editing_person_id == None:
        id = generate_uuid4()
    # editing a person
    else:
        id = editing_person_id

    # add person to people and to people_ids dict
    person_query = get_person_query_params(name, alias, surname, birth_date)  
    
    # check for being their own parent_1 or parent_2
    if parent_1_id == id or parent_2_id == id:
        messagebox.showinfo("Can't save this person", "A person cannot be their own parent")
        return

    # check for duplicates
    if (person_query in people_ids.keys() and editing_person_id == None):
        messagebox.showinfo("Can't save this person", "Another person with the same name and surname was found")
        return

    people.update({id : (name, alias, surname, gender, birth_date, death_date, parent_1_id, parent_2_id, picture_path)})

    # remove the marriage between two people who have been set as parents here
    if parent_1_id != None and parent_2_id != None:
        marriage_to_remove_id = None
        for marriage_id, marriage_data in marriages.items():
            marriage_people_ids = tuple(sorted((marriage_data[0], marriage_data[1])))
            current_marriage_ids = tuple(sorted((parent_1_id, parent_2_id)))
            if marriage_people_ids == current_marriage_ids:
                marriage_to_remove_id = marriage_id
                break # there is no need to check the rest of the dictionnary as you can only register one marriage with two people
        if marriage_to_remove_id != None:
            marriages.pop(marriage_to_remove_id)

    update_people_comboboxes()
    update_marriages_comboboxes()
    empty_fields()

    editing_person_id = None

    reload_tree_preview()

def remove_person():
    global editing_person_id

    if editing_person_id == None: return
    
    confirm = messagebox.askyesno(title="Remove person", message="Do you want to remove the currently selected person? This will also remove the marriages where this person appears.", icon="warning", default="no")
    if not confirm: return

    people.pop(editing_person_id)

    marriages_to_remove = list()
    for marriage_id, marriage_data in marriages.items():
        # person_1 == removed_person or person_2 == removed_person
        if marriage_data[0] == editing_person_id or marriage_data[1] == editing_person_id:
            marriages_to_remove.append(marriage_id) # schedule the remove
    
    # remove
    for marriage_id in marriages_to_remove:
        marriages.pop(marriage_id)

    update_people_comboboxes()
    empty_fields()

    editing_person_id = None

    reload_tree_preview()

# marriages form functions
def load_marriage_for_edit(event=None):
    global editing_marriage_id

    # get marriage
    editing_marriage_id = marriages_ids.get(selected_marriage_var.get())
    if editing_marriage_id == None:
        empty_fields()
        return

    # set widgets values
    editing_marriage = marriages.get(editing_marriage_id)

    marriage_person1_var.set(get_person_query_data(people.get(editing_marriage[0])))
    marriage_person2_var.set(get_person_query_data(people.get(editing_marriage[1])))
    marriage_date_var.set(editing_marriage[2])

# def empty_marriage_date_value():
#     marriage_date_cal.delete(0, 'end')

def save_marriage():
    global editing_marriage_id

    # get field values
    marriage_people = sorted([marriage_person1_var.get().strip(), marriage_person2_var.get().strip()])
    person_1 = marriage_people[0]
    person_2 = marriage_people[1]

    # get the people id as the program should work by id reference,
    # not by names, so when editing there is no need to update other
    # fields because the id stays the same
    person_1_id, person_2_id = None, None
    for p_id, p_data in people.items():
        if get_person_query_data(p_data) == person_1:
            person_1_id = p_id
        if get_person_query_data(p_data) == person_2:
            person_2_id = p_id
        
        if person_1_id != None and person_2_id != None:
            break

    # check for empty
    if person_1_id == None or person_2_id == None:
        messagebox.showinfo("Can't save this marriage", "You must input both people")
        return
    
    # check for valid marriage
    if person_1_id == person_2_id:
        messagebox.showinfo("Can't save this marriage", "A person cannot marry themselves")
        return
    
    date = marriage_date_var.get()

    old_marriage_query = None
    
    # creating a new marriage
    if editing_marriage_id == None:
        id = generate_uuid4()
    # editing a marriage
    else:
        old_data = marriages[editing_marriage_id]
        old_marriage_query = get_marriage_query_data(old_data)
        id = editing_marriage_id

    # add marriage to marriages and to marriages_ids dict
    marriage_query = get_marriage_query_params(person_1_id, person_2_id, date)
    
    # # check for duplicates
    if (marriage_query in marriages_ids.keys() and editing_marriage_id == None):
        messagebox.showinfo("Can't save this marriage", "Another marriage with the same people and date was found")
        return
        
    marriages.update({id : (person_1_id, person_2_id, date)})

    # remove the old one in case it's editing the marriage
    if old_marriage_query != None:
        marriages_ids.pop(old_marriage_query)
    # add the new one
    marriages_ids.update({marriage_query : id})

    update_marriages_comboboxes()
    empty_fields()

    editing_marriage_id = None

    reload_tree_preview()

def remove_marriage():
    global editing_marriage_id

    if editing_marriage_id == None: return
    
    confirm = messagebox.askyesno(title="Remove marriage", message="Do you want to remove the currently selected marriage?", icon="warning", default="no")
    if not confirm: return

    marriages.pop(editing_marriage_id)

    update_marriages_comboboxes()
    empty_fields()

    editing_marriage_id = None

    reload_tree_preview()

def update_tree_style_id(event=None):
    global tree_style_id
    
    tree_style_id = None
    for style_id, style_name in STYLES.items():
        if style_name == tree_style_var.get():
            tree_style_id = style_id
            
            reload_tree_preview()
            
            return

# CREATE UI
# define the tooltip class
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.id = None
        self.waittime = 500  # milliseconds (0.5 seconds)
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id_to_cancel = self.id
        self.id = None
        if id_to_cancel:
            self.widget.after_cancel(id_to_cancel)

    def showtip(self, event=None):
        "Display text in tooltip window"
        if self.tooltip_window or not self.text:
            return

        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + self.widget.winfo_height() + 2

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Remove window decorations
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        "Hide the tooltip window"
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

# menus: new tree, load tree, save tree | export tree | close
menubar = tk.Menu(window)
window.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New Tree", command=new_tree)
file_menu.add_command(label="Load Tree", command=load_tree)
file_menu.add_command(label="Save Tree", command=save_tree)
file_menu.add_separator()
file_menu.add_command(label="Export Tree", command=export_tree)
file_menu.add_separator()
file_menu.add_command(label="Documentation", command=documentation)
file_menu.add_separator()
file_menu.add_command(label="Close", command=close_app)

# views: editing | preview

# main content pane
content_pane = ttk.PanedWindow(window, orient=tk.HORIZONTAL)
content_pane.pack(expand=True, fill="both", padx=10, pady=10)

# editing view
editing_view = tk.Frame(content_pane, bg="lightblue", bd=2, relief="sunken")
content_pane.add(editing_view, weight=1)

# preview view
preview_view = tk.Frame(content_pane, bg="lightgreen", bd=2, relief="sunken")
content_pane.add(preview_view, weight=1)

preview_label = tk.Label(preview_view, text=UNAVAILABLE_PREVIEW_LABEL_TEXT, bg="lightgreen", font=("Arial", 12))
preview_label.pack(expand=True, pady=20)

credits_label = tk.Label(preview_view, text="Made by G3Dev", bg="lightgreen", font=("Arial", 8))
credits_label.pack(side=tk.BOTTOM, anchor=tk.E, padx=10, pady=10)

# panels: people | marriages | tree settings

# Frame for buttons inside editing_panel
editing_view_buttons_frame = tk.Frame(editing_view, bg="lightblue")
editing_view_buttons_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

# Add People Button
people_btn = tk.Button(editing_view_buttons_frame, text="People", command=show_people_panel)
people_btn.pack(side=tk.LEFT, padx=5, pady=5)

# Add Marriages Button
marriages_btn = tk.Button(editing_view_buttons_frame, text="Marriages", command=show_marriages_panel)
marriages_btn.pack(side=tk.LEFT, padx=5, pady=5)

# Add Tree Settings Button
tree_settings_btn = tk.Button(editing_view_buttons_frame, text="Tree Settings", command=show_tree_settings_panel)
tree_settings_btn.pack(side=tk.LEFT, padx=5, pady=5)

## People Form
# --- Add/Edit Person Panel ---
people_panel = tk.Frame(editing_view, bg="lightgray", bd=2, relief="groove")

# Person Selector Combobox
person_selector_combobox = ttk.Combobox(people_panel, textvariable=selected_person_var, state="readonly")
person_selector_combobox.pack(pady=5, padx=10, fill=tk.X)
person_selector_combobox.bind("<<ComboboxSelected>>", load_person_for_edit)

# Frame to hold all the input fields for better organization with grid
person_form_frame = tk.Frame(people_panel, bg="lightgray")
person_form_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Labels configuration for grid
label_font = ("Arial", 10)
entry_width = 30 # A reasonable width for entry fields

# Row 0: Name
tk.Label(person_form_frame, text="Name:", bg="lightgray", font=label_font).grid(row=0, column=0, sticky="w", pady=2, padx=5)
tk.Entry(person_form_frame, textvariable=person_name_var, width=entry_width).grid(row=0, column=1, sticky="ew", pady=2, padx=5)

# Row 1: Surname
tk.Label(person_form_frame, text="Surname:", bg="lightgray", font=label_font).grid(row=1, column=0, sticky="w", pady=2, padx=5)
tk.Entry(person_form_frame, textvariable=person_surname_var, width=entry_width).grid(row=1, column=1, sticky="ew", pady=2, padx=5)

# New: Row 2: Gender
tk.Label(person_form_frame, text="Gender:", bg="lightgray", font=label_font).grid(row=2, column=0, sticky="w", pady=2, padx=5)
gender_combobox = ttk.Combobox(person_form_frame, textvariable=person_gender_var, state="readonly", width=entry_width)
gender_combobox['values'] = tuple(GENDERS.values())
gender_combobox.grid(row=2, column=1, sticky="ew", pady=2, padx=5)

# Row 3: Alias
tk.Label(person_form_frame, text="Alias:", bg="lightgray", font=label_font).grid(row=3, column=0, sticky="w", pady=2, padx=5)
tk.Entry(person_form_frame, textvariable=person_alias_var, width=entry_width).grid(row=3, column=1, sticky="ew", pady=2, padx=5)

# Row 4: Birth Date
tk.Label(person_form_frame, text="Birth Date:", bg="lightgray", font=label_font).grid(row=4, column=0, sticky="w", pady=2, padx=5)
# birth_date_cal = DateEntry(person_form_frame, selectmode='day', textvariable=person_birth_date_var,
#                                 initialdate=None,
#                                 background='darkblue', foreground='white', borderwidth=2, width=entry_width)
# birth_date_cal.grid(row=4, column=1, sticky="ew", pady=2, padx=5)
tk.Entry(person_form_frame, textvariable=person_birth_date_var, width=entry_width).grid(row=4, column=1, sticky="ew", pady=2, padx=5)

# empty calendar date
# tk.Button(person_form_frame, text="Reset", command=empty_birth_date_value).grid(row=4, column=2, sticky="ew", pady=2, padx=5)

# Row 5: Death Date
tk.Label(person_form_frame, text="Death Date:", bg="lightgray", font=label_font).grid(row=5, column=0, sticky="w", pady=2, padx=5)
# death_date_cal = DateEntry(person_form_frame, selectmode='day', textvariable=person_death_date_var,
#                                 initialdate=None,
#                                 background='darkblue', foreground='white', borderwidth=2, width=entry_width)
# death_date_cal.grid(row=5, column=1, sticky="ew", pady=2, padx=5)
tk.Entry(person_form_frame, textvariable=person_death_date_var, width=entry_width).grid(row=5, column=1, sticky="ew", pady=2, padx=5)

# empty calendar date
# tk.Button(person_form_frame, text="Reset", command=empty_death_date_value).grid(row=5, column=2, sticky="ew", pady=2, padx=5)

# Row 6: Parent 1
tk.Label(person_form_frame, text="Parent 1:", bg="lightgray", font=label_font).grid(row=6, column=0, sticky="w", pady=2, padx=5)
parent_1_combobox = ttk.Combobox(person_form_frame, textvariable=person_parent_1_var, state="readonly", width=entry_width)
parent_1_combobox.grid(row=6, column=1, sticky="ew", pady=2, padx=5)

# Row 7: Parent 2
tk.Label(person_form_frame, text="Parent 2:", bg="lightgray", font=label_font).grid(row=7, column=0, sticky="w", pady=2, padx=5)
parent_2_combobox = ttk.Combobox(person_form_frame, textvariable=person_parent_2_var, state="readonly", width=entry_width)
parent_2_combobox.grid(row=7, column=1, sticky="ew", pady=2, padx=5)

# Row 8: picture
tk.Label(person_form_frame, text="Picture:", bg="lightgray", font=label_font).grid(row=8, column=0, sticky="w", pady=2, padx=5)
picture_frame = tk.Frame(person_form_frame, bg="lightgray")
picture_frame.grid(row=8, column=1, sticky="ew", pady=2, padx=5)
tk.Entry(picture_frame, textvariable=person_picture_path_var, state="readonly", width=entry_width - 8).pack(side=tk.LEFT, fill=tk.X, expand=True)
tk.Button(picture_frame, text="Browse...", command=select_person_picture).pack(side=tk.RIGHT, padx=(5,0))

# Configure column 1 to expand with the window
person_form_frame.grid_columnconfigure(1, weight=1)

# Save/Remove Person Button at the bottom
tk.Button(people_panel, text="Save Person", command=save_person).pack(side=tk.RIGHT, padx=5, pady=10)
tk.Button(people_panel, text="Remove Person", command=remove_person).pack(side=tk.LEFT, padx=5, pady=10)

# --- Add/Edit Marriage Panel ---
marriages_panel = tk.Frame(editing_view, bg="lightyellow", bd=2, relief="groove")

# Marriage Selector Combobox
marriage_selector_combobox = ttk.Combobox(marriages_panel, textvariable=selected_marriage_var, state="readonly")
marriage_selector_combobox.pack(pady=5, padx=10, fill=tk.X)
marriage_selector_combobox.bind("<<ComboboxSelected>>", load_marriage_for_edit)

# Frame to hold input fields for marriage
marriage_form_frame = tk.Frame(marriages_panel, bg="lightyellow")
marriage_form_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Row 0: Person 1
tk.Label(marriage_form_frame, text="Person 1:", bg="lightyellow", font=label_font).grid(row=0, column=0, sticky="w", pady=2, padx=5)
marriage_person1_combobox = ttk.Combobox(marriage_form_frame, textvariable=marriage_person1_var, state="readonly", width=entry_width)
marriage_person1_combobox.grid(row=0, column=1, sticky="ew", pady=2, padx=5)

# Row 1: Person 2
tk.Label(marriage_form_frame, text="Person 2:", bg="lightyellow", font=label_font).grid(row=1, column=0, sticky="w", pady=2, padx=5)
marriage_person2_combobox = ttk.Combobox(marriage_form_frame, textvariable=marriage_person2_var, state="readonly", width=entry_width)
marriage_person2_combobox.grid(row=1, column=1, sticky="ew", pady=2, padx=5)

# Row 2: Marriage Date
tk.Label(marriage_form_frame, text="Marriage Date:", bg="lightyellow", font=label_font).grid(row=2, column=0, sticky="w", pady=2, padx=5)
# marriage_date_cal = DateEntry(marriage_form_frame, selectmode='day', textvariable=marriage_date_var,
#                                 initialdate=None,
#                                 background='darkblue', foreground='white', borderwidth=2, width=entry_width)
# marriage_date_cal.grid(row=2, column=1, sticky="ew", pady=2, padx=5)
tk.Entry(marriage_form_frame, textvariable=marriage_date_var, width=entry_width).grid(row=2, column=1, sticky="ew", pady=2, padx=5)

# empty calendar date
# tk.Button(marriage_form_frame, text="Reset", command=empty_marriage_date_value).grid(row=2, column=2, sticky="ew", pady=2, padx=5)

# Row 3: Divorce Date
# tk.Label(marriage_form_frame, text="Divorce Date:", bg="lightyellow", font=label_font).grid(row=3, column=0, sticky="w", pady=2, padx=5)
# divorce_date_cal = DateEntry(marriage_form_frame, selectmode='day', textvariable=divorce_date_var,
#                                 initialdate=None,
#                                 background='darkblue', foreground='white', borderwidth=2, width=entry_width)
# divorce_date_cal.grid(row=3, column=1, sticky="ew", pady=2, padx=5)

# Configure column 1 to expand with the window
marriage_form_frame.grid_columnconfigure(1, weight=1)

# Save/Remove Marriage Button at the bottom
tk.Button(marriages_panel, text="Save Marriage", command=save_marriage).pack(side=tk.RIGHT, padx=5, pady=10)
tk.Button(marriages_panel, text="Remove Marriage", command=remove_marriage).pack(side=tk.LEFT, padx=5, pady=10)

# --- Tree Settings Panel (New) ---
tree_settings_panel = tk.Frame(editing_view, bg="lightcyan", bd=2, relief="groove")

settings_form_frame = tk.Frame(tree_settings_panel, bg="lightcyan")
settings_form_frame.pack(padx=10, pady=10, fill="both", expand=True)

tk.Label(settings_form_frame, text="Tree Title:", bg="lightcyan", font=label_font).grid(row=0, column=0, sticky="w", pady=5, padx=5)
tree_title_entry = tk.Entry(settings_form_frame, textvariable=tree_title_var, width=entry_width)
tree_title_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
tree_title_entry.bind("<Leave>", reload_tree_preview)

tk.Label(settings_form_frame, text="Tree Style:", bg="lightcyan", font=label_font).grid(row=1, column=0, sticky="w", pady=5, padx=5)
tree_style_combobox = ttk.Combobox(settings_form_frame, textvariable=tree_style_var, state="readonly", width=entry_width)
tree_style_combobox['values'] = tuple(STYLES.values())
tree_style_combobox.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
tree_style_combobox.bind("<<ComboboxSelected>>", update_tree_style_id)

tk.Label(settings_form_frame, text="Focused person:", bg="lightcyan", font=label_font).grid(row=2, column=0, sticky="w", pady=5, padx=5)
focused_person_combobox = ttk.Combobox(settings_form_frame, textvariable=focused_person_var, state="readonly", width=entry_width)
focused_person_combobox.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
focused_person_combobox.bind("<<ComboboxSelected>>", reload_tree_preview)

settings_form_frame.grid_columnconfigure(1, weight=1)

# set tooltip and placeholder texts
ToolTip(marriages_btn, "Used for couples with no offspring")

# prepare widgets values for app opening
erase_data()
update_people_comboboxes()
update_marriages_comboboxes()
empty_fields()

# START APPLICATION
window.mainloop()
