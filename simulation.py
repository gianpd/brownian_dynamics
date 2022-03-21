import argparse

import numpy as np
np.random.seed(12345)
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def kick_step_propagator(t, p, f=None):
    """t is the time step (usually dt/2); p is the momentum which must be propagated, f the external force"""
    if f:
        return p + t * f
    else:
        return p

def drift_step_propagator(t, r, p, box):
    r = r + t * (p / box)
    #r = r - np.rint(r) # periodic bounderies
    r = r % box
    return r
    

def random_step_propagator(t, p, gamma, T, n, random=True):
    """friction and random contributions propagator.
    t is the time over which to propagate (typically dt).
    gamma is the friction coefficient, T is the temperature, n is the number of particles
    """
    x = gamma * t
    c = 1 - np.exp(-2 * x) if x > 0.0001 else np.polyval([-2/3, 4/3, -2.0, 2.0, 0.0], x)
    c = np.sqrt(c)
    if random:
        p = p * np.exp(-x) + c * np.sqrt(T) * np.random.randn(n, 3)
        return p
    else:
        # the system will not reach any equilibrium state because 
        # at long-time its velocity will be zero, while the equipartition theorem requires:
        # <v**2> \sim K_BT. The random force allows to reach the equilibrium state (fluctuation-dissipation theorem)
        p = p * np.exp(-x)
        return p


def main(t, r, p, gamma, box, T, n, nsteps, f=None, random=True):
    rs, ps = [], []
    for i in range(nsteps):
        p = kick_step_propagator(t * 0.5, p, f)
        r = drift_step_propagator(t * 0.5, r, p, box)
        p = random_step_propagator(t, p, gamma, T, n, random=random)
        rs.append(drift_step_propagator(t * 0.5, r, p, box))
        ps.append(kick_step_propagator(t * 0.5, p, f))
    return rs, ps


def update_lines(num, walks, lines):
    for line, walk in zip(lines, walks):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(walk[:num, :2].T)
        line.set_3d_properties(walk[:num, 2])
    return lines

def save_gif(fname, dt, r, p, gamma, box, T, n, num_steps, f=None, lw=2, random=True):
    # Data: simulation of a 3D brownian dynamics of N particles
    rs, _ = main(dt, r, p, gamma, box, T, n, num_steps, f, random=random)
    rs = np.asarray(rs).reshape((n, num_steps, 3))
    
    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax1 = fig.add_subplot(projection="3d")
    
    # Create lines initially without data
    lines = [ax1.plot([], [], [], lw=lw)[0] for _ in rs]
    
    # Setting the axes properties
    ax1.set(xlim3d=(0, 1), xlabel='X')
    ax1.set(ylim3d=(0, 1), ylabel='Y')
    ax1.set(zlim3d=(0, 1), zlabel='Z')
    
    # Creating the Animation object
    anim = animation.FuncAnimation(
        fig, update_lines, num_steps, fargs=(rs, lines), interval=520)
    
    writergif = animation.PillowWriter(fps=30)
    f = f if f else 0.0
    anim.save(f'gifs/{fname}_G{gamma}_T{T}_N{n}_F{f}_dt{dt}.gif', writer=writergif, dpi=150)
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Brownian Dynamics MD simulation.')
    parser.add_argument(
        '--dt', help='time step integration (default value = 0.005)', 
        required=False, type=float, action='store', default=0.005
    )
    parser.add_argument(
        '--IC', required=False, type=float, action='store',
        help='initial position and velocity conditions, default=(0,0)',
        default=(0.0, 0.0)
    )
    parser.add_argument(
        '--box_dim', required=False, type=float, action='store', default=1.0,
        help='Box dimensions (default=1.0)'
    )
    parser.add_argument(
        '--num_steps', action='store', required=False, type=int, default=1000,
        help='# of stemps (default value = 1000)'
    )
    parser.add_argument(
        '--gamma', action='store', required=False, default=0.5, type=float,
        help='Friction coefficient (defalt value = 0.5)'
    )
    parser.add_argument(
        '--T', action='store', required=False, default=1.0, type=float,
        help='Temperature value (defalt value = 1.0)'
    )
    parser.add_argument(
        '--N', action='store', required=False, default=1, type=int,
        help='Number of particles (defalt value = 1)'
    )
    parser.add_argument(
        '--fname', action='store', required=False, default='sim', type=str,
        help='file name of the final gif simulation (without extensions).'
    )
    parser.add_argument(
        '--lw', action='store', required=False, type=float,
        help='Line Width dimension.'
    )
    parser.add_argument(
        '--F', action='store', required=False, type=float,
        help='External Force magnitude.'
    )
    parser.add_argument(
        '--exclude_random', action='store_false', required=False, default=True,
        help='If exluding the random force component.'
    )


    args = parser.parse_args()
    
    dt = args.dt
    r, p = args.IC
    box = args.box_dim
    gamma = args.gamma
    T = args.T
    N = args.N
    num_steps = args.num_steps
    fname = args.fname
    lw = args.lw
    F = args.F
    random = args.exclude_random
    
    save_gif(fname, dt, r, p, gamma, box, T, N, num_steps, f=F, lw=lw, random=random)

