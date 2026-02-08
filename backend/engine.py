import numpy as np

class PhysicsEngine:
    def __init__(self, N=1000, G=1.0, dt=0.02, softening=1e-2):
        self.N = N
        self.G = G
        self.dt = dt
        self.softening = softening

        # Galaxy-like initial conditions
        r = np.random.rand(N) * 5
        theta = np.random.rand(N) * 2 * np.pi

        self.positions = np.column_stack([
            r * np.cos(theta),
            r * np.sin(theta),
            np.zeros(N)
        ])

        self.velocities = np.column_stack([
            -np.sin(theta),
            np.cos(theta),
            np.zeros(N)
        ]) * 0.5

        self.masses = np.random.rand(N) + 0.5

    def step(self):
        diff = self.positions[:, None, :] - self.positions[None, :, :]
        r2 = np.sum(diff**2, axis=-1) + self.softening
        inv_r3 = r2 ** (-1.5)
        np.fill_diagonal(inv_r3, 0.0)

        accel = -self.G * np.sum(
            diff * inv_r3[..., None] * self.masses[None, :, None],
            axis=1
        )

        self.velocities += accel * self.dt
        self.positions += self.velocities * self.dt

        return self.positions, self.velocities
