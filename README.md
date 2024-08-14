# BMP Image Processing README

## Overview

This Python script provides basic functionality to load, modify, and save BMP images. It is capable of parsing the BMP file header, extracting image metadata, modifying the color channels of the image, and saving the modified image back to disk.

## Features

1. **Load BMP Images**: The script reads BMP files and extracts key information such as image dimensions, bits per pixel, color palette, and pixel data.
2. **Save BMP Images**: After modifying the image data, the script can save the BMP image to a new file.
3. **Modify Color Channels**: The script can modify the color palette of a BMP image by zeroing out a specific color channel (red, green, or blue).
4. **Batch Processing**: The script processes a list of BMP images and applies transformations to them.

## How to Use

### 1. Loading BMP Images

The `load_bmp_image(filepath)` function reads a BMP file from the specified `filepath` and returns a dictionary containing the image's metadata and pixel data.

**Example Usage:**

```python
image_data = load_bmp_image("example.bmp")
if image_data:
    print("Image loaded successfully.")
```

### 2. Saving BMP Images

The `save_bmp(image_info, output_path)` function saves the BMP image data contained in `image_info` to a file specified by `output_path`.

**Example Usage:**

```python
save_bmp(image_data, "example_processed.bmp")
```

### 3. Modifying Color Channels

The `modify_color_channel(image_info, channel_index, output_path)` function modifies the color palette of the BMP image by setting a specific color channel (red, green, or blue) to zero. The modified image is then saved to the specified `output_path`.

- `channel_index`: The index of the color channel to modify (0 for red, 1 for green, 2 for blue).
- `output_path`: The file path to save the modified image.

**Example Usage:**

```python
modify_color_channel(image_data, 0, "example_red_channel_removed.bmp")  # Removes the red channel
```

### 4. Batch Processing

The script processes a predefined list of BMP images. For each image, it loads the image data, displays the metadata, saves the image with a new filename, and modifies the color channels of the "corn.bmp" image.

**List of BMP Images:**

```python
images = ["cameraman.bmp", "corn.bmp", "pepper.bmp"]
```

### Processing and Modifying Example

The script processes the images in the `images` list. For the "corn.bmp" image, it creates three additional versions with the red, green, and blue channels removed, respectively.

**Example Output Files:**

- `corn_red_channel_removed.bmp`
- `corn_green_channel_removed.bmp`
- `corn_blue_channel_removed.bmp`

## Prerequisites

- Python 3.x
- BMP images to process

## Running the Script

Simply run the script in a Python environment where the BMP images are accessible. The script will automatically process the listed images and save the modified versions.

```bash
python bmp_processing.py
```

## Notes

- The script currently handles BMP images with a color depth of 8 bits per pixel or less.
- The BMP format must adhere to the standard Windows BMP format (i.e., starting with the "BM" magic number).

## License

This code is provided as-is without any warranty. Feel free to modify and distribute it as needed.
