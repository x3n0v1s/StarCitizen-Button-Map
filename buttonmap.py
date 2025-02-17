import xml.etree.ElementTree as ET
import cv2
import re
from collections import defaultdict

# Load the layout.xml file
tree = ET.parse('layout.xml')
root = tree.getroot()

# Extract action id -> name mapping
action_map = {}
for action in root.findall(".//action"):
    action_name = action.get("name")
    if action_name:
        # Find the parent actionmap name
        actionmap_element = action.find("../..")
        if actionmap_element is not None:
            actionmap_name = actionmap_element.get("name")
            action_map[action_name] = actionmap_name

# Extract button number -> action name (supporting multiple actions per button)
mappingsjs1 = defaultdict(list)
for action in root.findall(".//action"):
    action_name = action.get("name")
    rebind = action.find("rebind")
    if rebind is not None:
        input_value = rebind.get("input")
        if input_value and action_name:
            match_button = re.search(r'js1_button(\d+)', input_value)
            match_hat = re.search(r'js1_hat1_(up|down|left|right)', input_value)
            if match_button:
                button_number = match_button.group(1)
                mappingsjs1[button_number].append(action_name)
            elif match_hat:
                hat_direction = match_hat.group(1)
                mappingsjs1[f"hat1_{hat_direction}"].append(action_name)

mappingsjs2 = defaultdict(list)
for action in root.findall(".//action"):
    action_name = action.get("name")
    rebind = action.find("rebind")
    if rebind is not None:
        input_value = rebind.get("input")
        if input_value and action_name:
            match_button = re.search(r'js2_button(\d+)', input_value)
            match_hat = re.search(r'js2_hat1_(up|down|left|right)', input_value)
            if match_button:
                button_number = match_button.group(1)
                mappingsjs2[button_number].append(action_name)
            elif match_hat:
                hat_direction = match_hat.group(1)
                mappingsjs2[f"hat1_{hat_direction}"].append(action_name)


# Load images
evo_img = cv2.imread('EVO.jpg')
evo_omni_img = cv2.imread('EVO_OMNI.jpg')

# Define button positions for EVO.jpg (example positions, adjust as needed)
button_positions_evo = {
    '1': (293, 945),
    '2': (237, 990),
    '3': (332, 360),
    '4': (415, 748),
    '5': (508, 651),
    '6': (1106, 270),
    '7': (1288, 319),
    '8': (1105, 370),
    '9': (924, 319),
    '10': (1120, 319),
    '11': (1053, 70),
    '12': (1241, 119),
    '13': (1057, 168),
    '14': (874, 119),
    '15': (1056, 127),
    '16': (1164, 465),
    '17': (1346, 524),
    '18': (1165, 588),
    '19': (983, 525),
    '20': (1167, 509),
    '21': (433, 835),
    '22': (435, 881),
    '23': (1310, 1010),
    '24': (1310, 1057),
    '25': (1134, 1180),
    '26': (1135, 1230),
    '27': (1179, 820),
    '28': (1248, 890),
    '29': (1106, 762),
    'hat1_up': (292, 70),
    'hat1_down': (292, 165),
    'hat1_left': (110, 119),
    'hat1_right': (474, 119),
}

# Define button positions for EVO_OMNI.jpg (example positions, adjust as needed)
button_positions_evo_omni = {
    '1': (1328, 950),
    '2': (1397, 1004),
    '3': (1323, 478),
    '4': (1157, 750),
    '5': (994, 603),
    '6': (469, 279),
    '7': (651, 322),
    '8': (468, 373),
    '9': (286, 322),
    '10': (482, 322),
    '11': (541, 77),
    '12': (727, 120),
    '13': (544, 170),
    '14': (362, 120),
    '15': (543, 131),
    '16': (299, 469),
    '17': (483, 529),
    '18': (300, 591),
    '19': (118, 529),
    '20': (301, 513),
    '21': (1174, 830),
    '22': (1177, 878),
    '23': (472, 1178),
    '24': (472, 1224),
    '25': (296, 1005),
    '26': (297, 1051),
    '27': (425, 831),
    '28': (502, 763),
    '29': (357, 896),
    'hat1_up': (1250, 75),
    'hat1_down': (1249, 165),
    'hat1_left': (1067, 120),
    'hat1_right': (1433, 120),
}

# Helper function to overlay multiple lines of text on images
def overlay_text(img, button_number, actions, positions):
    if button_number in positions:
        base_x, base_y = positions[button_number]  # Store the base position for each button
        line_height = 20  # Space between lines

        for i, action in enumerate(actions):
            y_offset = base_y + i * line_height  # Calculate y position for each line
            #cleaned_action = action.replace("v_", "", 1)  # Remove 'v_' prefix if it exists
            if "shield" in action:
                color = (255, 0, 0)  # Blue
            elif "weapon" in action:
                color = (0, 0, 255)  # Red
            else:
                color = (0, 0, 0)  # Black (default)
            cleaned_action = action.replace("v_", "", 1).replace("target", "t", 1).replace("shield", "s", 1).replace("weapon", "w", 1).replace("toggle", "tog", 1).replace("engineering", "e", 1)  # Remove 'v_' prefix if it exists
            cv2.putText(
                img,
                cleaned_action,
                (base_x, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                color,
                1,
                cv2.LINE_AA
            )

# Overlay text on EVO.jpg
for button, actions in mappingsjs2.items():
    overlay_text(evo_img, button, actions, button_positions_evo)

# Overlay text on EVO_OMNI.jpg
for button, actions in mappingsjs1.items():
    overlay_text(evo_omni_img, button, actions, button_positions_evo_omni)

# Save the modified images
evo_output_path = 'EVO_annotated.jpg'
evo_omni_output_path = 'EVO_OMNI_annotated.jpg'

cv2.imwrite(evo_output_path, evo_img)
cv2.imwrite(evo_omni_output_path, evo_omni_img)

print(f"Annotated images saved: {evo_output_path}, {evo_omni_output_path}")
