def make_image_black(image_path):
    img = Image.open(image_path).convert("RGBA")

    # Get the pixel data from the image
    pixels = img.load()

    # Iterate over each pixel and update the color values
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b, a = pixels[i, j]

            # Check if alpha value is greater than or equal to 1
            if a >= 1:
                pixels[i, j] = (0, 0, 0, a)

    # Save the resulting image to a file
    img.save(f"{image_path[:-4]}_black.png")


crown_names = ['death', 'life', 'haste', 'guns', 'hatred', 'blood', 'destiny', 'love', 'luck', 'curses', 'risk', 'protection']
for crown in crown_names:
    path = f"C:\\Users\\jspen\\Desktop\\Fun Projects\\programming languages\\snek\\nt_tracker\\{crown}.png"
    make_image_black(path)

