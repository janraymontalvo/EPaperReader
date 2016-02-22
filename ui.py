from PIL import Image, ImageDraw, ImageFont
import textwrap

# def Alert(message):
# 	para = textwrap.wrap(message, width=15)

# 	MAX_W, MAX_H = 200, 200
# 	im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
# 	draw = ImageDraw.Draw(im)
# 	font = ImageFont.truetype('resources/fonts/ACaslonPro-Regular.otf', 16)

# 	current_h, pad = 50, 10
# 	for line in para:
# 	    w, h = draw.textsize(line, font=font)
# 	    draw.text(((MAX_W - w) / 2, current_h), line, font=font)
# 	    current_h += h + pad

# 	return im;
