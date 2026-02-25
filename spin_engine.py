"""
Core spin-lattice simulation utilities for classical magnetic models.

Implements minimal yet functional support for Ising, XY, and Heisenberg
models in 2D and 3D with exchange interaction, optional external field,
and uniaxial anisotropy. Designed as a lightweight foundation that can
be extended to the broader research-grade roadmap.

Copyright (c) 2026 Tony Ray Macier III
Licensed under the MIT License - see LICENSE file for details
"""

from __future__ import annotations

import numpy as np


class SpinLattice:
    """Simple nearest-neighbor spin lattice with Metropolis updates."""

    def __init__(
        self,
        L: int,
        dim: int = 2,
        model: str = "ising",
        J: float = 1.0,
        field=0.0,
        anisotropy: float = 0.0,
        anisotropy_axis=None,
        rng=None,
    ):
        if dim not in (2, 3):
            raise ValueError("dim must be 2 or 3")
        if model not in ("ising", "xy", "heisenberg"):
            raise ValueError("model must be 'ising', 'xy', or 'heisenberg'")

        self.L = int(L)
        self.dim = dim
        self.model = model
        self.J = float(J)
        self.spin_components = 1 if model == "ising" else 2 if model == "xy" else 3
        self.rng = rng or np.random.default_rng()

        # External field handling (broadcast scalar to vector if needed)
        field_arr = np.array(field, dtype=float)
        if field_arr.shape == ():  # scalar
            field_arr = np.full(self.spin_components, field_arr.item())
        elif field_arr.size == 1:
            field_arr = np.full(self.spin_components, field_arr.ravel()[0])
        if field_arr.shape[0] != self.spin_components:
            raise ValueError("field must match spin dimensionality")
        self.field = field_arr

        # Uniaxial anisotropy axis (defaults to last component)
        if anisotropy_axis is None:
            axis = np.zeros(self.spin_components)
            axis[-1] = 1.0
        else:
            axis = np.array(anisotropy_axis, dtype=float)
        if axis.shape[0] != self.spin_components:
            raise ValueError("anisotropy_axis must match spin dimensionality")
        # Normalize axis for stable energy evaluation
        norm = np.linalg.norm(axis)
        self.anisotropy_axis = axis / norm if norm != 0 else axis
        self.anisotropy = float(anisotropy)

        self.spins = self._initialize_spins()

    # ------------------------------------------------------------------ #
    # Initialization helpers
    # ------------------------------------------------------------------ #
    def _initialize_spins(self):
        """Initialize spins according to the chosen model."""
        lattice_shape = (self.L,) * self.dim + (self.spin_components,)

        if self.model == "ising":
            return self.rng.choice([-1.0, 1.0], size=lattice_shape)

        if self.model == "xy":
            theta = self.rng.uniform(0, 2 * np.pi, size=(self.L,) * self.dim)
            spins = np.stack((np.cos(theta), np.sin(theta)), axis=-1)
            return spins

        # Heisenberg
        vec = self.rng.normal(size=lattice_shape)
        norm = np.linalg.norm(vec, axis=-1, keepdims=True)
        norm[norm == 0] = 1.0
        return vec / norm

    # ------------------------------------------------------------------ #
    # Energy calculations
    # ------------------------------------------------------------------ #
    def _dot(self, a, b):
        return np.sum(a * b, axis=-1)

    def _neighbor_sum(self, spins):
        """Sum dot products with forward neighbors along each axis."""
        energy = 0.0
        for axis in range(self.dim):
            shifted = np.roll(spins, shift=-1, axis=axis)
            energy += self._dot(spins, shifted)
        return energy

    def total_energy(self) -> float:
        """Compute total Hamiltonian for the lattice."""
        exchange_term = -self.J * np.sum(self._neighbor_sum(self.spins))

        # Zeeman coupling to external field
        field_term = -np.sum(self._dot(self.spins, self.field))

        # Uniaxial anisotropy
        if self.anisotropy != 0.0:
            projection = self._dot(self.spins, self.anisotropy_axis)
            # Easy-axis convention: positive anisotropy favors alignment with axis
            anisotropy_term = -abs(self.anisotropy) * np.sum(projection ** 2)
        else:
            anisotropy_term = 0.0

        return float(exchange_term + field_term + anisotropy_term)

    def _local_energy(self, index) -> float:
        """Energy contribution for a single site (used for Metropolis updates)."""
        s = self.spins[index]

        neighbor_energy = 0.0
        for axis in range(self.dim):
            plus = list(index)
            minus = list(index)
            plus[axis] = (plus[axis] + 1) % self.L
            minus[axis] = (minus[axis] - 1) % self.L
            neighbor_energy += self._dot(s, self.spins[tuple(plus)])
            neighbor_energy += self._dot(s, self.spins[tuple(minus)])

        exchange = -0.5 * self.J * neighbor_energy  # each bond counted twice
        field = -self._dot(s, self.field)
        anis = 0.0
        if self.anisotropy != 0.0:
            proj = self._dot(s, self.anisotropy_axis)
            anis = -abs(self.anisotropy) * (proj ** 2)

        return float(exchange + field + anis)

    # ------------------------------------------------------------------ #
    # Observables
    # ------------------------------------------------------------------ #
    def magnetization(self):
        """Average spin vector (or scalar for Ising)."""
        return np.mean(self.spins, axis=tuple(range(self.dim)))

    # ------------------------------------------------------------------ #
    # Monte Carlo updates
    # ------------------------------------------------------------------ #
    def metropolis_step(self, T: float, sweeps: int = 1):
        """Perform Metropolis updates over the lattice."""
        beta = 1.0 / T
        for _ in range(sweeps):
            for _ in range(self.L ** self.dim):
                # Random site
                idx = tuple(self.rng.integers(0, self.L, size=self.dim))
                old_spin = self.spins[idx].copy()
                E_old = self._local_energy(idx)

                # Propose update
                if self.model == "ising":
                    self.spins[idx] = -old_spin
                else:
                    proposal = self.rng.normal(size=self.spin_components)
                    norm = np.linalg.norm(proposal)
                    if norm != 0:
                        proposal /= norm
                    self.spins[idx] = proposal

                E_new = self._local_energy(idx)
                dE = E_new - E_old

                if dE > 0 and self.rng.random() > np.exp(-beta * dE):
                    # Reject move
                    self.spins[idx] = old_spin


__all__ = ["SpinLattice"]
