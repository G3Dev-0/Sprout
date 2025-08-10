from random import randint
from utils import *

import pydot

# gender based coloring
MALE_COLOR_STYLE = "color=\"blue\"\n\t\tfillcolor=\"lightblue\""
FEMALE_COLOR_STYLE = "color=\"red\"\n\t\tfillcolor=\"pink\""
UNKNOWN_COLOR_STYLE = "color=\"black\"\n\t\tfillcolor=\"darkgrey\""
FOCUSED_COLOR_STYLE = "color=\"orange\"\n\t\tfillcolor=\"gold\""

COLORS = ["#619E1C", "#297F23", "#ED8F31", "#EF6502", "#A85426", "#207EBC", "#653A92", "#827DC6", "#D7191B", "#DB2783", "#FFC423", "#9E701C", "#1A9671", "#616161", "#00BABA"]
def random_color():
    return COLORS[randint(0, len(COLORS) - 1)]

def get_person_node_style(person_id:str, person_data:list, focused:bool):
    person_data = list(person_data)
    if len(person_data[1]) > 0: person_data[1] = f"\\\"{person_data[1]}\\\""
    
    birth_date = person_data[4]
    death_date = person_data[5]
    
    name_alias_surname = "\"" + " ".join(person_data[:3])
    name_alias_surname = name_alias_surname.replace("  ", " ") # remove the double space caused by the absence of an alias
    if len(birth_date.strip()) > 0:
        separator = " " if len(death_date.strip()) > 0 else ""
        name_alias_surname += f"\n*{birth_date}{separator}"
    if len(death_date.strip()) > 0:
        name_alias_surname += f"+{death_date}"
    name_alias_surname += "\""

    gender = person_data[3]
    image_path = person_data[8]
    
    node_style = f"{person_id} ["
    # set label
    node_style += f"\n\t\tlabel={name_alias_surname}"
    # set color
    if focused:
        node_style += f"\n\t\t{FOCUSED_COLOR_STYLE}"
    elif gender == GENDER_MALE:
        node_style += f"\n\t\t{MALE_COLOR_STYLE}"
    elif gender == GENDER_FEMALE:
        node_style += f"\n\t\t{FEMALE_COLOR_STYLE}"
    elif gender == GENDER_UNKNOWN:
        node_style += f"\n\t\t{UNKNOWN_COLOR_STYLE}"
    # set image
    if len(image_path.strip()) > 0:
        # replace non existing image paths with a default picture-not-found image 
        if not os.path.exists(image_path): image_path = UNKNOWN_IMAGE_PATH
        node_style += f"\n\t\timage=\"{image_path}\""

        node_style += "\n\t\tfixedsize=\"true\""
        node_style += "\n\t\twidth=\"3.8\""
        node_style += "\n\t\theight=\"5.5\""
        node_style += "\n\t\timagepos=\"mc\""
        node_style += "\n\t\tlabelloc=\"b\""

    node_style += "\n\t]"

    return node_style

def get_connector_node_style(connector_id:str, color:str):
    connector_style = f"{connector_id} ["
    connector_style += "\n\t\tlabel=\"\""
    connector_style += f"\n\t\tcolor=\"{color}\""
    connector_style += f"\n\t\tfillcolor=\"{color}\""
    connector_style += f"\n\t\twidth=0.1"
    connector_style += f"\n\t\theight=0.1"
    connector_style += "\n\t]"

    return connector_style

def get_or_generate_family_uuid(families:dict, parents_ids:tuple):
    # always assume that siblings with both None parents come from different families
    if parents_ids[0] == parents_ids[1] == None:
        return generate_uuid4()
    
    for family_id, family_data in families.items():
        if family_data[0] == parents_ids:
            return family_id
    return generate_uuid4()

