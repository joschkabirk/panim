# Simulating light pulses in an optical fiber

The repository contains some simple python code to visualise the construction 
and the propagation of light pulses.
The code uses a method that aims be a good approximation to the 
Fourier transformation.

You start with defining a frequency spectrum of the pulse you want to visualise.
Afterwards, the code constructs the spectral components of the pulse according
to the frequency spectrum you defined. This means that the final pulse is the 
sum of all the spectral components. The spectral components are just sinusoidal
waves with the corresponding frequency. In order to visualise the propagation 
of such a pulse, the wave vector `k` is calculated as a function of the
frequency `k(ν)`. 

    k(ν) = k(ν0) + k'(ν0) * (ν - ν0) + 1 / 2 * k''(ν0) * (ν - ν0) **2 + ...

This allows to visualise different effects that occur when
propagating the pulse along a z-axis.

## Phase velocity and group velocity

If the refractive index is the same for all frequencies, then the wave vector
`k(ν)` has to fulfill the equations

    k(ν0) = k'(ν0) * ν0 ,  k'(ν0) = n / c_0

where `n` is the refractive index and `c_0` the speed of light in vacuum. The
resulting propagation looks like this

![](animations/group_equal_phase.gif)

which means that phase velocity and group velocity are the same here.


## Group delay

Group delay in general is the derivative `dφ/dω`, which means that the first 
derivative `k'(ν0)` is non-zero. This was also the case in the above animation,
but if `k(ν0)` and `k'(ν0)` do not fulfill the conditions as in the above 
example, the phase velocity and the group velocity differ.
Assuming that all higher order derivatives vanish, the resulting
propagation looks like this:

![](animations/group_delay.gif)


## Group velocity dispersion

If also the second derivative is non-zero, then group velocity dispersion
occurs, resulting in a linear frequency chirp of the pulse:

![](animations/group_velocity_dispersion.gif)

