"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray


@pytest.fixture
def spatial_axis() -> NDArray[np.floating]:
    """Standard spatial axis for tests."""
    return np.linspace(0, 100, 500)


@pytest.fixture
def short_spatial_axis() -> NDArray[np.floating]:
    """Shorter spatial axis for fast tests."""
    return np.linspace(0, 50, 100)
