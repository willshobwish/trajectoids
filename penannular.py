import matplotlib.pyplot as plt
import numpy as np

from compute_trajectoid import *

def make_path_nonuniform(xlen, r, Npath = 400):
    # factor = 0.2
    xs = np.linspace(0, xlen, Npath)
    r0 = xlen/2
    ys = []
    for x in xs:
        if x <= r0-r or x >= r0 + r:
            y = 0
        else:
            y = np.sqrt(r**2 - (x-r0)**2)
        ys.append(y)
    ys = np.array(ys)
    input_path = np.stack((xs, ys)).T
    return input_path

def make_path(xlen, r, Npath = 400):
    # first linear section
    step_size = xlen/Npath
    overall_xs = np.linspace(0, xlen/2 - r, int(round(xlen/2 - r)/step_size))
    overall_ys = np.zeros_like(overall_xs)

    # semicirle section
    nsteps_in_theta = int(round(np.pi*r/step_size))
    thetas = np.linspace(np.pi, 0, nsteps_in_theta)
    xs = r*np.cos(thetas) + xlen/2
    ys = r*np.sin(thetas)
    overall_xs = np.concatenate((overall_xs[:-1], xs))
    overall_ys = np.concatenate((overall_ys[:-1], ys))

    # second linear section
    xs = np.linspace(xlen/2 + r, xlen, int(round(xlen/2 - r)/step_size))
    ys = np.zeros_like(xs)
    overall_xs = np.concatenate((overall_xs, xs[1:]))
    overall_ys = np.concatenate((overall_ys, ys[1:]))

    input_path = np.stack((overall_xs, overall_ys)).T

    input_path = double_the_path(input_path)

    return input_path

def plot_mismatch_map_for_penannular(N=60, M=60, kx_range=(0.1, 5*np.pi), kr_range=(0.01, 1.5*np.pi)):
    # sweeping parameter space for optimal match of the starting and ending orientation
    angles = np.zeros(shape=(N, M))
    xs = np.zeros_like(angles)
    ys = np.zeros_like(angles)
    for i, kx in enumerate(np.linspace(kx_range[0], kx_range[1], N)):
        print(i)
        for j, r in enumerate(np.linspace(kr_range[0], kr_range[1], M)):
            xs[i, j] = kx
            ys[i, j] = r
            if kx<2*r:
                angles[i, j] = np.nan
            else:
                data = make_path(xlen=kx, r=r)
                rotation_of_entire_traj = trimesh.transformations.rotation_from_matrix(rotation_to_origin(data.shape[0]-1, data))
                angle = rotation_of_entire_traj[0]
                angles[i, j] = angle

    print('Min angle = {0}'.format(np.min(np.abs(angles))))
    f3 = plt.figure(3)
    plt.pcolormesh(xs, ys, np.abs(angles), cmap='viridis')
    plt.colorbar()
    plt.ylabel('radius')
    plt.xlabel('total length')
    plt.show()

path = make_path(2*np.pi, 0.5)
plt.scatter(path[:, 0], path[:, 1], alpha=0.5, color='C0')
plt.axis('equal')
plt.show()

# plot_mismatch_map_for_penannular(N=20,
#                                  M=20,
#                                  kx_range=(0.1, 11.5),
#                                  kr_range=(0.01, 1.5*np.pi))


# plot_mismatch_map_for_penannular(N=20,
#                                  M=20,
#                                  kx_range=(3.2, 4),
#                                  kr_range=(0.5, 2))

# # data = make_path(xlen=9.5, r=2.82, Npath=150)
# data = make_path(2*np.pi, 0.5, Npath=150)
# # # data = make_path(xlen=9.5, r=2.5)
# trace_on_sphere(data, kx=0.5, ky=0.5, core_radius=1, do_plot=True)

data = make_path(xlen=3.81, r=1.23, Npath=150)
# data = make_path(2*np.pi, 0.5, Npath=150)
# # # data = make_path(xlen=9.5, r=2.5)
trace_on_sphere(data, kx=1, ky=1, core_radius=1, do_plot=True)