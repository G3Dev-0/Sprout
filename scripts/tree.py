from random import randint
from utils import *

import pydot

# sex based coloring
MALE_COLOR_STYLE = "color=\"blue\"\n\t\tfillcolor=\"lightblue\""
FEMALE_COLOR_STYLE = "color=\"red\"\n\t\tfillcolor=\"pink\""
UNKNOWN_COLOR_STYLE = "color=\"black\"\n\t\tfillcolor=\"darkgrey\""
FOCUSED_COLOR_STYLE = "color=\"orange\"\n\t\tfillcolor=\"gold\""

# avaiable edge colors
COLORS = ["#619E1C", "#297F23", "#ED8F31", "#EF6502", "#A85426", "#207EBC", "#653A92", "#827DC6", "#D7191B", "#DB2783", "#FFC423", "#9E701C", "#1A9671", "#616161", "#00BABA"]
def random_color():
    """
    Picks a random color for edges
    """
    return COLORS[randint(0, len(COLORS) - 1)]

def get_person_node_style(person_id:str, person_data:list, focused:bool) -> str:
    """
    Returns a person node properties descriptor in dot source
    """

    # retrieve person data
    person_data = list(person_data)
    if len(person_data[1]) > 0: person_data[1] = f"\\\"{person_data[1]}\\\"" # this is needed to surround the alias with double quotes
    
    birth_date = person_data[4]
    death_date = person_data[5]
    
    name_alias_surname = "\"" + " ".join(person_data[:3]) # formatted as name "alias" surname
    name_alias_surname = name_alias_surname.replace("  ", " ") # removes the double space caused by the absence of an alias
    # also add birth date
    if len(birth_date.strip()) > 0:
        separator = " " if len(death_date.strip()) > 0 else ""
        name_alias_surname += f"\n*{birth_date}{separator}"
    # and death date
    if len(death_date.strip()) > 0:
        name_alias_surname += f"+{death_date}"
    name_alias_surname += "\""

    sex = person_data[3]
    image_path = person_data[8]
    
    node_style = f"{person_id} ["
    # set label
    node_style += f"\n\t\tlabel={name_alias_surname}"
    # set color
    if focused:
        node_style += f"\n\t\t{FOCUSED_COLOR_STYLE}"
    elif sex == SEX_MALE:
        node_style += f"\n\t\t{MALE_COLOR_STYLE}"
    elif sex == SEX_FEMALE:
        node_style += f"\n\t\t{FEMALE_COLOR_STYLE}"
    elif sex == SEX_UNKNOWN:
        node_style += f"\n\t\t{UNKNOWN_COLOR_STYLE}"
    # set the image if needed
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

def get_connector_node_style(connector_id:str, color:str) -> str:
    """
    Returns a connector node properties descriptor in dot source
    """
    connector_style = f"{connector_id} ["
    connector_style += "\n\t\tlabel=\"\""
    connector_style += f"\n\t\tcolor=\"{color}\""
    connector_style += f"\n\t\tfillcolor=\"{color}\""
    connector_style += f"\n\t\twidth=0.1"
    connector_style += f"\n\t\theight=0.1"
    connector_style += "\n\t]"

    return connector_style

def get_or_generate_family_uuid(families:dict, parents_ids:tuple) -> str:
    """
    Returns the uuid of a family (based on the parents ids) or
    generates a new uuid if the family (parents ids pair) was not already registered
    Used for connectors (identifies a family)
    """
    # always assume that siblings with both None parents come from different families
    if parents_ids[0] == parents_ids[1] == None:
        return generate_uuid4()

    # search for the uuid and return it in case it's found
    for family_id, family_data in families.items():
        if family_data[0] == parents_ids:
            return family_id
    # generate a new one if it was not found
    return generate_uuid4()

