import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib import animation
# import scipy.constants as con
from IPython.display import HTML
from tqdm import tqdm
# import matplotlib.cm as cm

c = 1


def k(nu, k0=1, k1=0, k2=0):
    """ calculates the wave vector k as a function of the frequency nu """

    omega = 2 * np.pi * nu

    return k0 + k1 * omega + k2 * omega**2


def sin_sum(z, t, nu_center=1, nu_min=0.001, N_frequencies=4000, 
            k_i=[1, 5, 0], plotting=False, figuresize=(11, 4), spec_width=200):
    """ calculates the sum of plane waves (sinusoidal signals) over a
        given frequency spectrum """

    # create array of frequency spectrum and the corresponding weight 
    # i.e. how much the given frequency contributes
    frequencies = np.linspace(nu_min, nu_center * 2, N_frequencies)
    spectrum = signal.gaussian(len(frequencies), std=spec_width) / 1000 * 4

    # create array for spectral components
    E_nu = np.zeros([len(frequencies), len(z)])

    n_plotted = 0
    N_spec_plot_tot = 20
    N_spec_plot_min = int(2 * N_frequencies/5)
    N_spec_plot_max = int(3*N_frequencies/5)
    spacing = int(len(frequencies[N_spec_plot_min:N_spec_plot_max]) / N_spec_plot_tot)
    plotting_frequencies = frequencies[N_spec_plot_min: N_spec_plot_max: spacing]
    # colors = cm.rainbow(np.linspace(0, 1, N_spec_plot_tot))

    if plotting:
        fig, ax = plt.subplots(figsize=figuresize, frameon=False)
        ax.set_xlim(z.min(), z.max())
        plt.axis('off')

    # now loop over all frequencies and calculate the corresponding spectral
    # component
    for i in range(len(frequencies)):
        phi_nu = k(frequencies[i], *k_i) * z
        E_nu[i, :] = spectrum[i] * np.sin(2 * np.pi * frequencies[i] * t - phi_nu)

        if plotting:
            if frequencies[i] in plotting_frequencies:
                ax.plot(z, E_nu[i], label=frequencies[i])  # , color=colors[n_plotted])
                n_plotted += 1

    E = E_nu.sum(axis=0)

    # plot the different spectral components (in the center of the spectrum),
    # the resulting pulse (sum of the spectral components) and the underlying
    # spectrum
    if plotting:
        ymin = E_nu.min() * 2
        ymax = E_nu.max() * 1.5
        ax.set_ylim(ymin, ymax)
        delta_z = z.max() - z.min()
        arrow_coord = (z.mean() - 0.1 * delta_z, z.mean() + 0.1 * delta_z,
                       ymin, ymin)
        text_coord  = [z.mean() - 0.03 * delta_z, z.mean(), 
                       0.9 * ymin, 0.9 * ymin]
        ax.annotate("", xytext=(arrow_coord[0], arrow_coord[2]), 
                    xy=(arrow_coord[1], arrow_coord[3]),
                    arrowprops=dict(arrowstyle='->'))
        ax.annotate("position $z$", xytext=(text_coord[0], text_coord[2]), 
                    xy=(text_coord[1], text_coord[3]))
        print("plotted", n_plotted, "frequencies")
        plt.show()
        fig.savefig("plots/spectral_components.pdf")

        # now plot the resulting pulse
        fig, ax = plt.subplots(figsize=figuresize, frameon=False)
        ax.set_xlim(z.min(), z.max())
        plt.axis('off')
        ymin = E.min() * 2
        ymax = E.max()
        ax.set_ylim(ymin, ymax)
        delta_z = z.max() - z.min()
        arrow_coord = (z.mean() - 0.1 * delta_z, z.mean() + 0.1 * delta_z,
                       ymin, ymin)
        text_coord  = [z.mean() - 0.03 * delta_z, z.mean(), 
                       0.9 * ymin, 0.9 * ymin]
        ax.annotate("", xytext=(arrow_coord[0], arrow_coord[2]), 
                    xy=(arrow_coord[1], arrow_coord[3]),
                    arrowprops=dict(arrowstyle='->'))
        ax.annotate("position $z$", xytext=(text_coord[0], text_coord[2]), 
                    xy=(text_coord[1], text_coord[3]))
        ax.plot(z, E)
        fig.savefig("plots/resulting_pulse.pdf")

        # also plot the spectrum
        fig, ax = plt.subplots(figsize=(6, 4), frameon=False)
        ax.plot(frequencies, spectrum)
        ax.set_xlabel(r"Frequency $\nu$")
        ax.set_ylabel(r"Spectral amplitude $S(\nu)$")
        fig.savefig("plots/spectrum.pdf")

    return E


