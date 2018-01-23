import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

#################################################
# Parameter input
#################################################

N = 400
t = 1   # Why make computations harder than they need to be?

#################################################
# Parameter sanity check
#################################################
assert N%2 == 0, 'N must be an even number' # For easy potential placement

#################################################
# Base code
#################################################
# Building the hamiltonian operator matrix.
n  = int(N/2)
diag1 = np.full((N-1,), -1)# Divide t out
diag2 = np.full((N,), 2)
Hamiltonian = np.diag(diag1, - 1) +  np.diag(diag2) + np.diag(diag1, 1)

def potential(v0t):
    """
    Calculates the delta potential hamiltonian based on an input v0/t. Note that
    signs are reversed, so if v0t = 1, we're setting v0/t = -1.
    """
    Hamiltonian[n,n] = Hamiltonian[n,n] - v0t # Adds negative potential in middle.
    return np.linalg.eigh(Hamiltonian) # use .eig() if Hamiltonian is not symetric

#################################################
# Plotting code
#################################################
""" Usage:
In the paper, each plot is given a concise title. To obtain this plot from the 
code, please change the variable 'plot' to the title of this plot. Zooming can be
manually achieved using the lookingglass symbol in the resulting window.
The code further down can be evaluated, but needs no further input from the user.
"""
plot = 'Pbound100'

plots = {}
parse = lambda f: plots.setdefault(f.__name__,f)

# Parse each plot to a dictionary.
@parse
def Bound():
    eval, evec = potential(1)
    print(eval[0])
    plt.title('Bound')
    plt.plot(evec[:,0] , label = '$\psi$ state')
    plt.plot(evec[:,0]**2, label = 'Position probability')
    plt.legend()
    plt.show()
@parse
def Energies():
    eval, evec = potential(1)
    et = lambda x: x**2 * np.pi**2 / N**2 # Theoretical E/t
    et_list = [et(x) for x in range(N)]   # To plot et(x)
    plt.title('Energies')
    plt.plot(et_list, label='Theoretical')
    plt.plot(eval, label='Experimental')
    plt.legend()
    plt.xlabel('$n^{th}$ state')
    plt.ylabel('Energy (t)')
    plt.show()
def Pbound(v):
    eval, evec = potential(-v)
    print(eval[-1])
    plt.title('Pbound'+str(v))
    plt.plot(evec[:,-1], label = '$\psi$ state')
    plt.plot(evec[:,-1]**2, label = 'Position probability')
    plt.legend()
    plt.show()
@parse
def Pbound1():
    return Pbound(1)
@parse
def Pbound10():
    return Pbound(10)
@parse
def Pbound100():
    return Pbound(100)

# Call the desired plot.
try:
    plots[plot]()
except KeyError:
    print('You entered the wrong key. Please verify that the string assigned to the variable "plot" is correct.')
