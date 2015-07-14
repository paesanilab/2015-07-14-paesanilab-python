#!/usr/bin/env python
from __future__ import print_function

import mbpol
import os
import sys

import simtk.openmm as mm
from simtk import unit

try: # support for python 2
    from exceptions import ImportError
except:
    pass

simulation_name = "water14_cluster"
pdb = mm.app.PDBFile("water14_cluster.pdb")
forcefield = mm.app.ForceField("/home/zonca/anaconda/lib/python3.4/site-packages/mbpol-1.0-py3.4-linux-x86_64.egg/mbpol.xml")
nonbonded = mm.app.CutoffNonPeriodic

system = forcefield.createSystem(pdb.topology, nonbondedMethod=nonbonded, nonbondedCutoff=0.9*unit.nanometer, ewaldErrorTolerance=1e-08)
temperature = float(300)*unit.kelvin

integrator = mm.VerletIntegrator(0.2*unit.femtoseconds)

platform = mm.Platform.getPlatformByName('Reference')
simulation = mm.app.Simulation(pdb.topology, system, integrator, platform)
simulation.context.setPositions(pdb.positions)
simulation.context.computeVirtualSites()

simulation_steps=50
equilibration_steps=10

reporters = []
reporters.append(mm.app.PDBReporter(simulation_name + "_trajectory.pdb", 1))
reporters.append(mm.app.StateDataReporter(simulation_name + ".log", 1, step=True,
        potentialEnergy=True, temperature=True, progress=True, remainingTime=True,
        speed=True, totalEnergy=True, volume=True, density=True, kineticEnergy=True,
        totalSteps=max(simulation_steps+equilibration_steps, 1), separator=','))


print("Setting random velocities based on temperature")
simulation.context.setVelocitiesToTemperature(temperature)

# Add a `reporter` that prints out the simulation status every 10%
simulation.reporters.append(mm.app.StateDataReporter(sys.stdout, max(1, int((simulation_steps+equilibration_steps)/10)), step=True,
    progress=True, remainingTime=True,
    totalSteps=max(simulation_steps+equilibration_steps, 1), separator=','))

print("Running equilibration")
simulation.step(equilibration_steps)
print("Running simulation")

try:
    from chemistry.openmm.reporters import NetCDFReporter
    save_velocities_every = 1
    if save_velocities_every > 0:
        reporters.append(NetCDFReporter(simulation_name + ".nc", save_velocities_every, crds=True, vels=True, frcs=True))
except ImportError:
    print("Saving velocities to file requires the ParmEd python package")

for r in reporters:
    simulation.reporters.append(r)

simulation.step(simulation_steps)

