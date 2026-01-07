import matplotlib.pyplot as plt
import numpy as np

# import scipy.constants as con
from IPython.display import HTML

# from scipy import signal
from matplotlib import animation
from tqdm import tqdm

# import matplotlib.cm as cm

c = 1


def resonator_modes(
    t,
    z,
    n_modes=3,
    random_phases=False,
    plot=True,
    figuresize=(10, 4),
    spectrum_std=1000,
    save_in="",
):
    # length of the resonator
    L = z.max() - z.min()
    # calculate the frequency difference between two neighbouring modes of
    # the resonator
    delta_nu = c / (2 * L)
    frequencies = np.array([delta_nu * i for i in range(1, n_modes + 1)])

    phases = np.zeros(n_modes)
    if random_phases is True:
        phases = np.random.uniform(0, 200, n_modes)

    # spectrum = signal.gaussian(n_modes, std=spectrum_std)
    spectrum = np.ones(n_modes)

    if plot is True:
        fig, axs = plt.subplots(2, 1, figsize=figuresize, dpi=100, frameon=False)
        axs[0].axis("off")
        axs[1].axis("off")
        axs.flatten()
        axs[0].set_xlim(z.min(), z.max())
        axs[1].set_xlim(z.min(), z.max())
        # axs[2].plot(frequencies, spectrum)

    # calculate the sum...
    E_i = np.zeros([n_modes, len(z)])

    for i in range(n_modes):
        omega = 2 * np.pi * frequencies[i]
        k = omega / c
        E_i[i, :] = spectrum[i] * np.sin(2 * omega * t - phases[i]) * np.sin(k * z)

        if plot is True:
            fig_2, ax2 = plt.subplots(figsize=(10, 2), dpi=100, frameon=False)
            ax2.set_ylim(-1.1, 1.1)
            ax2.axis("off")
            ax2.plot(z, E_i[i])
            axs[0].plot(z, E_i[i], label=str(i))

            if save_in != "":
                fig_2.savefig(save_in + "_mode_" + str(i) + ".pdf")
                plt.close()
            else:
                pass

    if plot is True:
        E_total = np.sum(E_i, axis=0)
        maximum = np.max(np.abs(E_total))
        axs[1].set_ylim(-1.2 * maximum, 1.2 * maximum)
        # axs[0].legend()
        axs[1].plot(z, E_total)

        fig_3, ax3 = plt.subplots(figsize=(10, 2), dpi=100, frameon=False)
        ax3.axis("off")
        ax3.plot(z, E_total)
        if save_in != "":
            fig.savefig(save_in + "_both.pdf")
            fig_3.savefig(save_in + "_sum.pdf")
            plt.close()
        else:
            pass

    return E_i


def animate_resonator(
    z, times, n_modes, ms_between_frames=60, figuresize=(11, 4), saveas=""
):
    """Animates the time evolution of the wave packet

    Parameters
    ----------
    z : array_like
        Array of the z-axis your wave packet is propagating on.
    times : array_like
        Times you want to include in the animation.
    n_modes: int
        Number of modes included in the calculation.
    ms_between_frames : int, optional
        Milliseconds of pause between two frames in the animation. Default
        is 30.
    figuresize : tuple of ints, optional
        Size of the figure when plotting the wave. Default is (11, 4).
    saveas : string, optional
        Path where you want to save the animation as .gif-file.

    """

    modes = [resonator_modes(t, z, n_modes, plot=False) for t in tqdm(times)]
    pulses = [E_i.sum(axis=0) for E_i in tqdm(modes)]

    fig, ax = plt.subplots(figsize=figuresize)

    ax.set_xlim(z.min(), z.max())
    maximum = np.max(np.abs(np.array(pulses)))
    ax.set_ylim(-1.2 * maximum, 1.2 * maximum)

    ax.set_xlabel(r"position $z$")

    lines = [ax.plot([], [], color="forestgreen")[0] for i in pulses]

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        for j in range(len(lines)):
            lines[j].set_data(z, pulses[i])
        return lines

    plt.close()
    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        blit=True,
        frames=len(pulses),
        interval=ms_between_frames,
    )
    if saveas != "":
        anim.save(saveas, writer="imagemagick", fps=int(1000 / ms_between_frames))

    return HTML(anim.to_html5_video())