def animate(z, pulses, ms_between_frames=30, dot_size=0, steps_per_frame=1,
            figuresize=(7, 4)):
    """ method to animate the time evolution of the wave packet """

    fig, ax = plt.subplots(figsize=figuresize)

    ax.set_xlim(z.min(), z.max())
    ax.set_ylim(1.2 * pulses.min(), 1.2 * pulses.max())

    ax.set_xlabel(r"position $z$")

    lines = [ax.plot([], [], color="forestgreen")[0]
             for i in pulses]

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        for j in range(len(lines)):
            lines[j].set_data(z, pulses[i, :])
        return lines

    plt.close()
    anim = animation.FuncAnimation(fig, animate, init_func=init, blit=True,
                                   frames=len(pulses), 
                                   interval=ms_between_frames)
    # Writer = animation.writers['ffmpeg']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    # anim.save("animation.mp4", writer=writer)
    return HTML(anim.to_html5_video())


def calc_pulses(z, t_start, t_end, n_steps, nu_center=3, k_i=[1, 3, 0],
                spec_width=30):
    """ calculate the spatial form of the pulse at different times """

    times = np.linspace(t_start, t_end, n_steps)
    pulses = np.zeros([n_steps, len(z)])
    for i in tqdm(range(len(times))):
        pulses[i, :] = sin_sum(z, times[i], nu_center=nu_center, k_i=k_i,
                               spec_width=spec_width)

    return pulses


def plot_pulses(z, times, nu_center=0.5, k_i=[1, 10, 0], no_axes=False, 
                plotname="", dpi=100, figuresize=(11, 4), z_arrow=False,
                colors=["steelblue" for i in range(10)], spec_width=400):
    """ plots the pulse at different times """

    pulses = [sin_sum(z, t, nu_center=nu_center, k_i=k_i, spec_width=spec_width) for t in times]

    fig, ax = plt.subplots(figsize=figuresize, dpi=dpi, frameon=False)

    ax.set_xlim(z.min(), z.max())
    ymax = pulses[0].max()
    ymin = pulses[0].min()
    if z_arrow:
        ymin *= 2
    ax.set_ylim(ymin, ymax)

    if no_axes:
        # remove axes and draw arrow in z-direction
        plt.axis('off')
        if z_arrow:
            arrow_coord = (z.mean() - 0.2 * z.mean(), z.mean() + 0.2 * z.mean(), 
                           ymin, ymin)
            text_coord  = [z.mean() - 0.1 * z.mean(), z.mean(), 
                           0.9 * ymin, 0.9 * ymin]
            ax.annotate("", xytext=(arrow_coord[0], arrow_coord[2]), 
                        xy=(arrow_coord[1], arrow_coord[3]),
                        arrowprops=dict(arrowstyle='->'))
            ax.annotate("position $z$", xytext=(text_coord[0], text_coord[2]), 
                        xy=(text_coord[1], text_coord[3]))
    for i in range(len(pulses)):
        ax.plot(z, pulses[i], color=colors[i])
        if plotname != "":
            if len(pulses) > 1:
                fig.savefig(plotname+"_"+str(i+1)+".pdf")
            else:
                fig.savefig(plotname+".pdf")
    plt.show()





