import matplotlib
import matplotlib.pyplot as plt
from General.Other import truncate_colormap
import cmocean
import os


def load_style():
# Loading style sheet
    plt.style.use(os.path.join(os.path.dirname(__file__), '_static/style.mplstyle'))

############################################################################ figure properties
######################## sizes
text_width = 426.79 #en pt
fig_width = text_width*0.35136*0.1 # en cm
fig_width = fig_width*0.39 ### inches

fig_width_small = 0.75*fig_width
#
# fig_width_standard = 13.3 # cm
# fig_width_standard = fig_width_standard * 0.39 # inches
#
# fig_width_half = 5.1 ###cm
# fig_width_half = fig_width_half *0.39 ## cm


####################### line width

linewidth_small = 0.8
linewidth_contourplot = 0.5
linewidth_barscale = 2
linewidth_errorbar = 0.8

###################### Markers
markersize = 5
markersize_small = 2

###################### Cmaps
copper_t = truncate_colormap(plt.get_cmap("copper"), 0.2, 1)
# copper_t.set_under((0.4392156862745098, 0.5019607843137255, 0.5647058823529412, 0.7))
copper_t.set_under((0.6074509803921568, 0.6513725490196078, 0.6952941176470588, 1.0))

####################### Stability maps
# cmap_growth_rate = plt.cm.get_cmap('BrBG_r')
cmap_growth_rate = truncate_colormap(cmocean.cm.delta_r, 0.2, 0.8)
# cmap_growth_rate = truncate_colormap(cmocean.cm.delta_r, 0, 1)
color_max = '#ff7f0e'

##################### Windrose color
wind_grid_color = 'k'
flux_cmap = matplotlib.colors.ListedColormap('navajowhite')

wind_color = 'blanchedalmond'
color_rose = 'peru'
color_point = 'k'
alpha_bg = 0.25
color_resultant_flux = 'saddlebrown'

##################### line colors
# color_BI = 'darkviolet'
color_BI = 'mediumblue'
# color_F = 'deeppink'
color_F = 'crimson'
color_point = 'k'
color_ava_slope = 'lime'
color_th = 'crimson'


#################### Sketch colors
color_dune = '#D2691E'
alpha_dune = 0.2
flow_color = 'powderblue'

##### Arrow properties
lw_arrow = 1.5

#### font properties
fontsize_small = 9
fontsize_usual = matplotlib.rcParams['font.size']

#### color Rescal
Color_rescal = {'DUM': (127, 127, 127), 'GR': (64, 0, 0), 'IN': (255, 255, 255), 'OUT': (), 'AIR': (0, 255, 255)}
