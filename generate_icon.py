#!/usr/bin/env python3
from PIL import Image, ImageDraw

# Create a 64x64 image with transparent background
img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw canvas frame (white canvas with border)
draw.rounded_rectangle([(4, 4), (60, 60)], radius=4, fill='#FFFFFF', outline='#95A5A6', width=2)

# Draw inner canvas area
draw.rounded_rectangle([(8, 8), (56, 56)], radius=2, fill='#F8F8F8')

# Draw colorful doodles/squiggles on the canvas
# Pink squiggle (matching DARKPINK from the app)
draw.ellipse([(14, 16), (26, 28)], fill='#EC048C')
draw.ellipse([(18, 22), (30, 34)], fill='#EC048C')
draw.ellipse([(22, 28), (34, 40)], fill='#EC048C')

# Blue doodle
draw.ellipse([(32, 14), (44, 26)], fill='#3498DB')
draw.ellipse([(36, 20), (48, 32)], fill='#3498DB')

# Yellow/Orange doodle
draw.ellipse([(16, 36), (28, 48)], fill='#F39C12')
draw.ellipse([(20, 42), (32, 54)], fill='#F39C12')

# Purple accent
draw.ellipse([(38, 34), (48, 44)], fill='#9B59B6')

# Draw cursor crosshair (green to match app's CURSOR_COLOR)
cursor_x, cursor_y = 46, 18
cursor_size = 6
# Outer circle (white outline for visibility)
draw.ellipse([(cursor_x - cursor_size, cursor_y - cursor_size),
              (cursor_x + cursor_size, cursor_y + cursor_size)],
             outline='#FFFFFF', width=2)
# Inner circle (green)
draw.ellipse([(cursor_x - cursor_size + 1, cursor_y - cursor_size + 1),
              (cursor_x + cursor_size - 1, cursor_y + cursor_size - 1)],
             fill='#00FF00', outline='#00CC00', width=1)

# Save to res/mipmap-mdpi directory
img.save('res/mipmap-mdpi/icon_64x64.png', 'PNG', optimize=True)
print("✓ Icon saved as res/mipmap-mdpi/icon_64x64.png")
print("  Canvas with colorful doodles and green cursor")
