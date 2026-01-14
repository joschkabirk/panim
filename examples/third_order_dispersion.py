"""Third order dispersion example.

This is commented out to avoid running it in the CI pipeline as it's slow.
"""

from pathlib import Path

Path("plots").mkdir(exist_ok=True)

# Third order dispersion - commented out to avoid slow CI runs
# from panim import animate, calc_pulses
#
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
#     fps=15,
#     figuresize=(14, 4),
#     saveas="./plots/third_order_dispersion.gif",
# )
