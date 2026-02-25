import numpy as np
import pytest

from spin_engine import SpinLattice


def test_ising_2d_ground_state_energy():
    """All-aligned 2D Ising spins should have minimal exchange energy."""
    lattice = SpinLattice(L=2, dim=2, model="ising", J=1.0, field=0.0, rng=np.random.default_rng(0))
    lattice.spins[:] = 1.0  # deterministic ferromagnetic state

    energy = lattice.total_energy()

    # For L=2 with periodic boundaries: 8 unique bonds, each contributes -J
    assert energy == pytest.approx(-8.0)


def test_ising_with_field_prefers_alignment():
    """External field should bias spins to align and lower energy."""
    lattice = SpinLattice(L=2, dim=2, model="ising", J=0.0, field=0.5, rng=np.random.default_rng(1))
    lattice.spins[:] = 1.0
    energy_aligned = lattice.total_energy()

    lattice.spins[:] = -1.0
    energy_antialigned = lattice.total_energy()

    assert energy_aligned < energy_antialigned


def test_xy_magnetization_shape():
    """Magnetization for XY model should be 2-component vector."""
    lattice = SpinLattice(L=3, dim=2, model="xy", rng=np.random.default_rng(2))
    mag = lattice.magnetization()

    assert mag.shape == (2,)
    assert np.isfinite(mag).all()


def test_heisenberg_3d_local_update_changes_spin():
    """Metropolis step should update spins without breaking normalization."""
    lattice = SpinLattice(L=2, dim=3, model="heisenberg", rng=np.random.default_rng(3))
    before = lattice.spins.copy()

    lattice.metropolis_step(T=2.5, sweeps=1)

    assert not np.allclose(before, lattice.spins)
    norms = np.linalg.norm(lattice.spins, axis=-1)
    assert np.allclose(norms, 1.0, atol=1e-6)


def test_anisotropy_penalizes_transverse_components():
    """Uniaxial anisotropy should increase energy for off-axis spins."""
    axis = np.array([0.0, 0.0, 1.0])
    lattice = SpinLattice(
        L=1,
        dim=3,
        model="heisenberg",
        J=0.0,
        anisotropy=2.0,
        anisotropy_axis=axis,
        rng=np.random.default_rng(4),
    )
    lattice.spins[:] = np.array([1.0, 0.0, 0.0])  # perpendicular to axis
    energy_transverse = lattice.total_energy()

    lattice.spins[:] = np.array([0.0, 0.0, 1.0])  # aligned with axis
    energy_aligned = lattice.total_energy()

    assert energy_aligned < energy_transverse
