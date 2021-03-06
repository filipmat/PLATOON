import math

class FrenetPID():
    def __init__(self, path, k_p = 0, k_i = 0, k_d = 0, freq = 20):
        # PID parameters.
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d

        self._ey = 0                    # Current error.
        self._sumy = 0                  # Accumulated error.

        self._freq = freq                # Sampling frequency.
        self._alpha_max = math.pi/6      # Maximum wheel angle alpha.
        self._alpha_min = - math.pi/6
        self._l = 0.27                   # Length between wheel pairs.
        self._alpha = 0
        self._sumy_alpha = 0

        # Reference path.
        self._pt = path


    def get_omega(self, x, y, yaw, vel):
        """Calculate the control input omega. """

        index, closest = self._pt.get_closest([x, y]) # Closest point on path.

        self._ey = self._pt.get_ey([x, y])     # y error (distance from path)

        self._sumy = self._sumy + self._ey      # Accumulated error.

        gamma = self._pt.get_gamma(index)
        gamma_p = self._pt.get_gammap(index)
        gamma_pp = self._pt.get_gammapp(index)

        cos_t = math.cos(yaw - gamma)     # cos(theta)
        sin_t = math.sin(yaw - gamma)     # sin(theta)

        # y prime (derivative w.r.t. path).
        yp = math.tan(yaw - gamma)*(1 - gamma_p*self._ey)*self._sign(
            vel*cos_t/(1 - gamma_p*self._ey))

        # PID controller.
        u = - self.k_p*self._ey - self.k_d*yp - self.k_i * self._sumy

        # Feedback linearization.
        omega = vel*cos_t/(1 - gamma_p*self._ey) * (
                        u*cos_t**2/(1 - gamma_p*self._ey) +
                        gamma_p*(1 + sin_t**2) +
                        gamma_pp*self._ey*cos_t*sin_t/(1 - gamma_p*self._ey))

        return omega


    def get_alpha(self, x, y, yaw, vel):
        """Calculate the control input alpha. """

        index, closest = self._pt.get_closest([x, y]) # Closest point on path.

        self._ey = self._pt.get_ey([x, y])     # y error (distance from path)

        self._sumy_alpha = self._sumy_alpha + self._ey      # Accumulated error.

        gamma = self._pt.get_gamma(index)
        gamma_p = self._pt.get_gammap(index)
        gamma_pp = self._pt.get_gammapp(index)

        cosa = math.cos(yaw - gamma + self._alpha)
        sina = math.sin(yaw - gamma + self._alpha)

        # y prime (derivative w.r.t. path).
        yp = sina/cosa*(1 - gamma_p*self._ey)*self._sign(
            vel*cosa/(1 - gamma_p*self._ey))

        # PID controller.
        u = - self.k_p*self._ey - self.k_d*yp - self.k_i * self._sumy_alpha

        # Feedback linearization.
        alphap = vel*cosa/(1 - gamma_p*self._ey)*(
            u*cosa**2/(1 - gamma_p*self._ey) +
            gamma_p*(1 + sina**2) +
            gamma_pp*self._ey*cosa*sina/(1 - gamma_p*self._ey)
        ) - vel*math.sin(self._alpha)/self._l

        self._alpha = self._alpha + alphap/self._freq
        if self._alpha < self._alpha_min:
            self._alpha = self._alpha_min
        if self._alpha > self._alpha_max:
            self._alpha = self._alpha_max

        return self._alpha


    def _sign(self, x):
        """Returns the sign of x. """
        if x > 0:
            return 1
        else:
            return -1


    def set_pid(self, kp = None, ki = None, kd = None):
        """Sets the PID parameters. """
        if kp is not None:
            self.k_p = kp
        if ki is not None:
            self.k_i = ki
        if kd is not None:
            self.k_d = kd

        self.reset_sum()


    def get_pid(self):
        """Returns the PID parameters. """
        return self.k_p, self.k_i, self.k_d


    def reset_sum(self):
        """Resets the sum for I part in PID controller. """
        self._sumy = 0
        self._sumy_alpha = 0


    def update_path(self, path):
        """Updates the reference path. """
        self._pt = path


    def get_y_error(self):
        """Returns the latest y error. """
        return self._ey
