import matplotlib as mpl
from pylab import *
from qutip import *
from matplotlib import cm
import imageio
from qutip.qip.operations.gates import *
import numpy as np
import math
import random

def generate_final_seq():
    """
    Protocol for Randomized Benchmarking
    """


    """
    we have 3 types of pulses to generate:
    Pauli Gates (pi_x, pi_y and pi_z), Computational Gates (pi/2_x, pi/2_y, pi/2_z) and the R gate (This is a custom gate to make sure the
    final measurement is an eigenstate of sigma_z)

    Parameters:
    Nl = Number of different truncation lengths
    Ng = Different computational gate sequences
    Np = Number of Pauli Randomization
    Ne = Number of Total experiments
    """
    l_max = 100 # Number of Computational gates that will be generated in each of the Ng sequences and then truncated Nl times.
    P = ['(identity)', '(+pi_x)', '(+pi_y)', '(-pi_x)', '(-pi_y)']  # The Set of Pauli gates
    G = ['(+pi/2_x)', '(+pi/2_y)', '(-pi/2_x)', '(-pi/2_y)']  # The set of Comp. gates
    L = [2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96] # The list of different truncation lengths
    l = 4
    """
    Generate the Ng computational gate sequences
    """
    Comp_seq_list = [[], [], [], []]
    for seq in Comp_seq_list:
        for i in range(l_max):
            seq.append(random.choice(G))
    """
    Choose one of the Ng sequences randomly truncate it to length l (should be done to all Ng sequences, not just one sequence)
    """
    G_list = Comp_seq_list[random.randint(0, 3)][:l]

    """Generate a list of l+2 Pauli gates randomly"""
    P_list = []
    for i in range(l + 2):
        P_list.append(random.choice(P))
    # print(P_list)
    # print(G_list)


    """"Pauli operators and their eigenstates"""
    I = np.array( [[1,0],[0,1]]) #Identity
    X = np.array( [[0, 1],[ 1,0]]) #Sx
    Y = np.array( [[0,-1j],[1j,0]]) #Sy
    Z = np.array( [[1,0],[0,-1]]) #Sz

    z0 = np.array([[1],[0]]) #|+z>
    z1 = np.array([[0],[1]])#|-z>
    x0 = np.round(np.array([[1],[1]]) / np.sqrt(2),3)#|+x>
    x1 = np.round(np.array([[1],[-1]]) / np.sqrt(2),3)#|-x>
    y0 = np.round(np.array([[1],[1j]]) / np.sqrt(2),3)#|+y>
    y1 = np.round(np.array([[1],[-1j]]) / np.sqrt(2),3)#|-y>

    def rotation(spin_axis,angle): # takes a rotation axis and angle and returns a rotation matrix
        #return round(np.cos(angle/2),3)*I -1j* round(np.sin(angle/2),3)*spin_axis
        return np.cos(angle / 2) * I - 1j * np.sin(angle / 2) * spin_axis

    gate = {'(identity)' : I,
            '(+pi_x)' : rotation(X,np.pi),
            '(-pi_x)' : rotation(-1*X,np.pi),
            '(+pi_y)' : rotation(Y,np.pi),
            '(-pi_y)' : rotation(-1*Y,np.pi),
            '(+pi/2_x)' : rotation(X,np.pi /2),
            '(-pi/2_x)' : rotation(-1*X,np.pi /2),
            '(+pi/2_y)' : rotation(Y,np.pi/2),
            '(-pi/2_y)' : rotation(-1*Y,np.pi/2),
            '(+pi_z)': rotation(Z, np.pi),
            '(-pi_z)': rotation(-1 * Z, np.pi),
            '(+pi/2_z)': rotation(Z, np.pi / 2),
            '(-pi/2_z)': rotation(-1 * Z, np.pi / 2)
            }
    r_gate= {'(+pi/2_x)' : rotation(X,np.pi /2),
            '(-pi/2_x)' : rotation(-1*X,np.pi /2),
            '(+pi/2_y)' : rotation(Y,np.pi/2),
            '(-pi/2_y)' : rotation(-1*Y,np.pi/2),
            '(+pi/2_z)': rotation(Z, np.pi / 2),
            '(-pi/2_z)': rotation(-1 * Z, np.pi / 2)
            }

    def find_R(gate_list):
        M = I
        Rlist = []
        for i in gate_list:
            M = np.matmul(gate[i], M)
        for i in r_gate:
            M2 = np.matmul(r_gate[i], M)
            if np.allclose(abs(np.inner(np.ndarray.flatten(z0), np.ndarray.flatten(np.matmul(M2, z0)))), 1) or np.allclose(
                    abs(np.inner(np.ndarray.flatten(z1), np.ndarray.flatten(np.matmul(M2, z0)))), 1):
                Rlist.append(i)
        R = random.choice(Rlist)
        M3 = np.matmul(r_gate[R], M)
        if np.isclose(abs(np.inner(np.ndarray.flatten(z0), np.ndarray.flatten(np.matmul(M3, z0)))), 1):
            final_state = 'z0'
        elif np.isclose(abs(np.inner(np.ndarray.flatten(z1), np.ndarray.flatten(np.matmul(M3, z0)))), 1):
            final_state = 'z1'
        else:
            print("error!!!")
        return R,final_state


    """"Generate the full sequence"""
    R,final_state = find_R(G_list)
    sequence=[]
    for i in range(l):
        sequence.append(P_list[i])
        sequence.append(G_list[i])
    sequence.append(P_list[-2])
    sequence.append(R)
    sequence.append(P_list[-1])

    return sequence

def animate_bloch(states, duration=0.1, save_all=False):

    b = Bloch()
    b.vector_color = ['r']
    b.view = [-40,30]
    images=[]
    try:
        length = len(states)
    except:
        length = 1
        states = [states]
    ## normalize colors to the length of data ##
    nrm = mpl.colors.Normalize(0,length)
    colors = cm.summer(nrm(range(length))) # options: cool, summer, winter, autumn etc.

    ## customize sphere properties ##
    b.point_color = ['b'] # options: 'r', 'g', 'b' etc.
    b.point_marker = ['o']
    b.point_size = [60]
    
    for i in range(length):
        b.clear()
        b.add_states(states[i])
        b.add_states(states[:(i+1)],'point')
        if save_all:
            b.save(dirc='tmp') #saving images to tmp directory
            filename="tmp/bloch_%01d.png" % i
        else:
            filename='final.png'
            b.save('RandBenchmarking\\' + filename)
        images.append(imageio.imread('RandBenchmarking\\' + filename))
    imageio.mimsave('RandBenchmarking\\final.gif', images, duration=duration)

gates = {'(identity)' : qeye(2),
        '(+pi_x)' : rx(np.pi),
        '(-pi_x)' : rx(-np.pi),
        '(+pi_y)' : ry(np.pi),
        '(-pi_y)' : ry(-np.pi),
        '(+pi/2_x)' : rx(np.pi /2),
        '(-pi/2_x)' : rx(-np.pi /2),
        '(+pi/2_y)' : ry(np.pi/2),
        '(-pi/2_y)' : ry(-np.pi/2),
        '(+pi_z)': rz(np.pi),
        '(-pi_z)': rz(-np.pi),
        '(+pi/2_z)': rz(np.pi / 2),
        '(-pi/2_z)': rz(-np.pi / 2)
        }

final_gate_seq = generate_final_seq()
res = basis(2,0)
states = []
for g in final_gate_seq:
    res = gates[g]*res
    states.append(res)

animate_bloch(states, duration=0.5, save_all=False)