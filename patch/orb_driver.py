"""
Copyright (c) 2023, AdvanceSoft Corp.
Copyright (c) 2024, Stefan Bringuier <stefanbringuier@gmail.com>

This source code is licensed under the GNU General Public License Version 2
found in the LICENSE file in the root directory of this source tree.
"""

from ase import Atoms
from orb_models.forcefield import pretrained
from orb_models.forcefield.calculator import ORBCalculator


import torch

def orb_initialize(model_name = None, gpu = False, cutoff=4.0):
    """
    Initialize Orb models: https://github.com/orbital-materials/orb-models
    Args:
        model_name (str): name of model for GNNP.
        gpu (bool): using GPU, if possible.
    Returns:
        cutoff: cutoff radius.

    Note:
        The cutoff from ORBCalculator is not available.
    """

    # Get Orb model
    if model_name is not None:
        orbff = pretrained.ORB_PRETRAINED_MODELS[model_name]()
    else:
        orbff = pretrained.orb_v2()
   
    #  Assign Calculator and Device Type
    global calculator
    if gpu and torch.cuda.is_available():
        calculator = ORBCalculator(orbff,device="cuda")
    else:
        calculator = ORBCalculator(orbff,device="cpu")

    global aseAtoms

    aseAtoms = None

    # Orb Model isn't providing cutoff
    #cutoff = calculator.model.cutoff
    return cutoff

def orb_get_energy_forces_stress(cell, atomic_numbers, positions):
    """
    Predict total energy, atomic forces and stress w/ pre-trained Orb Model
    Args:
        cell: lattice vectors in angstroms.
        atomic_numbers: atomic numbers for all atoms.
        positions: xyz coordinates for all atoms in angstroms.
    Returns:
        energy:  total energy.
        forcces: atomic forces.
        stress:  stress tensor (Voigt order).

    NOTES:
    - Assumes PBC is always True. This should eventually be changed so that this function takes LAMMPS cell and BC.
    """

    # Initialize Atoms
    global aseAtoms
    global calculator

    if aseAtoms is not None and len(aseAtoms.numbers) != len(atomic_numbers):
        aseAtoms = None

    if aseAtoms is None:
        aseAtoms = Atoms(
            numbers   = atomic_numbers,
            positions = positions,
            cell      = cell,
            pbc       = [True, True, True]
        )

        aseAtoms.calc = calculator

    else:
        aseAtoms.set_cell(cell)
        aseAtoms.set_atomic_numbers(atomic_numbers)
        aseAtoms.set_positions(positions)

    energy = aseAtoms.get_potential_energy()
    if not isinstance(energy, float):
        energy = energy.item()

    forces = aseAtoms.get_forces().tolist()

    stress = aseAtoms.get_stress().tolist()

    return energy, forces, stress
