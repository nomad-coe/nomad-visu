from enum import Enum
from typing import Union
from itertools import cycle
from dataclasses import dataclass

import plotly.express as px


class SymbolsEnum(Enum):
    """List of possible marker symbols"""

    circle = "circle"
    circle_open = "circle-open"
    circle_dot = "circle-dot"
    circle_open_dot = "circle-open-dot"
    circle_cross = "circle-cross"
    circle_x = "circle-x"
    square = "square"
    square_open = "square-open"
    square_dot = "square-dot"
    square_open_dot = "square-open-dot"
    square_cross = "square-cross"
    square_x = "square-x"
    diamond = "diamond"
    diamond_open = "diamond-open"
    diamond_dot = "diamond-dot"
    diamond_open_dot = "diamond-open-dot"
    diamond_cross = "diamond-cross"
    diamond_x = "diamond-x"
    triangle_up = "triangle-up"
    triangle_up_open = "triangle-up-open"
    triangle_up_dot = "triangle-up-dot"
    triangle_up_open_dot = "triangle-up-open-dot"
    triangle_down = "triangle-down"
    triangle_down_open = "triangle-down-open"
    triangle_down_dot = "triangle-down-dot"
    triangle_down_open_dot = "triangle-down-open-dot"


class ColorEnum(Enum):
    """List of possible colors eg. of the hulls or of the regression line etc."""

    Black = "Black"
    Blue = "Blue"
    Cyan = "Cyan"
    Green = "Green"
    Grey = "Grey"
    Orange = "Orange"
    Red = "Red"
    Yellow = "Yellow"


class LineTypeEnum(Enum):
    """List of possible dash types eg. for the regression line orfor the hulls etc."""

    dash = "dash"
    solid = "solid"
    dot = "dot"
    longdash = "longdash"
    dashdot = "dashdot"
    longdashdot = "longdashdot"


class FontFamilyEnum(Enum):
    """List of possible font families"""

    Arial = "Arial"
    CourierNew = "Courier New"
    Helvetica = "Helvetica"
    OpenSans = "Open Sans"
    TimesNewRoman = "Times New Roman"
    Verdana = "Verdana"


class ColorTypeEnum(Enum):
    """eg. if a feature is used for color this can be 'Gradient' for continuous feature values or 'Discrete'"""

    Gradient = "Gradient"
    Discrete = "Discrete"


class DiscretePaletteEnum(Enum):
    """List of possible discrete palette colors"""

    Plotly = "Plotly"
    D3 = "D3"
    G10 = "G10"
    T10 = "T10"
    Alphabet = "Alphabet"
    Dark24 = "Dark24"
    Light24 = "Light24"
    Set1 = "Set1"
    Pastel1 = "Pastel1"
    Dark2 = "Dark2"
    Set2 = "Set2"
    Pastel2 = "Pastel2"
    Set3 = "Set3"
    Antique = "Antique"
    Bold = "Bold"
    Pastel = "Pastel"
    Prism = "Prism"
    Safe = "Safe"
    Vivid = "Vivid"