def generate_dot_source(people:dict, marriages:dict, tree_title:str, tree_style:int, focused_person_id:str|None):
    # parse data to have a family structure where you have a list of couples (parents) associated with a tuple of siblings
    families = dict() # family_uuid (used for connectors) : [(parents), (siblings)]

    for person_id, person_data in people.items():
        parents_ids = (person_data[6], person_data[7])

        # sort them based on their UUID 4 to have the same couple every time
        if parents_ids[0] != None and parents_ids[1] != None:
            parents_ids = tuple(sorted(parents_ids))

        family_uuid = get_or_generate_family_uuid(families, parents_ids)

        # add siblings
        siblings_ids_string = [person_id]
        if families.get(family_uuid, None) != None: # if this family exists then append this sibling to the previously added ones
            siblings_ids_string += families[family_uuid][1] # append the previous siblings
        siblings_ids_string = tuple(siblings_ids_string)

        # register the updated family
        families[family_uuid] = [parents_ids, siblings_ids_string]

    # putting marriages after so node style is not repeated
    for marriage_id, marriage_data in marriages.items():
        families[marriage_id] = [tuple(marriage_data[:2]), (None, marriage_data[2])] # [(person_1_id, person_2_id), (None, marriage_date)] # None is there to make it possible to distinguish a marriage from a family with children

    dot_source = ""
    
    # 
    dot_source += "digraph {"

    # graph settings
    dot_source += f"\n\tlabel=\"{tree_title}\n\n\" labelloc=\"t\" fontsize=\"44\" fontname=\"Consolas\""

    # graph style
    # if tree_style == STYLE_SQUARES:
    #     node_style = ""
    #     splines = "ortho"
    if tree_style == STYLE_CURVES:
        node_style = ""
        splines = "true"
    elif tree_style == STYLE_STRAIGHT:
        node_style = ", rounded"
        splines = "false"
    elif tree_style == STYLE_ROUNDED:
        node_style = ", rounded"
        splines = "true"

    dot_source += f"\n\tgraph ["
    dot_source += f"\n\t\tbgcolor=\"grey94\""
    dot_source += f"\n\t\tsplines=\"{splines}\""
    dot_source += f"\n\t\tpad=\"0.7\""
    dot_source += f"\n\t\tnodesep=\"0.5\""
    dot_source += f"\n\t\tranksep=\"0.8\""
    dot_source += f"\n\t\trankdir=\"tb\""
    dot_source += f"\n\t]"


    # default node settings
    dot_source += "\n\tnode ["
    dot_source += "\n\t\tshape=\"rect\""
    dot_source += f"\n\t\tstyle=\"filled{node_style}\""
    dot_source += "\n\t\tfontname=\"Consolas\""
    dot_source += "\n\t]"

    # default node settings
    dot_source += "\n\tedge ["
    dot_source += "\n\t\tpenwidth=2"
    dot_source += "\n\t\tfontname=\"Consolas\""
    dot_source += "\n\t]"
    
    for family_id, family_data in families.items():
        edge_color = random_color()
        connector_id = f"\"connector_{family_id.strip("\"")}\""
        connector_style = None

        # parents

        # parent 1
        parent_1_id = family_data[0][0]
        parent_2_id = family_data[0][1]

        # marriage
        if family_data[1][0] == None:
            marriage_date = family_data[1][1]

            dot_source += "\n\t{" + f"rank=\"same\"; {parent_1_id}; {parent_2_id}" + "}"
            dot_source += f"\n\t{parent_1_id} -> {parent_2_id} [label=\"{marriage_date}\" arrowsize=0 color=\"{edge_color}\"]"

            parent_1_data = people.get(parent_1_id)
            parent_1_node_style = get_person_node_style(parent_1_id, parent_1_data, focused_person_id == parent_1_id)

            parent_2_data = people.get(parent_2_id)
            parent_2_node_style = get_person_node_style(parent_2_id, parent_2_data, focused_person_id == parent_2_id)

            if not parent_1_node_style in dot_source:
                dot_source += f"\n\t{parent_1_node_style}"
            if not parent_2_node_style in dot_source:
                dot_source += f"\n\t{parent_2_node_style}"
        # family (marriage + siblings)
        else:
            # add connector node connection only if there is at least one parent to connect to the sibling
            should_connecto_parent_to_sibling = parent_1_id != None or parent_2_id != None

            # don't save people with no registered parents
            if not should_connecto_parent_to_sibling: continue
            
            connector_style = get_connector_node_style(connector_id, edge_color)

            def get_parent_to_connector_source(parent_1_id:str, connector_id:str, edge_color:str):
                parent_1_part = ""
                parent_1_node_style = None
                if parent_1_id != None:
                    parent_1_part += f"{parent_1_id}:s -> {connector_id} [arrowsize=0 color=\"{edge_color}\"]"

                    parent_1_data = people.get(parent_1_id)
                    parent_1_node_style = get_person_node_style(parent_1_id, parent_1_data, focused_person_id == parent_1_id)
                
                return parent_1_part, parent_1_node_style

            # parent 1
            parent_1_part, parent_1_node_style = get_parent_to_connector_source(parent_1_id, connector_id, edge_color)

            # parent 2
            parent_2_part, parent_2_node_style = get_parent_to_connector_source(parent_2_id, connector_id, edge_color)
            
            # add parents dot code to source
            dot_source += f"\n\t{parent_1_part}"
            dot_source += f"\n\t{parent_2_part}"

            # siblings
            # node_1 -> sibling_0_id:n, sibling_1_id:n [arrowsize=0.5 color="green"]
            siblings_part = ""

            siblings_ids = family_data[1]
            # siblings_ids_string = ":n, ".join(siblings_ids) + ":n"

            def get_connector_to_sibling_source(sibling_id:str, connector_id:str, edge_color:str):
                return f"\n\t{connector_id} -> {sibling_id}:n [arrowsize=0.5 color=\"{edge_color}\"]"

            # add connector node connection only if there is at least one parent to connect to the sibling
            for sibling_id in siblings_ids:
                siblings_part += get_connector_to_sibling_source(sibling_id, connector_id, edge_color)

            # add siblings dot code to source
            dot_source += f"{siblings_part}"

            # add node style parts
            # parent 1
            if parent_1_node_style != None:
                dot_source += f"\n\t{parent_1_node_style}"
            # parent 2
            if parent_2_node_style != None:
                dot_source += f"\n\t{parent_2_node_style}"
            # siblings
            for sibling_id in siblings_ids:
                dot_source += f"\n\t{get_person_node_style(sibling_id, people.get(sibling_id), focused_person_id == sibling_id)}"
            # connectors
            if connector_style != None:
                dot_source += f"\n\t{connector_style}"
    
    dot_source += "\n}"
    
    return dot_source

FILE_PNG = "png"
FILE_PDF = "pdf"
def compile_dot(path:str, dot_source:str, file_type:int, save_dot_source:bool, dot_path:str|None):
    """
    Returns True if successfully compiled the tree, False otherwise
    """
    try:
        # write the dot file
        if save_dot_source:
            with open(dot_path, "w") as f:
                f.write(dot_source)

        # compile the tree file
        (graph,) = pydot.graph_from_dot_data(dot_source)
        graph.write(path, prog="dot", format=file_type)

        return True
    except:
        return False