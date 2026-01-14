"""Tests for resonator functions."""

from __future__ import annotations

import numpy as np

from panim import resonator_modes


class TestResonatorModes:
    """Tests for resonator_modes function."""

    def test_output_shape(self, short_spatial_axis: np.ndarray) -> None:
        """Output has correct shape (n_modes, len(z))."""
        n_modes = 5
        result = resonator_modes(t=0, z=short_spatial_axis, n_modes=n_modes, plot=False)
        assert result.shape == (n_modes, len(short_spatial_axis))

    def test_single_mode(self, short_spatial_axis: np.ndarray) -> None:
        """Single mode returns array with one row."""
        result = resonator_modes(t=0, z=short_spatial_axis, n_modes=1, plot=False)
        assert result.shape == (1, len(short_spatial_axis))

    def test_random_phases_changes_result(self, short_spatial_axis: np.ndarray) -> None:
        """Random phases produce different results each time."""
        np.random.seed(42)
        result1 = resonator_modes(
            t=0, z=short_spatial_axis, n_modes=3, random_phases=True, plot=False
        )
        np.random.seed(123)
        result2 = resonator_modes(
            t=0, z=short_spatial_axis, n_modes=3, random_phases=True, plot=False
        )
        assert not np.allclose(result1, result2)

    def test_fixed_phases_reproducible(self, short_spatial_axis: np.ndarray) -> None:
        """Without random phases, results are reproducible."""
        result1 = resonator_modes(
            t=0, z=short_spatial_axis, n_modes=3, random_phases=False, plot=False
        )
        result2 = resonator_modes(
            t=0, z=short_spatial_axis, n_modes=3, random_phases=False, plot=False
        )
        assert np.allclose(result1, result2)