class ContinuousPaletteEnum(Enum):
    """List of possible continuous gradient colors"""

    aggrnyl = "aggrnyl"
    agsunset = "agsunset"
    blackbody = "blackbody"
    bluered = "bluered"
    blues = "blues"
    blugrn = "blugrn"
    bluyl = "bluyl"
    brwnyl = "brwnyl"
    bugn = "bugn"
    bupu = "bupu"
    burg = "burg"
    burgyl = "burgyl"
    cividis = "cividis"
    darkmint = "darkmint"
    electric = "electric"
    emrld = "emrld"
    gnbu = "gnbu"
    greens = "greens"
    greys = "greys"
    hot = "hot"
    inferno = "inferno"
    jet = "jet"
    magenta = "magenta"
    magma = "magma"
    mint = "mint"
    orrd = "orrd"
    oranges = "oranges"
    oryel = "oryel"
    peach = "peach"
    pinkyl = "pinkyl"
    plasma = "plasma"
    plotly3 = "plotly3"
    pubu = "pubu"
    pubugn = "pubugn"
    purd = "purd"
    purp = "purp"
    purples = "purples"
    purpor = "purpor"
    rainbow = "rainbow"
    rdbu = "rdbu"
    rdpu = "rdpu"
    redor = "redor"
    reds = "reds"
    sunset = "sunset"
    sunsetdark = "sunsetdark"
    teal = "teal"
    tealgrn = "tealgrn"
    turbo = "turbo"
    viridis = "viridis"
    ylgn = "ylgn"
    ylgnbu = "ylgnbu"
    ylorbr = "ylorbr"
    ylorrd = "ylorrd"
    algae = "algae"
    amp = "amp"
    deep = "deep"
    dense = "dense"
    gray = "gray"
    haline = "haline"
    ice = "ice"
    matter = "matter"
    solar = "solar"
    speed = "speed"
    tempo = "tempo"
    thermal = "thermal"
    turbid = "turbid"
    armyrose = "armyrose"
    brbg = "brbg"
    earth = "earth"
    fall = "fall"
    geyser = "geyser"
    prgn = "prgn"
    piyg = "piyg"
    picnic = "picnic"
    portland = "portland"
    puor = "puor"
    rdgy = "rdgy"
    rdylbu = "rdylbu"
    rdylgn = "rdylgn"
    spectral = "spectral"
    tealrose = "tealrose"
    temps = "temps"
    tropic = "tropic"
    balance = "balance"
    curl = "curl"
    delta = "delta"
    oxy = "oxy"
    edge = "edge"
    hsv = "hsv"
    icefire = "icefire"
    phase = "phase"
    twilight = "twilight"
    mrybm = "mrybm"
    mygbm = "mygbm"


@dataclass
class Config:
    """Store configurations and provide default values

    Attributes:
        bg_color_default (str): Default value of the background color
        marker_size: The size of all markers
        cross_size: The size of the crosses
        min_value_markerfeat:  The min value of markers size if sizes represent a certain feature value
        max_value_markerfeat:  The max value of markers size if sizes represent a certain feature value
        font_size: The size of fonts
        hull_width: The width of the  the convex hull
        line_width: The width of the regression line
        hull_dash: The dash of the convex hull
        line_dash: The dash of the regression line
        hull_color: The color of the convex hull
        line_color: The color of the regression line
        bg_color: The background color
        bg_toggle (bool): The background color is shown
        color_palette: The color palette used for the initial values
        font_family: The font families
        font_color: The font colors
        featmarker: The feature used for markers size
        featcolor: The feature used for markers color
        featcolor_type: if a feature is used for color this can be 'Gradient' for continuous feature values or 'Discrete'
        featcolor_list: The color palette used for features
    """

    bg_color_default: str = "rgba(229,236,246, 0.5)"
    bg_color: str = "rgba(229, 236, 246, 0.5)"
    bg_toggle: bool = True
    color_palette: DiscretePaletteEnum = DiscretePaletteEnum.Plotly

    marker_size: int = 7
    cross_size: int = 15
    min_value_markerfeat: int = 4
    max_value_markerfeat: int = 20

    font_size: int = 12
    hull_width: int = 1
    line_width: int = 1
    hull_dash: LineTypeEnum = LineTypeEnum.solid
    line_dash: LineTypeEnum = LineTypeEnum.dash
    hull_color: ColorEnum = ColorEnum.Grey
    line_color: ColorEnum = ColorEnum.Black

    font_family: FontFamilyEnum = FontFamilyEnum.Arial
    font_color: ColorEnum = ColorEnum.Black

    featmarker: int = 7
    featcolor: ColorEnum = ColorEnum.Green
    featcolor_type: ColorTypeEnum = ColorTypeEnum.Gradient
    featcolor_list: Union[
        DiscretePaletteEnum, ContinuousPaletteEnum
    ] = ContinuousPaletteEnum.viridis


