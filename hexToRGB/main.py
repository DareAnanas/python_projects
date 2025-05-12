def hexToRgba(hex_color, alpha=1):
    # Convert a hex color string to an RGBA tuple (0-1 range).
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    print(r, g, b)
    return [round(r / 255.0, 4), round(g / 255.0, 4), round(b / 255.0, 4), alpha]


print(hexToRgba('#A52A2A'))

# print(int(0.11764705882352941 * 255))


