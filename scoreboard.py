# -*- coding: iso-8859-15 -*-
from PIL import Image, ImageDraw, ImageFont

TEAMS = [{
    "name": "Kostanjevica na Krki",
    "color": "blue",
    "nameColor": "white",
    "sets": 2,
    "points": 25,
}, {
    "name": "ŠD Braslovce",
    "color": "green",
    "nameColor": "white",
    "sets": 0,
    "points": 1,
},]

SETTINGS = {
    "OUTPUT": "overlay",
    "FONT": "Antonio-Regular",
    "FONT_SIZE": 20,
    "COLOR": {
        "POINTS": {
            "FONT": "black",
            "BACKGROUND": "white",
        },
        "SETS": {
            "FONT": "black",
            "BACKGROUND": "white",
        },
        "BACKGROUND": (128, 128, 128, 128),
    },
    "MARGINS": 8,
    "HEIGHT": {
        "TEAM_RECT": 32,
        "SCOREBOARD": 88,
    },
    "WIDTH": {
        "TEAM_NAME_RECT": 166,
        "SETS_RECT": 20,
        "POINTS_RECT": 40,
        "SCOREBOARD": 258,
    }
}

def escape_team_name(name):
    return name \
        .replace("Č", "C") \
        .replace("č", "c") \
        .replace("Š", "S") \
        .replace("š", "s") \
        .replace("ž", "z")

img = Image.new(
    'RGBA', 
    (SETTINGS["WIDTH"]["SCOREBOARD"], SETTINGS["HEIGHT"]["SCOREBOARD"]), 
    color = SETTINGS["COLOR"]["BACKGROUND"]
)
# get a font
fnt = ImageFont.truetype("{}.ttf".format(SETTINGS["FONT"]), SETTINGS["FONT_SIZE"])
# get a drawing context
d = ImageDraw.Draw(img)

def centered_text(text, rect, text_color="white"):
    x1, y1, x2, y2 = rect
    W, H = (x2 - x1, y2 - y1)
    assert W >= 0 and H >= 0, "Invalid param `rect` ({}) in `centered_text`".format(rect)

    w, h = d.textsize(text, font=fnt)

    font_vertical_offset = -2 if SETTINGS["FONT"] == "Antonio-Regular" else 0

    d.text((x1 + (W-w)/2, y1 + (H-h)/2 + font_vertical_offset), text, font=fnt, fill=text_color)
    pass

def left_aligned_text(text, rect, text_color="white"):
    x1, y1, x2, y2 = rect
    W, H = (x2 - x1, y2 - y1)
    assert W >= 0 and H >= 0, "Invalid param `rect` ({}) in `centered_text`".format(rect)

    w, h = d.textsize(text, font=fnt)

    font_vertical_offset = -2 if SETTINGS["FONT"] == "Antonio-Regular" else 0

    d.text((x1 + SETTINGS["MARGINS"], y1 + (H-h)/2 + font_vertical_offset), text, font=fnt, fill=text_color)
    pass

def draw_team_info(team, vertical_offset=0):
    # Team name
    team_name_rect = (
        SETTINGS["MARGINS"], 
        SETTINGS["MARGINS"] + vertical_offset, 
        SETTINGS["MARGINS"] + SETTINGS["WIDTH"]["TEAM_NAME_RECT"], 
        SETTINGS["MARGINS"] + SETTINGS["HEIGHT"]["TEAM_RECT"] + vertical_offset
    )

    d.rectangle(team_name_rect, fill=team["color"], outline="black")
    left_aligned_text(escape_team_name(team["name"]), team_name_rect, team["nameColor"])

    # Sets
    sets_rect = (
        SETTINGS["MARGINS"] + team_name_rect[2],
        team_name_rect[1],
        SETTINGS["MARGINS"] + team_name_rect[2] + SETTINGS["WIDTH"]["SETS_RECT"],
        team_name_rect[3],
    )
    
    d.rectangle(sets_rect, fill=SETTINGS["COLOR"]["SETS"]["BACKGROUND"], outline="black")
    centered_text(str(team["sets"]), sets_rect, SETTINGS["COLOR"]["SETS"]["FONT"])

    # Points
    points_rect = (
        SETTINGS["MARGINS"] + sets_rect[2],
        team_name_rect[1],
        SETTINGS["MARGINS"] + sets_rect[2] + SETTINGS["WIDTH"]["POINTS_RECT"],
        team_name_rect[3],
    )
    
    d.rectangle(points_rect, fill=SETTINGS["COLOR"]["POINTS"]["BACKGROUND"], outline="black")
    centered_text(str(team["points"]), points_rect, SETTINGS["COLOR"]["POINTS"]["FONT"])

    # Return bottom-most coordinate so that it is used as 
    # the `vertical_offset` in the next call.
    return team_name_rect[3]


offset = draw_team_info(TEAMS[0])
draw_team_info(TEAMS[1], offset)

img.save("{}.png".format(SETTINGS["OUTPUT"]))

def update_scoreboard(teams):
    offset = draw_team_info(teams[0])
    draw_team_info(teams[1], offset)
    img.save("{}.png".format(SETTINGS["OUTPUT"]))
    pass

if (__name__ == "__main__"):
    update_scoreboard(TEAMS)
    pass