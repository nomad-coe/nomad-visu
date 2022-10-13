import plotly.express as px
from itertools import cycle

class ConfigWidgets(object):

    # Default value of the background color
    bg_color_default = (
        "rgba(229,236,246, 0.5)"
    )
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
    bg_color = (
        "rgba(229,236,246, 0.5)"  # background color 
    )  
    bg_toggle = True  # background color is shown
    structures_list = []
    replica_l = 0    # which file in the list is shown in the left visualizer
    replica_r = 0    # which file in the list is shown in the right visualizer
    fract = 1 # fraction of points visualized on the map
    palette = cycle(getattr(px.colors.qualitative, discrete_palette_colors[0])) #  color palette used for the initial values
    color_palette = discrete_palette_colors[0] 
    font_family = font_families[0]
    font_color = font_colors[0]

    structure_text_l = '...'
    structure_text_r = '...'

    featmarker = 'Default size' # feature used for markers size
    featcolor =  'Default color' # feature used for markers color
    featcolor_type = 'Gradient' # if a feature is used for color this can be 'Gradient' for continuous feature values or 'Discrete'
    featcolor_list = 'viridis' # color palette used for features




