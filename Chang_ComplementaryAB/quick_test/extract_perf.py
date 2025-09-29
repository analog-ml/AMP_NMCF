import numpy as np
import scipy.interpolate as interp
import scipy.optimize as sciopt
import matplotlib.pyplot as plt
import os


class PerformanceExtractor(object):
    def __init__(self, output_path):
        self.output_path = output_path

    def extract(self):
        freq, vout, ibias = self.parse_output(self.output_path)

        gain = PerformanceExtractor.find_dc_gain(vout)
        ugbw, valid = PerformanceExtractor.find_ugbw(freq, vout)
        phm = PerformanceExtractor.find_phm(freq, vout)
        return {"gain": gain, "ugbw": ugbw, "pm": phm, "power": ibias}

    def parse_output(self, output_path):

        ac_fname = os.path.join(output_path, "ac.csv")
        dc_fname = os.path.join(output_path, "dc.csv")

        if not os.path.isfile(ac_fname) or not os.path.isfile(dc_fname):
            print("ac/dc file doesn't exist: %s" % output_path)

        ac_raw_outputs = np.genfromtxt(ac_fname, skip_header=1)
        dc_raw_outputs = np.genfromtxt(dc_fname, skip_header=1)
        freq = ac_raw_outputs[:, 0]
        vout_real = ac_raw_outputs[:, 1]
        vout_imag = ac_raw_outputs[:, 2]
        vout = vout_real + 1j * vout_imag
        ibias = -dc_raw_outputs[1]

        return freq, vout, ibias

    @classmethod
    def find_dc_gain(self, vout):
        return np.abs(vout)[0]

    @classmethod
    def find_ugbw(self, freq, vout):
        gain = np.abs(vout)
        ugbw, valid = self._get_best_crossing(freq, gain, val=1)
        if valid:
            return ugbw, valid
        else:
            return freq[0], valid

    @classmethod
    def find_phm(self, freq, vout):
        gain = np.abs(vout)
        phase = np.angle(vout, deg=False)
        phase = np.unwrap(phase)  # unwrap the discontinuity
        phase = np.rad2deg(phase)  # convert to degrees

        phase_fun = interp.interp1d(freq, phase, kind="quadratic")
        ugbw, valid = self._get_best_crossing(freq, gain, val=1)
        # if valid:
        #     if phase[0] > 150:
        #         return phase_fun(ugbw)
        #     else:
        #         return 180 + phase_fun(ugbw)
        # else:
        #     return -180
        if valid:
            if phase_fun(ugbw) > 0:
                return -180 + phase_fun(ugbw)
            else:
                return 180 + phase_fun(ugbw)
        else:
            return -180

    @classmethod
    def _get_best_crossing(cls, xvec, yvec, val):
        interp_fun = interp.InterpolatedUnivariateSpline(xvec, yvec)

        def fzero(x):
            return interp_fun(x) - val

        xstart, xstop = xvec[0], xvec[-1]
        try:
            return sciopt.brentq(fzero, xstart, xstop), True
        except ValueError:
            return xstop, False


def print_metrics(metrics: dict):
    print(
        f"gain={float(metrics['gain']):.3f}, "
        f"gain_dB={float(20*np.log10(metrics['gain'])):.3f}, "
        f"ugbw={float(metrics['ugbw']/1e6):.3f} (MHz), "
        f"pm={float(metrics['pm']):.3f} (degrees), "
        f"power={float(metrics['power'] * 1e3):.3f} mA"
    )


if __name__ == "__main__":
    performance_extractor = PerformanceExtractor(".")
    result = performance_extractor.extract()
    print_metrics(result)
