# Print things to the stdout in Color
# By way of John Schulman at- https://spinningup.openai.com/en/latest/_modules/spinup/utils/logx.html#Logger

color2num = dict(
    gray=30,
    red=31,
    green=32,
    yellow=33,
    blue=34,
    magenta=35,
    cyan=36,
    white=37,
    crimson=39,
	#additional colors do string highlighting (i.e, 42 prints strings highlighted green w white text) or are plain white
	red_highlight=41,
	green_highlight=42,
	yellow_highlight=43,
	blue_highlight=44,
)

def colorize(string, color, bold=False, highlight=False):
    """
    Colorize a string.

    This function was originally written by John Schulman.
    """
    attr = []
    num = color2num[color]
    if highlight: num += 10
    attr.append(str(num))
    if bold: attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


STRING = "colors are quite pretty"

for col in color2num:
	print(colorize(STRING, col))
