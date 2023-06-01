from PIL import Image

MINIMUM_LINE_HEIGHT = 4
MINIMUM_LINE_WIDTH = 25
WHITE_RGB = (255, 255, 255)

"""
Returns the height from the starting_y variable until the pixel is white or the end of the image height.
"""


def get_line_height(pix, height, starting_y, x):
    height_from_starting_y = 0
    for y in range(starting_y, height):
        if pix[x, y] == WHITE_RGB:
            break
        height_from_starting_y += 1
    return height_from_starting_y


"""
Returns the width of the line.

We scan from the starting_x and starting_y values, we scan from this starting point if the height from there is equal or
greater than MINIMUM_LINE_HEIGHT using get_line_height function and for each successful scan we iterate to the next x 
value.

once the height from the current x is not equal or greater than the MINIMUM_LINE_HEIGHT value or we reached the end 
of the x axis we stop scanning and proceed to check if width_from_starting_x is equal or greater than 
MINIMUM_LINE_WIDTH.

If it is, we return width_from_starting_x which is equal to the width of the line we found.
If it is not, we return -1.

* No need to return the height since we assume that the height of the line will always be the same, defined by 
MINIMUM_LINE_HEIGHT parameter.

"""


def get_line(pix, width, height, starting_x, starting_y):
    width_from_starting_x = 0
    while starting_x + width_from_starting_x < width \
            and get_line_height(pix, height, starting_y, starting_x + width_from_starting_x) >= MINIMUM_LINE_HEIGHT:
        width_from_starting_x += 1
    if width_from_starting_x >= MINIMUM_LINE_WIDTH:
        return width_from_starting_x
    return -1


"""
Returns a new image matrix with the requested line removed.
"""


def remove_line(pix, starting_x, starting_y, width):
    for x in range(starting_x, starting_x + width):
        for y in range(starting_y, starting_y + MINIMUM_LINE_HEIGHT):
            pix[x, y] = WHITE_RGB
    return pix


"""
Scans the pixel array of an image.
If we reached a pixel that is not white we summon the function get_line and see if there is a line (defined by our
line size requirements) and if so we proceed to remove it with remove_line.

Returns the new pixel array with the removed lines.
"""


def scan_image(pix, width, height):
    for x in range(width):
        for y in range(height):
            if pix[x, y] != WHITE_RGB:
                line_width = get_line(pix, width, height, x, y)
                if line_width == -1:
                    continue
                pix = remove_line(pix, x, y, line_width)
    return pix


"""
Opens the image from the image_path parameter, takes its pixel array, width and height and sends it for our scanning
image to find lines, if it finds, it removes them and returns a new pixel array without them which we use to override
the image we got.
"""


def remove_lines_from_equation(image_path):
    im = Image.open(image_path)  # Can be many different formats.
    pix = im.load()
    width, height = im.size
    pix = scan_image(pix, width, height)
    im.save(image_path)  # Save the modified pixels as .png
