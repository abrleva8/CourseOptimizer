import matplotlib.pyplot as plt
from matplotlib import cm, animation
from matplotlib.animation import FuncAnimation, PillowWriter, MovieWriter
from matplotlib.patches import Polygon
from matplotlib.ticker import LinearLocator
import numpy as np
import point


class Function:
    def __init__(self):
        self.triangle_points = []
        self.alpha = 1
        self.alpha_1 = 1
        self.beta = 1
        self.beta_1 = 1
        self.mu = 1
        self.mu_1 = 1
        self.v_1 = 11
        self.v_2 = 7
        self.N = 2
        self.min_a1 = 1
        self.min_a2 = 1
        self.max_a1 = 10
        self.max_a2 = 10
        self.max_sum_of_a1_and_a2 = 8

    def limits(self):
        x = np.arange(self.min_a1, self.max_a1, 0.25)
        y = np.arange(self.min_a2, self.max_a2, 0.25)
        x, y = np.meshgrid(x, y)
        mask = np.where((x + y) <= self.max_sum_of_a1_and_a2, True, False)
        x = np.ma.masked_array(x, ~mask)
        y = np.ma.masked_array(y, ~mask)
        return x, y

    def calculate(self, point):
        a1, a2 = point
        return self.alpha * (a1 ** 2 + self.beta * a2 - self.mu * self.v_1) ** self.N + \
            self.alpha_1 * (self.beta_1 * a1 + a2 ** 2 - self.mu_1 * self.v_2) ** self.N

    def plot(self):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, dpi=100)
        x, y = self.limits()
        z = self.calculate((x, y))
        surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
        ax.set_zlim(z.min(), z.max())
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min(), y.max())
        ax.zaxis.set_major_locator(LinearLocator(20))
        ax.zaxis.set_major_formatter('{x:.02f}')
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()

    # TODO: try split animation and static
    # also delete redundant functions
    def plot_contours(self):
        self.nelder_mead()
        points = self.triangle_points
        fig, ax = plt.subplots()
        x, y = self.limits()
        z = self.calculate((x, y))
        ax.contour(x, y, z, levels=20, linewidths=0.5, colors='k')
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min(), y.max())
        cntr = ax.contourf(x, y, z, levels=20, cmap="RdBu_r")
        fig.colorbar(cntr, ax=ax)
        points = self.triangle_points

        def animate(i):
            ax.clear()
            # Get the point from the points list at index i
            point = points[i]
            triangle = np.array(point + point[:1])
            ax.contour(x, y, z, levels=20, linewidths=0.5, colors='k')
            # ax.set_xlim(-1, 10)
            # ax.set_ylim(-1, 10)
            ax.plot(triangle[:, 0], triangle[:, 1], marker='o')
            cntr = ax.contourf(x, y, z, levels=20, cmap="RdBu_r")
            # fig.colorbar(cntr, ax=ax)
            ax.fill(triangle[:, 0], triangle[:, 1], color='yellow', alpha=0.3)
            ax.set_xlim([0.99, 7.05])
            ax.set_ylim([0.99, 7.05])

        # fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(5, 5)

        ani = FuncAnimation(fig, animate, frames=10, interval=500, repeat=False)
        ani.save("simple_animation.gif", writer='PillowWriter')


        # plt.show()

    def xxx(self):
        self.nelder_mead()
        points = self.triangle_points

        def animate(i):
            ax.clear()
            # Get the point from the points list at index i
            point = points[i]
            triangle = np.array(point + point[:1])

            ax.plot(triangle[:, 0], triangle[:, 1], marker='o')
            ax.fill(triangle[:, 0], triangle[:, 1], color='yellow', alpha=0.3)
            ax.set_xlim([-1, 10])
            ax.set_ylim([-1, 10])

        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(5, 5)

        ani = FuncAnimation(fig, animate, frames=10, interval=500, repeat=False)
        ani.save("simple_animation.gif", writer='PillowWriter')

    def nelder_mead(self, alpha=1, beta=0.5, gamma=2, max_iter=10):
        self.triangle_points = []
        v1 = point.Point(7, 1)
        v2 = point.Point(1, 7)
        v3 = point.Point(3, 4)
        self.triangle_points.append([v1.tuple_from_data(), v2.tuple_from_data(), v3.tuple_from_data()])

        for i in range(max_iter):
            adict = {v1: self.calculate(v1.tuple_from_data()),
                     v2: self.calculate(v2.tuple_from_data()),
                     v3: self.calculate(v3.tuple_from_data())}
            points = sorted(adict.items(), key=lambda x: x[1])

            b, g, w = points[0][0], points[1][0], points[2][0]
            mid = (g + b) / 2
            xr = mid + alpha * (mid - w)

            # reflection
            if self.calculate(xr.tuple_from_data()) < self.calculate(g.tuple_from_data()):
                w = xr
            else:
                if self.calculate(xr.tuple_from_data()) < self.calculate(w.tuple_from_data()):
                    w = xr
                center = (w + mid) / 2
                if self.calculate(center.tuple_from_data()) < self.calculate(w.tuple_from_data()):
                    w = center

            if self.calculate(xr.tuple_from_data()) < self.calculate(b.tuple_from_data()):

                # expansion
                xe = mid + gamma * (xr - mid)
                if self.calculate(xe.tuple_from_data()) < self.calculate(xr.tuple_from_data()):
                    w = xe
                else:
                    w = xr

            if self.calculate(xr.tuple_from_data()) > self.calculate(g.tuple_from_data()):

                # contraction
                xc = mid + beta * (w - mid)
                if self.calculate(xc.tuple_from_data()) < self.calculate(w.tuple_from_data()):
                    w = xc

            v1 = w
            v2 = g
            v3 = b
            self.triangle_points.append([v1.tuple_from_data(), v2.tuple_from_data(), v3.tuple_from_data()])
        return b
