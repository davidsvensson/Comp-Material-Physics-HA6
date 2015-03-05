from ase.structure import bulk
from ase.calculators.emt import EMT
from ase.dft.kpoints import ibz_points, get_bandpath
from ase.phonons import Phonons

# Setup crystal and EMT calculator
atoms = bulk('Al', 'fcc', a=4.05)
calc = EMT()

# Phonon calculator
N = 7
ph = Phonons(atoms, calc, supercell=(N, N, N), delta=0.05)
ph.run()

# Read forces and assemble the dynamical matrix
ph.read(acoustic=True)

# High-symmetry points in the Brillouin zone
points = ibz_points['fcc']
G = points['Gamma']
X = points['X']
W = points['W']
K = points['K']
L = points['L']
U = points['U']

point_names = ['$\Gamma$', 'X', 'U', 'L', '$\Gamma$', 'K']
path = [G, X, U, L, G, K]

# Band structure in meV
path_kc, q, Q = get_bandpath(path, atoms.cell, 100)
omega_kn = 1000 * ph.band_structure(path_kc)

# Calculate phonon DOS
omega_e, dos_e = ph.dos(kpts=(50, 50, 50), npts=5000, delta=5e-4)
omega_e *= 1000

# Plot the band structure and DOS
import pylab as plt
plt.figure(1, (8, 6))
plt.axes([.1, .07, .67, .85])
for n in range(len(omega_kn[0])):
    omega_n = omega_kn[:, n]
    plt.plot(q, omega_n, 'k-', lw=2)

plt.xticks(Q, point_names, fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(q[0], q[-1])
plt.ylabel("Frequency ($\mathrm{meV}$)", fontsize=22)
plt.grid('on')

plt.axes([.8, .07, .17, .85])
plt.fill_between(dos_e, omega_e, y2=0, color='lightgrey', edgecolor='k', lw=1)
plt.ylim(0, 35)
plt.xticks([], [])
plt.yticks([], [])
plt.xlabel("DOS", fontsize=18)
plt.show()
