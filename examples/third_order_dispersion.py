from panim import *
import os
import numpy as np

z = np.linspace(-20, 200, 10000)
os.makedirs("plots", exist_ok=True)

# this is just here as an example, but commented out to avoid running it in the pipeline
# for now

# Third order dispersion
# z = np.linspace(-30, 600, 1000)
# p = calc_pulses(
#     z,
#     t_start=0,
#     t_end=2500,
#     n_steps=200,
#     nu_center=0.02,
#     k_i=[1, 3, 2, 6],
#     spec_width=600,
# )
# animate(
#     z,
#     p,
#     ms_between_frames=40,
#     figuresize=(14, 4),
#     saveas="./plots/3rd_order_dispersion.gif",
# )
