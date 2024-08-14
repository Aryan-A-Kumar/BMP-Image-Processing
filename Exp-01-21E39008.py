def load_bmp_image(filepath):
    with open(filepath, "rb") as file:
        # File header parsing
        magic_number = file.read(2).decode("ascii")
        if magic_number != "BM":
            return None
        
        file_size = int.from_bytes(file.read(4), "little")
        reserved_data = int.from_bytes(file.read(4), "little")
        pixel_data_offset = int.from_bytes(file.read(4), "little")

        # BMP Header parsing
        header_size = int.from_bytes(file.read(4), "little")
        image_width = int.from_bytes(file.read(4), "little")
        image_height = int.from_bytes(file.read(4), "little")
        color_planes = int.from_bytes(file.read(2), "little")
        bpp = int.from_bytes(file.read(2), "little")
        compression_method = int.from_bytes(file.read(4), "little")
        bitmap_size = int.from_bytes(file.read(4), "little")
        horizontal_resolution = int.from_bytes(file.read(4), "little")
        vertical_resolution = int.from_bytes(file.read(4), "little")
        palette_colors = int.from_bytes(file.read(4), "little")
        important_colors = int.from_bytes(file.read(4), "little")

        # Parsing color table if applicable
        color_palette = []
        if bpp <= 8:
            for _ in range(palette_colors):
                blue, green, red, _ = file.read(4)
                color_palette.append((red, green, blue))

        # Reading pixel data into an array
        pixel_data = []
        for _ in range(image_height):
            row_data = []
            for _ in range(image_width):
                row_data.append(int.from_bytes(file.read(bpp // 8), "little"))
            pixel_data.append(row_data)

        return {
            "filepath": filepath,
            "file_size": file_size,
            "pixel_data_offset": pixel_data_offset,
            "width": image_width,
            "height": image_height,
            "bits_per_pixel": bpp,
            "bitmap_size": bitmap_size,
            "color_palette": color_palette,
            "pixel_data": pixel_data
        }

def save_bmp(image_info, output_path):
    with open(output_path, "wb") as file:
        # Writing file header
        magic_number = "BM"
        header_size = 14 + 40 + (len(image_info["color_palette"]) * 4 if image_info["bits_per_pixel"] <= 8 else 0)
        total_size = header_size + image_info["height"] * image_info["width"] * image_info["bits_per_pixel"] // 8
        reserved_data = 0

        file.write(magic_number.encode("ascii"))
        file.write(total_size.to_bytes(4, "little"))
        file.write(reserved_data.to_bytes(4, "little"))
        file.write(header_size.to_bytes(4, "little"))

        # Writing BMP Header
        file.write((40).to_bytes(4, "little"))
        file.write(image_info["width"].to_bytes(4, "little"))
        file.write(image_info["height"].to_bytes(4, "little"))
        file.write((1).to_bytes(2, "little"))  # color planes
        file.write(image_info["bits_per_pixel"].to_bytes(2, "little"))
        file.write((0).to_bytes(4, "little"))  # no compression
        file.write(image_info["bitmap_size"].to_bytes(4, "little"))
        file.write((0).to_bytes(4, "little"))  # horizontal resolution
        file.write((0).to_bytes(4, "little"))  # vertical resolution
        file.write(len(image_info["color_palette"]).to_bytes(4, "little"))
        file.write((0).to_bytes(4, "little"))  # important colors

        # Writing color palette if applicable
        if image_info["bits_per_pixel"] <= 8:
            for color in image_info["color_palette"]:
                file.write(bytes(color[::-1]) + b'\x00')

        # Writing pixel data
        for row in image_info["pixel_data"]:
            for pixel in row:
                file.write(pixel.to_bytes(image_info["bits_per_pixel"] // 8, "little"))

def modify_color_channel(image_info, channel_index, output_path):
    modified_palette = [list(color) for color in image_info["color_palette"]]
    new_image_info = image_info.copy()
    for color in modified_palette:
        color[channel_index] = 0
    new_image_info["color_palette"] = [tuple(color) for color in modified_palette]
    save_bmp(new_image_info, output_path)

# List of BMP image filenames
images = ["cameraman.bmp", "corn.bmp", "pepper.bmp"]

# Processing each image
for image_filename in images:
    image_data = load_bmp_image(image_filename)
    if image_data:
        # Display image metadata
        print(f"Processing Image: {image_filename}")
        print(f"  Dimensions: {image_data['width']}x{image_data['height']} pixels")
        print(f"  Bits per Pixel: {image_data['bits_per_pixel']}")
        print(f"  Image Size: {image_data['bitmap_size']} bytes")
        print(f"  Colors Used: {len(image_data['color_palette'])} colors")

        # Save the processed image with a new filename
        new_filename = image_filename.replace(".bmp", "_processed.bmp")
        save_bmp(image_data, new_filename)

        # Apply channel modifications to the 'corn.bmp' image
        if image_filename == "corn.bmp":
            modify_color_channel(image_data, 0, "corn_red_channel_removed.bmp")  # Red channel
            modify_color_channel(image_data, 2, "corn_blue_channel_removed.bmp")  # Blue channel
            modify_color_channel(image_data, 1, "corn_green_channel_removed.bmp")  # Green channel