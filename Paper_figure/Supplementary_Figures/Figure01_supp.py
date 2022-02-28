"""
============================
Figure 1 -- Online Resource
============================

"""

import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
sys.path.append('../../')
import python_codes.theme as theme

# Loading figure theme
theme.load_style()


# paths
path_savefig = '../../Paper/Figures'
path_images = '../../static/images'

# images
list_images = sorted(glob.glob(os.path.join(path_images, '*+*')))
order_plot = [6, 4, 5, 2, 1]
labels = [r'\textbf{a}', r'\textbf{b}', r'\textbf{c}', r'\textbf{d}', r'\textbf{e}']

axd = plt.figure(constrained_layout=True,
                 figsize=(theme.fig_width, 0.7*theme.fig_height_max)).subplot_mosaic(
    """
    AABB
    CCDD
    .EE.
    """,
    gridspec_kw={'height_ratios': (1, 1.2, 1)}
)

for ax_key, i, label in zip(axd.keys(), order_plot, labels):
    axd[ax_key].imshow(np.array(Image.open(list_images[i])))
    axd[ax_key].set_axis_off()
    axd[ax_key].text(0.02, 0.98, label, ha='left', va='top', transform=axd[ax_key].transAxes)

plt.savefig(os.path.join(path_savefig, 'Figure1_supp.pdf'), dpi=400)
plt.show()
