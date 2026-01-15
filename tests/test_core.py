"""Tests for core physics functions."""

from __future__ import annotations

import numpy as np

from panim import calc_pulses, compute_spectral_field, wave_vector


class TestWaveVector:
    """Tests for wave_vector function."""

    def test_zero_order_only(self) -> None:
        """Wave vector with only k_0 is constant."""
        result = wave_vector(1.0, 1.0, k_0=5.0)
        assert result == 5.0

    def test_at_center_frequency(self) -> None:
        """At center frequency, only k_0 contributes."""
        result = wave_vector(1.0, 1.0, k_0=1.0, k_1=10.0, k_2=5.0)
        assert result == 1.0

    def test_first_order(self) -> None:
        """First order term scales linearly with frequency deviation."""
        nu_center = 1.0
        k_1 = 5.0
        delta_nu = 0.5

        result = wave_vector(nu_center + delta_nu, nu_center, k_0=0, k_1=k_1)
        expected = k_1 * 2 * np.pi * delta_nu
        assert np.isclose(result, expected)

    def test_array_input(self) -> None:
        """Function works with array inputs."""
        nu = np.array([0.5, 1.0, 1.5])
        result = wave_vector(nu, 1.0, k_0=1.0)
        assert isinstance(result, np.ndarray)
        assert result.shape == (3,)
        assert result[1] == 1.0  # At center frequency


class TestComputeSpectralField:
    """Tests for compute_spectral_field function."""

    def test_output_shape(self, short_spatial_axis: np.ndarray) -> None:
        """Output has same shape as input z array."""
        result = compute_spectral_field(short_spatial_axis, t=0)
        assert result.shape == short_spatial_axis.shape

    def test_returns_array(self, short_spatial_axis: np.ndarray) -> None:
        """Function returns numpy array."""
        result = compute_spectral_field(short_spatial_axis, t=0)
        assert isinstance(result, np.ndarray)

    def test_different_times_give_different_results(
        self, short_spatial_axis: np.ndarray
    ) -> None:
        """Field at different times should differ."""
        result_t0 = compute_spectral_field(short_spatial_axis, t=0, n_frequencies=100)
        result_t1 = compute_spectral_field(short_spatial_axis, t=10, n_frequencies=100)
        assert not np.allclose(result_t0, result_t1)

    def test_custom_k_coefficients(self, short_spatial_axis: np.ndarray) -> None:
        """Custom k coefficients affect the result."""
        k1 = [1.0, 5.0, 0.0]
        k2 = [1.0, 10.0, 0.0]

        result1 = compute_spectral_field(
            short_spatial_axis, t=5, k_coefficients=k1, n_frequencies=100
        )
        result2 = compute_spectral_field(
            short_spatial_axis, t=5, k_coefficients=k2, n_frequencies=100
        )
        assert not np.allclose(result1, result2)


class TestCalcPulses:
    """Tests for calc_pulses function."""

    def test_output_shape(self, short_spatial_axis: np.ndarray) -> None:
        """Output has correct shape (n_steps, len(z))."""
        n_steps = 10
        result = calc_pulses(short_spatial_axis, 0, 10, n_steps, show_progress=False)
        assert result.shape == (n_steps, len(short_spatial_axis))

    def test_first_step_matches_compute_spectral_field(
        self, short_spatial_axis: np.ndarray
    ) -> None:
        """First time step should match direct computation."""
        t_start = 0
        k_i = [1.0, 5.0, 0.0]
        spec_width = 100.0

        pulses = calc_pulses(
            short_spatial_axis,
            t_start,
            10,
            n_steps=5,
            k_i=k_i,
            spec_width=spec_width,
            show_progress=False,
        )

        direct = compute_spectral_field(
            short_spatial_axis,
            t_start,
            k_coefficients=k_i,
            spec_width=spec_width,
        )

        assert np.allclose(pulses[0], direct)

    def test_progress_bar_can_be_disabled(self, short_spatial_axis: np.ndarray) -> None:
        """Function runs without progress bar when disabled."""
        # Should not raise
        result = calc_pulses(short_spatial_axis, 0, 5, 3, show_progress=False)
        assert result.shape[0] == 3
