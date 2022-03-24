import argparse

import numpy as np
np.random.seed(123)
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def kick_step_propagator(t, p, f=None):
    """t is the time step (usually dt/2); p is the momentum which must be propagated """
    if f:
        return p + t * f
    else:
        return p 

def drift_step_propagator(t, r, p, box, periodic=True):
    r = r + t * (p / box)
    #r = r - np.rint(r) # periodic bounderies
    r = r % box if periodic else r
    return r
    

def random_step_propagator(t, p, gamma, T, n):
    """friction and random contributions propagator.
    t is the time over which to propagate (typically dt).
    gamma is the friction coefficient, T is the temperature, n is the number of particles
    """
    x = gamma * t
    c = 1 - np.exp(-2 * x) if x > 0.0001 else np.polyval([-2/3, 4/3, -2.0, 2.0, 0.0], x)
    c = np.sqrt(c)
    p = p * np.exp(-x) + c * np.sqrt(T) * np.random.randn(n, 3)
    return p


def main(t, r, p, gamma, box, T, n, nsteps, f=None, periodic=True):
    rs, ps = [], []
    for i in range(nsteps):
        p = kick_step_propagator(t * 0.5, p, f)
        r = drift_step_propagator(t * 0.5, r, p, box, periodic=periodic)
        p = random_step_propagator(t, p, gamma, T, n)
        rs.append(drift_step_propagator(t * 0.5, r, p, box, periodic=periodic))
        ps.append(kick_step_propagator(t * 0.5, p, f))
    return np.asarray(rs), np.asarray(ps)

def update_lines(num, walks, lines):
    """
    CALLED FROM ANIMATION ---
    It updates the lines containing axes plot with the particles trajectories:
    walks is a numpy 3D Tensor where dimension is: num particles x num_steps x 3
    """
    for i, line in enumerate(lines):
        x, y, z = walks[:num, i, 0], walks[:num, i, 1], walks[:num, i, 2]
        #print(x.shape)
        line.set_data_3d(x, y, z)
        #line.set_3d_properties()
    return lines

def save_gif(fname, dt, r, p, gamma, box, T, n, num_steps, f=None, lw=1.5, periodic=True):
    # Data: simulation of a 3D brownian dynamics of N particles
    STEP = p*dt + np.sqrt(dt)
    r_left = r - STEP
    r_right = r + STEP
    rs, _ = main(dt, r, p, gamma, box, T, n, num_steps, f, periodic=periodic)
    #print(f'RS shape: {rs.shape}') -> num_steps x N x 3
    #rs = rs.reshape((n, num_steps, 3))
    
    # Attaching 3D axis to the figure
    fig, ax1 = plt.subplots(1, 1)
    ax1 = fig.add_subplot(projection="3d")
    
    # Create lines initially without data
    lines = [ax1.plot([], [], [], lw=lw)[0] for _ in range(n)] # one plot for each particle
    
    # Setting the axes properties
    ax1.set(xlim3d=(r_left, r_right), xlabel='X')
    ax1.set(ylim3d=(r_left, r_right), ylabel='Y')
    ax1.set(zlim3d=(r_left, r_right), zlabel='Z')
    
    # Creating the Animation object
    anim = animation.FuncAnimation(
        fig, update_lines, frames=num_steps, fargs=(rs, lines), interval=200)
    
    writergif = animation.PillowWriter(fps=30)
    f = f if f else 0.0
    anim.save(f'gifs/{fname}_G{gamma}_T{T}_N{n}_F{f}_dt{dt}_box{box}.gif', writer=writergif, dpi=150)
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Brownian Dynamics MD simulation.')
    parser.add_argument(
        '--dt', help='time step integration (default value = 7e-4)', 
        required=False, type=float, action='store', default=7e-4
    )
    parser.add_argument(
        '--IC', required=False, nargs=2, action='store', type=float,
        help='initial position and velocity conditions, default=(0,0)',
        default=(4.0, 0.25)
    )
    parser.add_argument(
        '--box_dim', required=False, type=float, action='store', default=8.0,
        help='Box dimensions (default=8.0)'
    )
    parser.add_argument(
        '--num_steps', action='store', required=False, type=int, default=1000,
        help='# of stemps (default value = 1000)'
    )
    parser.add_argument(
        '--gamma', action='store', required=False, default=0.1, type=float,
        help='Friction coefficient (defalt value = 0.1)'
    )
    parser.add_argument(
        '--T', action='store', required=False, default=1.25, type=float,
        help='Temperature value (defalt value = 1.25)'
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


    args = parser.parse_args()
    
    dt = args.dt
    num_steps = args.num_steps
    r, p = args.IC
    box = args.box_dim
    gamma = args.gamma
    T = args.T
    N = args.N
    fname = args.fname
    lw = args.lw
    F = args.F

    save_gif(fname, dt, r, p, gamma, box, T, N, num_steps, f=F, lw=lw)
