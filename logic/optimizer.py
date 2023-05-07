from function import Function


class Optimizer:
    def __init__(self, max_iter=10):
        self.f = Function()
        self._start(max_iter)

    def _start(self, max_iter):
        self.__min_point = self.f.nelder_mead(max_iter=max_iter)
        self.__min_value = self.f.calculate((self.__min_point.x, self.__min_point.y))
        self.__x_limits, self.__y_limits = self.f.limits()
        self.__z_limits = self.f.calculate((self.__x_limits, self.__y_limits))

    def get_min_point(self):
        return self.__min_point

    def get_min_value(self):
        return self.__min_value

    def get_limits(self):
        return self.__x_limits, self.__y_limits, self.__z_limits

    def x_limits(self):
        return self.__x_limits

    def get_x_min_max(self):
        return self.__x_limits.min(), self.__x_limits.max()

    def y_limits(self):
        return self.__y_limits

    def get_y_min_max(self):
        return self.__y_limits.min(), self.__y_limits.max()

    def z_limits(self):
        return self.__z_limits

    def get_z_min_max(self):
        return self.__z_limits.min(), self.__z_limits.max()

    def get_points(self):
        return self.f.triangle_points