class ConfigWidgets(object):

    # Default value of the background color
    bg_color_default = "rgba(229,236,246, 0.5)"
    # List of possible marker symbols
    symbols_list = [
        "circle",
        "circle-open",
        "circle-dot",
        "circle-open-dot",
        "circle-cross",
        "circle-x",
        "square",
        "square-open",
        "square-dot",
        "square-open-dot",
        "square-cross",
        "square-x",
        "diamond",
        "diamond-open",
        "diamond-dot",
        "diamond-open-dot",
        "diamond-cross",
        "diamond-x",
        "triangle-up",
        "triangle-up-open",
        "triangle-up-dot",
        "triangle-up-open-dot",
        "triangle-down",
        "triangle-down-open",
        "triangle-down-dot",
        "triangle-down-open-dot",
    ]
    # List of possible colors of the hulls
    color_hull = [
        "Black",
        "Blue",
        "Cyan",
        "Green",
        "Grey",
        "Orange",
        "Red",
        "Yellow",
    ]
    # List of possible colors of the regression line
    color_line = [
        "Black",
        "Blue",
        "Cyan",
        "Green",
        "Grey",
        "Orange",
        "Red",
        "Yellow",
    ]
    # List of possible dash types for the regression line
    line_dashs = ["dash", "solid", "dot", "longdash", "dashdot", "longdashdot"]
    # List of possible dash types for the hulls
    hull_dashs = ["dash", "solid", "dot", "longdash", "dashdot", "longdashdot"]
    # List of possible font families
    font_families = [
        "Arial",
        "Courier New",
        "Helvetica",
        "Open Sans",
        "Times New Roman",
        "Verdana",
    ]
    # List of possible font colors
    font_colors = [
        "Black",
        "Blue",
        "Cyan",
        "Green",
        "Grey",
        "Orange",
        "Red",
        "Yellow",
    ]
    # List of possible discrete palette colors
    discrete_palette_colors = [
        "Plotly",
        "D3",
        "G10",
        "T10",
        "Alphabet",
        "Dark24",
        "Light24",
        "Set1",
        "Pastel1",
        "Dark2",
        "Set2",
        "Pastel2",
        "Set3",
        "Antique",
        "Bold",
        "Pastel",
        "Prism",
        "Safe",
        "Vivid",
    ]
    # List of possible continuous gradient colors
    continuous_gradient_colors = px.colors.named_colorscales()

    # Values below are initialized to a specific value that can be modified using widgets
    hover_features = []
    embedding_features = []
    feat_x = ""
    feat_y = ""
    marker_size = 7  # size of all markers
    cross_size = 15  # size of the crosses
    min_value_markerfeat = (
        4  # min value of markers size if sizes represent a certain feature value
    )
    max_value_markerfeat = (
        20  # max value of markers size if sizes represent a certain feature value
    )

    font_size = 12  # size of fonts
    hull_width = 1  # width of the  the convex hull
    line_width = 1  # width of the regression line
    hull_dash = "solid"  # dash of the convex hull
    line_dash = "dash"  # dash of the regression line
    hull_color = "Grey"  # color of the convex hull
    line_color = "Black"  # color of the regression line
    bg_color = "rgba(229,236,246, 0.5)"  # background color
    bg_toggle = True  # background color is shown
    structures_list = []
    replica_l = 0  # which file in the list is shown in the left visualizer
    replica_r = 0  # which file in the list is shown in the right visualizer
    fract = 1  # fraction of points visualized on the map
    palette = cycle(
        getattr(px.colors.qualitative, discrete_palette_colors[0])
    )  #  color palette used for the initial values
    color_palette = discrete_palette_colors[0]
    font_family = font_families[0]
    font_color = font_colors[0]

    structure_text_l = "..."
    structure_text_r = "..."

    featmarker = "Default size"  # feature used for markers size
    featcolor = "Default color"  # feature used for markers color
    featcolor_type = "Gradient"  # if a feature is used for color this can be 'Gradient' for continuous feature values or 'Discrete'
    featcolor_list = "viridis"  # color palette used for features
