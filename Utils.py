def hex_to_rgb(hex_color):
    """Convert hex string to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def calculate_luminance(hex_color):
    """Calculate relative luminance of a color."""
    r, g, b = hex_to_rgb(hex_color)
    return (0.299 * r) + (0.587 * g) + (0.114 * b)


def get_text_color(hex_color):
    """Returns 'black' or 'white' based on luminance contrast."""
    luminance = calculate_luminance(hex_color)
    return "black" if luminance > 128 else "white"
