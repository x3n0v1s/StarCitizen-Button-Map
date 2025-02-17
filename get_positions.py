import cv2

# Load images
evo_img = cv2.imread('EVO.jpg')
evo_omni_img = cv2.imread('EVO_OMNI.jpg')

# Initialize global variables
coordinates = []

# Click event handler
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at: ({x}, {y})")
        coordinates.append((x, y))

# Display image for EVO.jpg
print("Click on the positions for EVO.jpg...")
cv2.imshow('EVO', evo_img)
cv2.setMouseCallback('EVO', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Coordinates for EVO.jpg:", coordinates)
evo_positions = coordinates.copy()  # Save the EVO positions
coordinates.clear()

# Display image for EVO_OMNI.jpg
print("Click on the positions for EVO_OMNI.jpg...")
cv2.imshow('EVO_OMNI', evo_omni_img)
cv2.setMouseCallback('EVO_OMNI', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Coordinates for EVO_OMNI.jpg:", coordinates)
evo_omni_positions = coordinates.copy()

# Output the positions in a usable format
print("\nButton positions for EVO.jpg:")
for i, pos in enumerate(evo_positions, start=1):
    print(f"'{i}': {pos},")

print("\nButton positions for EVO_OMNI.jpg:")
for i, pos in enumerate(evo_omni_positions, start=1):
    print(f"'{i}': {pos},")
