import os
from tkinter import Tk, Label, Button, filedialog, StringVar, OptionMenu
from PIL import Image, UnidentifiedImageError

def combine_images(folder_path, layout='horizontal'):
    """
    Combines all images in a folder into a single image and saves it using the folder name.

    Args:
        folder_path (str): Path to the folder containing images.
        layout (str): Layout for combining images ('horizontal' or 'vertical').
    """
    folder_name = os.path.basename(folder_path)
    # Get all image files from the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if len(image_files) < 2:
        status_var.set(f"Skipping '{folder_name}' (not enough images).")
        return

    try:
        # Load and resize images to the same dimensions
        images = [Image.open(os.path.join(folder_path, img)) for img in image_files]
        max_width = max(img.width for img in images)
        max_height = max(img.height for img in images)
        resized_images = [img.resize((max_width, max_height)) for img in images]

        # Determine the size of the combined image
        if layout == 'horizontal':
            combined_width = sum(img.width for img in resized_images)
            combined_height = max_height
            combined_image = Image.new('RGB', (combined_width, combined_height))
            x_offset = 0
            for img in resized_images:
                combined_image.paste(img, (x_offset, 0))
                x_offset += img.width
        elif layout == 'vertical':
            combined_width = max_width
            combined_height = sum(img.height for img in resized_images)
            combined_image = Image.new('RGB', (combined_width, combined_height))
            y_offset = 0
            for img in resized_images:
                combined_image.paste(img, (0, y_offset))
                y_offset += img.height
        else:
            status_var.set("Invalid layout selected.")
            return

        # Save the combined image
        save_path = os.path.join(folder_path, f"{folder_name}.jpg")
        combined_image.save(save_path)
        status_var.set(f"Saved combined image: {save_path}")

    except UnidentifiedImageError:
        status_var.set(f"Error: Unable to process images in '{folder_name}'.")

def process_all_folders(base_path, layout='horizontal'):
    """
    Processes all subfolders in a given base directory.

    Args:
        base_path (str): Path to the base directory containing subfolders.
        layout (str): Layout for combining images ('horizontal' or 'vertical').
    """
    if not os.path.exists(base_path):
        status_var.set("Invalid folder path.")
        return

    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):  # Process only subfolders
            combine_images(folder_path, layout)
    status_var.set("Processing complete!")

def select_folder():
    """
    Open a file dialog to select the base folder and update the GUI.
    """
    folder = filedialog.askdirectory()
    if folder:  # If a folder is selected
        folder_var.set(folder)
        status_var.set(f"Selected folder: {folder}")

def run_app():
    """
    Run the image combination process.
    """
    base_path = folder_var.get()
    selected_layout = layout_var.get()
    if not base_path:
        status_var.set("Please select a folder.")
        return
    status_var.set("Processing started...")
    process_all_folders(base_path, layout=selected_layout)

# Create the main GUI window
root = Tk()
root.title("Image Combiner App")
root.geometry("400x300")

# Variables for GUI components
folder_var = StringVar()
layout_var = StringVar(value="horizontal")
status_var = StringVar()

# Folder Selection
Label(root, text="Select Base Folder:").pack(pady=5)
Button(root, text="Browse", command=select_folder).pack(pady=5)
Label(root, textvariable=folder_var, wraplength=300).pack(pady=5)

# Layout Selection
Label(root, text="Select Layout:").pack(pady=5)
OptionMenu(root, layout_var, "horizontal", "vertical").pack(pady=5)

# Run Button
Button(root, text="Run", command=run_app).pack(pady=20)

# Status Display
Label(root, text="Status:").pack(pady=5)
Label(root, textvariable=status_var, wraplength=300).pack(pady=5)

# Run the GUI loop
root.mainloop()

