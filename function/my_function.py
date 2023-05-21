import numpy as np

from function import point


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

    def minus_calculate(self, point):
        a1, a2 = point
        try:
            if 1 > a1 or a1 > 10:
                return 1e10
            if 1 > a2 or a2 > 10:
                return 1e10
            if a1 + a2 > 8:
                return 1e10
        except:
            pass
        return -(self.alpha * (a1 ** 2 + self.beta * a2 - self.mu * self.v_1) ** self.N +
                 self.alpha_1 * (self.beta_1 * a1 + a2 ** 2 - self.mu_1 * self.v_2) ** self.N)

    def calculate(self, point):
        a1, a2 = point
        return self.alpha * (a1 ** 2 + self.beta * a2 - self.mu * self.v_1) ** self.N + \
            self.alpha_1 * (self.beta_1 * a1 + a2 ** 2 - self.mu_1 * self.v_2) ** self.N

    def limits(self):
        x = np.arange(self.min_a1, self.max_a1, 0.25)
        y = np.arange(self.min_a2, self.max_a2, 0.25)
        x, y = np.meshgrid(x, y)
        mask = np.where((x + y) <= self.max_sum_of_a1_and_a2, True, False)
        x = np.ma.masked_array(x, ~mask)
        y = np.ma.masked_array(y, ~mask)
        return x, y

    def nelder_mead(self, alpha=0.5, beta=0.2, gamma=2, max_iter=10) -> point:
        self.triangle_points = []
        v1 = point.Point(1.4, 4)
        v2 = point.Point(2, 2)
        v3 = point.Point(4, 2)
        self.triangle_points.append([v1.tuple_from_data(), v2.tuple_from_data(), v3.tuple_from_data()])

        for i in range(max_iter):
            adict = {v1: self.minus_calculate(v1.tuple_from_data()),
                     v2: self.minus_calculate(v2.tuple_from_data()),
                     v3: self.minus_calculate(v3.tuple_from_data())}
            points = sorted(adict.items(), key=lambda x: x[1])

            b, g, w = points[0][0], points[1][0], points[2][0]
            mid = (g + b) / 2
            xr = mid + alpha * (mid - w)

            # reflection
            if self.minus_calculate(xr.tuple_from_data()) < self.minus_calculate(g.tuple_from_data()):
                w = xr
            else:
                if self.minus_calculate(xr.tuple_from_data()) < self.minus_calculate(w.tuple_from_data()):
                    w = xr
                center = (w + mid) / 2
                if self.minus_calculate(center.tuple_from_data()) < self.minus_calculate(w.tuple_from_data()):
                    w = center

            if self.minus_calculate(xr.tuple_from_data()) < self.minus_calculate(b.tuple_from_data()):

                # expansion
                xe = mid + gamma * (xr - mid)
                if self.minus_calculate(xe.tuple_from_data()) < self.minus_calculate(xr.tuple_from_data()):
                    w = xe
                else:
                    w = xr

            if self.minus_calculate(xr.tuple_from_data()) > self.minus_calculate(g.tuple_from_data()):

                # contraction
                xc = mid + beta * (w - mid)
                if self.minus_calculate(xc.tuple_from_data()) < self.minus_calculate(w.tuple_from_data()):
                    w = xc

            v1 = w
            v2 = g
            v3 = b
            self.triangle_points.append([v1.tuple_from_data(), v2.tuple_from_data(), v3.tuple_from_data()])
        return b


if __name__ == '__main__':
    f = Function()
    x, y = f.limits()