def generate_dot_source(people:dict, marriages:dict, tree_title:str, tree_style:int, focused_person_id:str|None) -> str:
    """
    Returns the dot source decribing the family tree graph based on the given tree data
    """
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

    # registering marriages after so the people node style is not repeated in dot source
    for marriage_id, marriage_data in marriages.items():
        families[marriage_id] = [tuple(marriage_data[:2]), (None, marriage_data[2])] # [(person_1_id, person_2_id), (None, marriage_date)] # None is there to make it possible to distinguish a marriage from a family with children

    # start building the dot source code
    dot_source = "digraph {"

    # graph settings
    dot_source += f"\n\tlabel=\"{tree_title}\n\n\" labelloc=\"t\" fontsize=\"44\" fontname=\"Consolas\""

    # graph style (ortho breaks sometimes so won't use it until a good solution is found)
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

    # set the graph settings
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

    # default edge settings
    dot_source += "\n\tedge ["
    dot_source += "\n\t\tpenwidth=2"
    dot_source += "\n\t\tfontname=\"Consolas\""
    dot_source += "\n\t]"

    # create the nodes and edges
    for family_id, family_data in families.items():
        edge_color = random_color() # get an edge color
        connector_id = f"\"connector_{family_id.strip("\"")}\"" # get the connector id
        connector_style = None # set later (this will be the connector node properties dot source descriptor)

        # parent 1
        parent_1_id = family_data[0][0]
        parent_2_id = family_data[0][1]

        # marriages (couples without children)
        if family_data[1][0] == None:
            marriage_date = family_data[1][1]

            # give them the same ranking otherwise they appear at different heights
            dot_source += "\n\t{" + f"rank=\"same\"; {parent_1_id}; {parent_2_id}" + "}"
            # person_1_id -> person_2_id [label="marriage_date" arrowsize=0 color="edge_color"]
            dot_source += f"\n\t{parent_1_id} -> {parent_2_id} [label=\"{marriage_date}\" arrowsize=0 color=\"{edge_color}\"]"

            parent_1_data = people.get(parent_1_id)
            parent_1_node_style = get_person_node_style(parent_1_id, parent_1_data, focused_person_id == parent_1_id)

            parent_2_data = people.get(parent_2_id)
            parent_2_node_style = get_person_node_style(parent_2_id, parent_2_data, focused_person_id == parent_2_id)

            """
            This conditions make it impossible to add a person node descriptor twice.
            It can happen that a person (A) has registered parents, thus A is already described in dot source becasue families (with children)
            are registered BEFORE marriages (couples with no childer), because marriages are added after families.
            So if then a marriage between said person (A) and another person (B) is registered, (A) would be described twice
            (once as the family is registered, and then when the marriage is registered).
            To prevent this from happening we just check if the node descriptor is already there in the dot source and if so we don't add it.
            """
            if not parent_1_node_style in dot_source:
                dot_source += f"\n\t{parent_1_node_style}"
            if not parent_2_node_style in dot_source:
                dot_source += f"\n\t{parent_2_node_style}"
        # families (couples with children)
        else:
            # add connector node connection only if there is at least one parent to connect to the sibling
            # if the current person has no parents Sprout will just add the person and show them in the graph with no connections
            should_connect_parent_to_sibling = parent_1_id != None or parent_2_id != None

            # set the connector properties dot source descriptor
            connector_style = get_connector_node_style(connector_id, edge_color)

            # small function to not repeat code twice
            def get_parent_to_connector_source(parent_1_id:str, connector_id:str, edge_color:str):
                parent_1_part = ""
                parent_1_node_style = None
                if parent_1_id != None:
                    # parent_id:s -> connector_id [arrowsize=0 color="edge_color"]
                    parent_1_part += f"{parent_1_id}:s -> {connector_id} [arrowsize=0 color=\"{edge_color}\"]"

                    parent_1_data = people.get(parent_1_id)
                    parent_1_node_style = get_person_node_style(parent_1_id, parent_1_data, focused_person_id == parent_1_id)
                
                return parent_1_part, parent_1_node_style

            # add parents nodes to dot source only if they are registered for the current person
            if should_connect_parent_to_sibling:
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

            # small function to not repeat code twice
            def get_connector_to_sibling_source(sibling_id:str, connector_id:str, edge_color:str):
                # add the connector only if there are parents registered for the current person
                if should_connect_parent_to_sibling:
                    result = f"\n\t{connector_id} -> {sibling_id}:n [arrowsize=0.5 color=\"{edge_color}\"]"
                # only add the person node if there are no parents registered for the current person
                else:
                    result = f"\n\t{sibling_id}"
                return result

            # add connector node connection only if there is at least one parent to connect to the sibling
            for sibling_id in siblings_ids:
                siblings_part += get_connector_to_sibling_source(sibling_id, connector_id, edge_color)

            # add siblings dot code to source
            dot_source += f"{siblings_part}"

            # add node properties descriptors
            if should_connect_parent_to_sibling:
                # parent 1
                if parent_1_node_style != None:
                    dot_source += f"\n\t{parent_1_node_style}"
                # parent 2
                if parent_2_node_style != None:
                    dot_source += f"\n\t{parent_2_node_style}"
            # siblings
            for sibling_id in siblings_ids:
                dot_source += f"\n\t{get_person_node_style(sibling_id, people.get(sibling_id), focused_person_id == sibling_id)}"
            if should_connect_parent_to_sibling:
                # connectors
                if connector_style != None:
                    dot_source += f"\n\t{connector_style}"
    
    dot_source += "\n}"
    
    return dot_source

FILE_PNG = "png"
FILE_PDF = "pdf"
def compile_dot(path:str, dot_source:str, file_type:int, save_dot_source:bool, dot_path:str|None) -> bool:
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
