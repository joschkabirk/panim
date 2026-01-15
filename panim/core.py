"""Core physics functions for pulse simulation.

This module contains the fundamental physics calculations for modeling
light pulses as sums of spectral components with frequency-dependent
wave vectors.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.signal import windows
from tqdm import tqdm

if TYPE_CHECKING:
    from collections.abc import Sequence

# Speed of light (normalized to 1 for simulations)
c: float = 1.0


def wave_vector(
    nu: float | NDArray[np.floating],
    nu_center: float,
    k_0: float = 1.0,
    k_1: float = 0.0,
    k_2: float = 0.0,
    k_3: float = 0.0,
) -> float | NDArray[np.floating]:
    """Calculate the wave vector k as a function of frequency.

    Uses Taylor expansion: k(nu) = k_0 + k_1*(omega-omega_0) + k_2*(omega-omega_0)^2 + ...

    Parameters
    ----------
    nu : float or array_like
        Frequency at which to calculate the wave vector.
    nu_center : float
        Center frequency of the spectrum.
    k_0 : float, optional
        Zero-order term (constant phase). Default is 1.0.
    k_1 : float, optional
        First-order derivative dk/d(omega), related to group velocity.
        Default is 0.0.
    k_2 : float, optional
        Second-order derivative d^2k/d(omega)^2, group velocity dispersion.
        Default is 0.0.
    k_3 : float, optional
        Third-order derivative d^3k/d(omega)^3. Default is 0.0.

    Returns
    -------
    k : float or ndarray
        Wave vector k(omega) at the given frequency.

    Examples
    --------
    >>> wave_vector(1.0, 1.0, k_0=1, k_1=5)
    1.0
    >>> wave_vector(1.5, 1.0, k_0=1, k_1=5)  # doctest: +ELLIPSIS
    16.707...
    """
    omega = 2 * np.pi * nu
    omega_0 = 2 * np.pi * nu_center
    delta_omega = omega - omega_0

    return k_0 + k_1 * delta_omega + k_2 * delta_omega**2 + k_3 * delta_omega**3


def compute_spectral_field(
    z: NDArray[np.floating],
    t: float,
    nu_center: float = 1.0,
    nu_min: float = 0.001,
    n_frequencies: int = 4000,
    spec_width: float = 200.0,
    k_coefficients: Sequence[float] | None = None,
) -> NDArray[np.floating]:
    """Compute the electric field as a sum of spectral components.

    Calculates the sum of plane waves (sinusoidal signals) over a given
    frequency spectrum with Gaussian weighting.

    Parameters
    ----------
    z : ndarray
        Spatial coordinate array (propagation axis).
    t : float
        Time at which to calculate the field snapshot.
    nu_center : float, optional
        Center frequency of the spectrum. Default is 1.0.
    nu_min : float, optional
        Minimum frequency in the spectrum. Default is 0.001.
    n_frequencies : int, optional
        Number of frequency components. Default is 4000.
    spec_width : float, optional
        Standard deviation of the Gaussian spectral envelope.
        Default is 200.0.
    k_coefficients : sequence of float, optional
        Coefficients [k_0, k_1, k_2, k_3] for the wave vector expansion.
        Default is [1.0, 5.0, 0.0].

    Returns
    -------
    E_field : ndarray
        Electric field amplitude along the z-axis at time t.

    See Also
    --------
    wave_vector : Compute wave vector from frequency.
    calc_pulses : Calculate field evolution over multiple time steps.
    """
    if k_coefficients is None:
        k_coefficients = [1.0, 5.0, 0.0]

    # Pad k_coefficients to length 4
    k_i = list(k_coefficients) + [0.0] * (4 - len(k_coefficients))

    # Create frequency array and Gaussian spectral envelope
    frequencies = np.linspace(nu_min, nu_center * 2, n_frequencies)
    spectrum = windows.gaussian(len(frequencies), std=spec_width)

    # Compute spectral components
    E_field_components = np.zeros((len(frequencies), len(z)))

    for i, freq in enumerate(frequencies):
        phi = wave_vector(freq, nu_center, *k_i[:4]) * z
        E_field_components[i, :] = spectrum[i] * np.sin(2 * np.pi * freq * t - phi)

    result: NDArray[np.floating] = E_field_components.sum(axis=0)
    return result


def calc_pulses(
    z: ArrayLike,
    t_start: float,
    t_end: float,
    n_steps: int,
    nu_center: float = 1.0,
    k_i: Sequence[float] | None = None,
    spec_width: float = 100.0,
    *,
    show_progress: bool = True,
) -> NDArray[np.floating]:
    """Calculate the spatial pulse form at multiple time steps.

    Parameters
    ----------
    z : array_like
        Spatial coordinate array (propagation axis).
    t_start : float
        Start time of the simulation.
    t_end : float
        End time of the simulation.
    n_steps : int
        Number of time steps to calculate.
    nu_center : float, optional
        Center frequency of the spectrum. Default is 1.0.
    k_i : sequence of float, optional
        Wave vector coefficients [k_0, k_1, k_2, ...]. Default is [1, 5, 0].
    spec_width : float, optional
        Spectral width parameter. Default is 100.0.
    show_progress : bool, optional
        Whether to show a progress bar. Default is True.

    Returns
    -------
    pulses : ndarray
        Array of shape (n_steps, len(z)) containing the electric field
        at each time step.

    Examples
    --------
    >>> import numpy as np
    >>> z = np.linspace(0, 100, 500)
    >>> pulses = calc_pulses(z, 0, 10, 5, show_progress=False)
    >>> pulses.shape
    (5, 500)
    """
    if k_i is None:
        k_i = [1.0, 5.0, 0.0]

    z_arr = np.asarray(z)
    times = np.linspace(t_start, t_end, n_steps)
    pulses = np.zeros((n_steps, len(z_arr)))

    iterator = tqdm(range(n_steps)) if show_progress else range(n_steps)
    for i in iterator:
        pulses[i, :] = compute_spectral_field(
            z_arr,
            times[i],
            nu_center=nu_center,
            k_coefficients=k_i,
            spec_width=spec_width,
        )

    return pulses
