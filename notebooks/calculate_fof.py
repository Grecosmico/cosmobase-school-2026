#!/usr/bin/env python

import os
import numpy as np
import readgadget

from nbodykit.source.catalog import ArrayCatalog
from nbodykit.algorithms.fof import FOF


# ============================================================
# CONFIGURATION
# ============================================================

# Directory where this script is located: notebooks/
script_dir = os.path.dirname(os.path.abspath(__file__))

# L-PICOLA snapshots
snapshots = {
    'z0': os.path.join(script_dir, '../../codes/l-picola/snapshots/test_z0p000'),
    'z0p5': os.path.join(script_dir, '../../codes/l-picola/snapshots/test_z0p500')
}

# FoF parameters
b = 0.2       # Linking length relative to mean particle separation
Nmin = 20     # Minimum number of particles per halo

# Output directory: notebooks/halos/
output_dir = os.path.join(script_dir, 'halos')
os.makedirs(output_dir, exist_ok=True)


# ============================================================
# LOOP OVER SNAPSHOTS
# ============================================================

for name, snapshot in snapshots.items():

    print('\n====================================================')
    print('Processing:', name)
    print('Snapshot:', snapshot)
    print('====================================================')


    # ========================================================
    # READ GADGET SNAPSHOT
    # ========================================================

    header = readgadget.header(snapshot)

    # Simulation information
    BoxSize = header.boxsize        # Mpc/h
    redshift = header.redshift

    # CDM particle mass
    mp = header.massarr[1] * 1e10        # Msun/h

    # Read CDM particle positions and velocities
    pos = readgadget.read_block(snapshot, "POS ", [1])   # Mpc/h
    vel = readgadget.read_block(snapshot, "VEL ", [1])         # km/s

    print('Redshift       = %.3f' % redshift)
    print('Box size       = %.3f Mpc/h' % BoxSize)
    print('Particles      =', len(pos))
    print('Particle mass  = %.3e Msun/h' % mp)


    # ========================================================
    # CREATE NBODYKIT PARTICLE CATALOGUE
    # ========================================================

    # nbodykit requires Position.
    # Velocity is also needed by find_features() to calculate
    # the center-of-mass velocity of each FoF group.
    data = ArrayCatalog({
        'Position': pos,
        'Velocity': vel
    })

    # Periodic simulation box
    data.attrs['BoxSize'] = np.array([BoxSize, BoxSize, BoxSize])


    # ========================================================
    # FRIENDS-OF-FRIENDS HALO FINDER
    # ========================================================

    print('\nRunning FoF...')
    print('b    =', b)
    print('Nmin =', Nmin)

    fof = FOF(
        data,
        linking_length=b,
        nmin=Nmin,
        absolute=False,
        periodic=True
    )

    # Construct catalogue containing:
    # CMPosition : center-of-mass position
    # CMVelocity : center-of-mass velocity
    # Length     : number of particles in each FoF halo
    halos = fof.find_features()

    print('FoF finished.')


    # ========================================================
    # EXTRACT HALO PROPERTIES
    # ========================================================

    length = halos['Length'].compute()
    position = halos['CMPosition'].compute()
    velocity = halos['CMVelocity'].compute()

    # Remove possible empty entries
    mask = length > 0

    length = length[mask]
    position = position[mask]
    velocity = velocity[mask]

    # Halo mass:
    #
    # M_halo = N_particles * m_particle
    #
    mass = length.astype(np.float64) * mp

    print('Number of halos =', len(mass))


    # ========================================================
    # BASIC HALO INFORMATION
    # ========================================================

    if len(mass) > 0:

        print('Minimum Npart =', np.min(length))
        print('Maximum Npart =', np.max(length))

        print('Minimum halo mass = %.3e Msun/h' % np.min(mass))
        print('Maximum halo mass = %.3e Msun/h' % np.max(mass))

    else:

        print('WARNING: no halos were found.')
        continue


    # ========================================================
    # SAVE HALO CATALOGUE
    # ========================================================

    output_file = os.path.join(output_dir, 'fof_%s.npz' % name)

    np.savez(
        output_file,

        # Halo properties
        Position=position,
        Velocity=velocity,
        Mass=mass,
        Npart=length,

        # Simulation properties
        BoxSize=BoxSize,
        redshift=redshift,
        particle_mass=mp,

        # FoF parameters
        linking_length=b,
        Nmin=Nmin
    )

    print('\nCatalogue saved:')
    print(output_file)


# ============================================================
# FINISHED
# ============================================================

print('\n====================================================')
print('All FoF catalogues completed.')
print('====================================================')
