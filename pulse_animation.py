import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib import animation
# import scipy.constants as con
from IPython.display import HTML
from tqdm import tqdm
# import matplotlib.cm as cm

c = 1


def n(nu, n0=1, n1=5, n2=0):
    """ calculates the index of refraction as a function of the 
        frequency nu """

    return n0 + n1 * nu + n2 * nu**2


def sin_sum(z_array, t, nu_max=1, nu_min=0.001, N_frequencies=4000, 
            n_i=[1, 5, 0], plotting=False):
    """ calculates the sum of plane waves (sinusoidal signals) over a
        given frequency spectrum """

    # create array of frequency spectrum and the corresponding weight 
    # i.e. how much the given frequency contributes
    frequencies = np.linspace(nu_min, nu_max, N_frequencies)
    spectrum = signal.gaussian(len(frequencies), std=N_frequencies/40) / 1000 * 4

    # create array for spectral components
    E_nu = np.zeros([len(frequencies), len(z_array)])

    n_plotted = 0
    N_spec_plot_tot = 20
    N_spec_plot_min = int(2 * N_frequencies/5)
    N_spec_plot_max = int(3*N_frequencies/5)
    spacing = int(len(frequencies[N_spec_plot_min:N_spec_plot_max]) / N_spec_plot_tot)
    plotting_frequencies = frequencies[N_spec_plot_min: N_spec_plot_max: spacing]
    # colors = cm.rainbow(np.linspace(0, 1, N_spec_plot_tot))

    if plotting:
        fig, ax = plt.subplots(figsize=(11, 4), frameon=False)
        ax.set_xlim(z_array.min(), z_array.max())
        plt.axis('off')

    # now loop over all frequencies and calculate the corresponding spectral
    # component
    for i in range(len(frequencies)):
        phi_nu = 2 * np.pi / c  * frequencies[i] * n(frequencies[i], n_i[0], n_i[1], n_i[2]) * z_array
        E_nu[i, :] = spectrum[i] * np.sin(2 * np.pi * frequencies[i] * t - phi_nu)

        if plotting:
            if frequencies[i] in plotting_frequencies:
                ax.plot(z_array, E_nu[i], label=frequencies[i])  # , color=colors[n_plotted])
                n_plotted += 1

    E = E_nu.sum(axis=0)

    # plot the different spectral components (in the center of the spectrum),
    # the resulting pulse (sum of the spectral components) and the underlying
    # spectrum
    if plotting:
        print("plotted", n_plotted, "frequencies")
        fig.savefig("plots/spectral_components.pdf")

        # now plot the resulting pulse
        fig, ax = plt.subplots(figsize=(11, 4), frameon=False)
        ax.set_xlim(z_array.min(), z_array.max())
        plt.axis('off')
        ax.plot(z_array, E)
        fig.savefig("plots/resulting_pulse.pdf")

        # also plot the spectrum
        fig, ax = plt.subplots(figsize=(6, 4), frameon=False)
        ax.plot(frequencies, spectrum)
        ax.set_xlabel(r"Frequency $\nu$")
        ax.set_ylabel(r"Spectral amplitude $S(\nu)$")
        fig.savefig("plots/spectrum.pdf")

    return E


def animate(z, pulses, ms_between_frames=30, dot_size=0, steps_per_frame=1):
    """ method to animate the particle movement """

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.set_xlim(0, z.max())
    ax.set_ylim(-1, 1)

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


def calc_pulses(z, t_start, t_end, n_steps, nu_max=3, n_i=[1, 3, 0]):
    """ calculate the spatial form of the pulse at different times """

    times = np.linspace(t_start, t_end, n_steps)
    pulses = np.zeros([n_steps, len(z)])
    for i in tqdm(range(len(times))):
        pulses[i, :] = sin_sum(z, times[i], nu_max=nu_max, n_i=n_i)

    return pulses


def plot_pulses(z, times, nu_max=0.5, n_i=[1, 10, 0], no_axes=False, plotname=""):
    """ plots the pulse at different times """

    pulses = [sin_sum(z, t, nu_max=nu_max, n_i=n_i) for t in times]

    fig, ax = plt.subplots(figsize=(11, 4), frameon=False)

    ax.set_xlim(z.min(), z.max())
    ax.set_ylim(pulses[0].min()*1.2, pulses[0].max())

    if no_axes:
        # remove axes and draw arrow in z-direction
        plt.axis('off')
        arrow_coord = (z.mean() - 0.2 * z.mean(), z.mean() + 0.2 * z.mean(), 
                       1.2 * pulses[0].min(), 1.2 * pulses[0].min())
        text_coord  = [z.mean() - 0.1 * z.mean(), z.mean(), 
                       1.1 * pulses[0].min(), 1.1 * pulses[0].min()]
        ax.annotate("", xytext=(arrow_coord[0], arrow_coord[2]), 
                    xy=(arrow_coord[1], arrow_coord[3]),
                    arrowprops=dict(arrowstyle='->'))
        ax.annotate("position $z$", xytext=(text_coord[0], text_coord[2]), 
                    xy=(text_coord[1], text_coord[3]))
    for i in range(len(pulses)):
        ax.plot(z, pulses[i])
        if plotname != "":
            fig.savefig(plotname+"_"+str(i+1)+".pdf")
    plt.show()





