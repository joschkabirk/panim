import matplotlib
import numpy as np
from pulse_animation import animate_with_time, calc_pulses

matplotlib.rcParams.update({"font.size": 13})

z = np.linspace(0, 350, 500)
p = calc_pulses(
    z,
    t_start=-1000,
    t_end=5000,
    n_steps=400,
    nu_center=0.02,
    k_i=[10 * 2 * np.pi * 0.02, 10, 20, 0],
    spec_width=500,
)

animate_with_time(
    z,
    p,
    fixed_z_1=0,
    fixed_z_2=499,
    figuresize=(14, 10),
    ms_between_frames=40,
    saveas="./optical_fibre.mp4",
    z_offset=30,
)
