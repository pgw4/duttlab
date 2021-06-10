# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 15:41:36 2015

@author: DUTTLAB7
"""
# This file has been modified on Sept. 23, 2019 by
# Gurudev Dutt. Mainly to make it compatible with Python 3
# TODO: code is rather bloated and reproduces stuff like fitting to exponentials
# TODO: need to simplify and cut bloat.


# PicoHarp 300    File Access Utility
# ported from the PicoQuant matlab demo to python by KJR, Oct 2010
# (for python version 2.6)

# This script reads a binary PicoHarp 300 data file (*.phd)
# and returns its contents. Works with file format version 2.0 only!

# Original Matlab code disclaimer:
# Peter Kapusta, PicoQuant GmbH, September 2006
# This is demo code. Use at your own risk. No warranties.
# Make sure you have enough memory when loading large files!



import sys
import os.path
import os
import struct  # deal with binary data
# import np
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit, leastsq
from scipy.signal import cspline1d, cspline1d_eval


class Trace():
    """ A class for holding lifetime data. You pass
        it the name of the phdfile (including .phd)
        and it will load it and offer various methods
        for plotting, wrapping (removing time offset)
        and fitting exponentials.
    """

    def __init__(self, phdfile):
        self.fname = phdfile
        self.has_fit = False
        self.ax = None
        self.irf = None
        self.wraptime = None

        with open(phdfile, 'rb') as self.fobj:
            self.readasciiheader(verbose=False)
            self.readbinaryheader(verbose=False)
            self.readboardheader()
            self.readcurveheaders(verbose=False)
            self.readhistograms()
            self.resolution = self.curveheaders[0]['Resolution']  # curve 0 resolution, actually (ns)
            self.t = []
            for i, curve in enumerate(self.curves):
                self.t.append(np.arange(len(curve)) * self.curveheaders[i]['Resolution'])  # this is in ns
            self.raw_t = self.t[:]

    def fit_exponential(
            self,
            tstart=0.0,
            tend=None,
            guess=dict(l0=5.0, a0=1.0, b=0.0),
            num_exp=None,
            verbose=True,
            deconvolve=False,
            fixed_params=[None],
            curve_num=0):
        """
        fit a function of exponentials to a single curve of the file
        (my files only have one curve at this point anyway,
        curve 0).
        The parameter num_exp (default is 1, max is 3) defines the number of
        exponentials in the funtion to be fitted.
        num_exp=1 yields:
        f(t) = a0*exp(-t/l0) + b
        where l0 is the lifetime and a0 and b are constants,
        and we fit over the range from tstart to tend.
        You don't have to pass this parameter anymore; just pass an initial guess and
        the number of parameters passed will determine the type of model used.

        If tend==None, we fit until the end of the curve.

        If num_exp > 1, you will need to modify the initial
        parameters for the fit (i.e. pass the method an explicit `guess`
        parameter) because the default has only three parameters
        but you will need two additional parameters for each additional
        exponential (another lifetime and another amplitude) to describe
        a multi-exponential fit.
        For num_exp=2:
        f(t) = a1*exp(-t/l1) + a0*exp(-t/l0) + b

        and for num_exp=3:
        f(t) = a2*exp(-t/l2) + a1*exp(-t/l1) + a0*exp(-t/l0) + b

        verbose=True (default) results in printing of fitting results to terminal.

        """
        self.fitstart = tstart
        self.deconvolved = deconvolve
        tpulse = 1.0e9 / self.curveheaders[0]['InpRate0']  # avg. time between pulses, in ns

        if num_exp is None:
            num_exp = (1 + int('l1' in guess) +
                       int('l2' in guess) +
                       int('l3' in guess) +
                       int('l4' in guess))
            num_a = (1 + int('a1' in guess) +
                     int('a2' in guess) +
                     int('a3' in guess) +
                     int('a4' in guess))
            if num_exp != num_a:
                raise ValueError("Missing a parameter! Unequal number of lifetimes and amplitudes.")

        keylist = ["l0", "a0", "b"]
        errlist = ["l0_err", "a0_err"]
        if num_exp == 2:
            keylist = ["l1", "a1", "l0", "a0", "b"]
            errlist = ["l1_err", "a1_err", "l0_err", "a0_err"]
        elif num_exp == 3 and 't_ag' not in guess and 't_d3' not in guess:
            keylist = ["l2", "a2", "l1", "a1", "l0", "a0", "b"]
            errlist = ["l2_err", "a2_err", "l1_err", "a1_err", "l0_err", "a0_err"]
        elif num_exp == 3 and 't_ag' in guess:
            keylist = ["l2", "a2", "l1", "a1", "l0", "a0", "t_ag"]
            errlist = ["l2_err", "a2_err", "l1_err", "a1_err", "l0_err", "a0_err"]
        elif num_exp == 3 and 't_d3' in guess:
            keylist = ["l2", "a2", "l1", "a1", "l0", "a0", "t_d3"]
            errlist = ["l2_err", "a2_err", "l1_err", "a1_err", "l0_err", "a0_err"]
        elif num_exp == 4:
            keylist = ["l3", "a3", "l2", "a2", "l1", "a1", "l0", "a0", "b"]
            errlist = ["l3_err", "a3_err", "l2_err", "a2_err", "l1_err", "a1_err", "l0_err", "a0_err"]
        elif num_exp == 5:
            keylist = ["l4", "a4", "l3", "a3", "l2", "a2", "l1", "a1", "l0", "a0", "b"]
            errlist = ["l4_err", "a4_err", "l3_err", "a3_err", "l2_err", "a2_err", "l1_err", "a1_err", "l0_err",
                       "a0_err"]

        if deconvolve == False:
            params = [guess[key] for key in keylist]
            free_params = [i for i, key in enumerate(keylist) if not key in fixed_params]
            initparams = [guess[key] for key in keylist if not key in fixed_params]

            def f(t, *args):
                for i, arg in enumerate(args): params[free_params[i]] = arg
                local_params = params[:]
                b = local_params.pop(-1)
                result = np.zeros(len(t))
                for l, a in zip(params[::2], params[1::2]):
                    result += abs(a) * np.exp(-(t - tstart) / abs(l))
                return result + b

        else:
            raise NameError(
                "Deconvolution with this module is not kept current. Use FastFit module from fit directory instead.")
            if self.irf == None: raise AttributeError("No detector trace!!! Use self.set_detector() method.")
            t0 = tstart
            tstart = 0.0
            keylist.append("tshift")
            params = [guess[key] for key in keylist]
            free_params = [i for i, key in enumerate(keylist) if not key in fixed_params]
            initparams = [guess[key] for key in keylist if not key in fixed_params]

            def f(t, *args):
                for i, arg in enumerate(args): params[free_params[i]] = arg
                tshift = params[-1]
                ideal = fmodel(t, *args)
                irf = cspline1d_eval(self.irf_generator, t - tshift, dx=self.irf_dt, x0=self.irf_t0)
                convoluted = np.real(np.ifft(np.fft(ideal) * np.fft(irf)))  # very small imaginary anyway
                return convoluted

            def fmodel(t, *args):
                for i, arg in enumerate(args): params[free_params[i]] = arg
                local_params = params[:]
                tshift = local_params.pop(-1)
                if 't_ag' in guess:
                    t_ag = abs(local_params.pop(-1))
                elif 't_d3' in guess:
                    t_d3 = abs(local_params.pop(-1))
                elif 'a_fix' in guess:
                    scale = local_params.pop(-1)
                else:
                    b = local_params.pop(-1)

                result = np.zeros(len(t))
                for l, a in zip(local_params[::2], local_params[1::2]):
                    if 't_ag' in guess: l = 1.0 / (1.0 / l + 1.0 / t_ag)
                    if 't_d3' in guess: l *= t_d3
                    if 'a_fix' in guess: a *= scale
                    result += abs(a) * np.exp(-t / abs(l)) / (1.0 - np.exp(-tpulse / abs(l)))
                return result

        istart = np.find(self.t[curve_num] >= tstart)[0]
        if tend is not None:
            iend = np.find(self.t[curve_num] <= tend)[-1]
        else:
            iend = len(self.t[curve_num])

        # sigma (std dev.) is equal to sqrt of intensity, see
        # Lakowicz, principles of fluorescence spectroscopy (2006)
        # sigma gets inverted to find a weight for leastsq, so avoid zero
        # and imaginary weight doesn't make sense.
        trace_scaling = self.curves[0].max() / self.raw_curves[0].max()
        sigma = np.sqrt(
            self.raw_curves[curve_num][istart:iend] * trace_scaling)  # use raw curves for actual noise, scale properly
        self.bestparams, self.pcov = curve_fit(f, self.t[curve_num][istart:iend],
                                               self.curves[curve_num][istart:iend],
                                               p0=initparams,
                                               sigma=sigma)

        if np.size(self.pcov) > 1 and len(np.find(self.pcov == np.inf)) == 0:
            self.stderr = np.sqrt(np.diag(self.pcov))  # is this true?
        else:
            self.stderr = [np.inf] * len(guess)

        stderr = [numpy.NaN] * len(params)
        for i, p in enumerate(self.bestparams):
            params[free_params[i]] = p
            stderr[free_params[i]] = self.stderr[i]
        self.stderr = stderr

        self.fitresults = dict()
        keys = keylist[:]
        stderr = stderr[:]
        p = params[:]
        if deconvolve:
            tshift = p.pop(-1)
            self.fitresults['tshift'] = tshift
            tshift_err = stderr.pop(-1)
            self.fitresults['tshift_err'] = tshift_err
            keys.pop(-1)
            self.fitresults['irf_dispersion'] = self.irf_dispersion

        b = p.pop(-1)
        self.fitresults['b'] = b
        b_err = stderr.pop(-1)
        self.fitresults['b_err'] = b_err
        keys.pop(-1)
        self.lifetime = [abs(l) for l in p[::2]]
        for l, a, lkey, akey in zip(p[::2], p[1::2], keys[::2], keys[1::2]):
            if 't_ag' in guess: l = 1.0 / (1.0 / l + 1.0 / b)
            if 't_d3' in guess: l *= b
            if 'a_fix' in guess: a *= b
            self.fitresults[lkey] = abs(l)
            self.fitresults[akey] = abs(a)
        for l, a, lkey, akey in zip(stderr[::2], stderr[1::2], errlist[::2], errlist[1::2]):
            self.fitresults[lkey] = l
            self.fitresults[akey] = a
        self.fitresults['l0_int'] = self.fitresults['l0'] * self.fitresults['a0']

        if num_exp > 1: self.fitresults['l1_int'] = self.fitresults['l1'] * self.fitresults['a1']
        if num_exp > 2: self.fitresults['l2_int'] = self.fitresults['l2'] * self.fitresults['a2']
        if num_exp > 3: self.fitresults['l3_int'] = self.fitresults['l3'] * self.fitresults['a3']
        if num_exp > 4: self.fitresults['l4_int'] = self.fitresults['l4'] * self.fitresults['a4']

        self.bestfit = f(self.t[curve_num][istart:iend], *self.bestparams)
        if deconvolve: self.model = fmodel(self.t[curve_num][istart:iend], *self.bestparams)

        Chi2 = np.sum((self.bestfit - self.curves[0][istart:iend]) ** 2 / sigma ** 2)
        # Chi2 *= self.raw_curves[0].max()/self.curves[0].max() # undo any scaling
        mean_squares = np.mean((self.bestfit - self.curves[0][istart:iend]) ** 2)
        degrees_of_freedom = len(self.bestfit) - len(free_params)
        self.fitresults['MSE'] = mean_squares / degrees_of_freedom
        self.fitresults['ReducedChi2'] = Chi2 / degrees_of_freedom

        if verbose:
            print(
            "Fit results: (Reduced Chi2 = %.3E)" % (self.fitresults['ReducedChi2']))
            print()
            "             (MSE = %.3E)" % (self.fitresults['MSE'])
            print(
            "  Offset/t_ag/scale = %.3f +-%.3e" % (self.fitresults['b'], self.fitresults['b_err']))
            print(
            "  l0=%.3f +-%.3f ns, a0=%.3e +-%.3e" % (self.fitresults['l0'],
                                                     self.fitresults['l0_err'],
                                                     self.fitresults['a0'],
                                                     self.fitresults['a0_err']))
            if num_exp > 1:
                print(
                "  l1=%.3f +-%.3f ns, a1=%.3e +-%.3e" % (self.fitresults['l1'],
                                                         self.fitresults['l1_err'],
                                                         self.fitresults['a1'],
                                                         self.fitresults['a1_err']))
            if num_exp > 2:
                print(
                "  l2=%.3f +-%.3f ns, a2=%.3e +-%.3e" % (self.fitresults['l2'],
                                                         self.fitresults['l2_err'],
                                                         self.fitresults['a2'],
                                                         self.fitresults['a2_err']))
            if num_exp > 3:
                print(
                "  l3=%.3f +-%.3f ns, a3=%.3e +-%.3e" % (self.fitresults['l3'],
                                                         self.fitresults['l3_err'],
                                                         self.fitresults['a3'],
                                                         self.fitresults['a3_err']))
            if num_exp > 4:
                print(
                "  l4=%.3f +-%.3f ns, a4=%.3e +-%.3e" % (self.fitresults['l4'],
                                                         self.fitresults['l4_err'],
                                                         self.fitresults['a4'],
                                                         self.fitresults['a4_err']))
            print(
            " ")

        self.has_fit = True

    def autocorr(self):
        x = self.residuals()
        result = np.correlate(x, x, mode='full')
        return result[result.size / 2 + 1:] / sum(x ** 2)

    def residuals(self):
        return self.bestfit - self.curves[0]

    def counts_per_second(self):
        """
        Divide by acquisition time (self.Tacq). Note that Tacq is in milliseconds.
        """
        for i, curve in enumerate(self.curves):
            curve = np.array(curve, dtype=np.float)
            curve /= self.Tacq / 1000.0

            self.curves[i] = curve

    def get_max(self):
        """ return a tuple containing the time and height of
            the maximum of curve[0]:

                t_max, cts_max = self.get_max()
        """
        cts_max = self.curves[0].max()
        t_max = self.t[0][np.where(self.curves[0] == cts_max)[0][0]]
        return t_max, cts_max

    def normalize(self, value=None):
        # just a wrapper around normalize_curves
        self.normalize_curves(value=value)

    def normalize_curves(self, value=None):
        """
        Normalize the curve to its maximum value (default),
        or normalize to some arbitrary value (if value != None).
        """
        for i, curve in enumerate(self.curves):
            curve = np.array(curve, dtype=np.float)
            if value is None:
                curve /= curve.max()
            else:
                curve /= np.float(value)

            self.curves[i] = curve

    def plot(self, *args, **kwargs):
        kwargs['type'] = "trace"
        self.plot_misc(*args, **kwargs)

    def plotfit(self, *args, **kwargs):
        kwargs['type'] = "fit"
        self.plot_misc(*args, **kwargs)

    def plotmodel(self, *args, **kwargs):
        kwargs['type'] = "model"
        self.plot_misc(*args, **kwargs)

    def plotresiduals(self, *args, **kwargs):
        kwargs['type'] = "residuals"
        if not 'weighted' in list(kwargs.keys()): kwargs['weighted'] = False
        self.plot_misc(*args, **kwargs)

    def plot_misc(self, *args, **kwargs):
        if kwargs['type'] == "trace":
            data = self.curves[0]
            t = self.t[0]
        elif kwargs['type'] == "fit":
            t = self.t[0].copy()
            if self.deconvolved:
                data = self.bestfit
            else:
                data = self.bestfit
                t = t[np.find(t >= self.fitstart)]
        elif kwargs['type'] == "model":
            data = self.model
            t = self.t[0]
        elif kwargs['type'] == "residuals":
            data = self.residuals()
            if kwargs['weighted']:
                trace_scaling = self.curves[0].max() / self.raw_curves[0].max()
                data /= np.sqrt(self.raw_curves[0] * trace_scaling)  # use raw curves in case BG was subtracted
            del kwargs['weighted']
            t = self.t[0]
        del kwargs['type']

        if 't0' in list(kwargs.keys()):
            t0 = kwargs['t0']
            del kwargs['t0']
        else:
            t0 = 0.0

        if 'semilogy' in list(kwargs.keys()):
            semilogy = kwargs['semilogy']
            del kwargs['semilogy']
        else:
            semilogy = False

        if 'fill' in list(kwargs.keys()):
            fill = kwargs['fill']
            del kwargs['fill']
        else:
            fill = False

        if 'yoffset' in list(kwargs.keys()):
            voffset = kwargs['yoffset']
            del kwargs['yoffset']
        else:
            voffset = 1.0e-5  # makes toggling to semilog okay with fill

        if self.ax is None:
            try:
                self.ax = np.gca()
            except AttributeError:
                f = np.figure(1)
                self.ax = f.add_subplot(111)

        if semilogy:
            self.ax.plot(t + t0, data, *args, **kwargs)
            self.ax.set_yscale('log')
        else:
            if fill:
                self.ax.fill_between(t + t0, data, y2=voffset, *args, **kwargs)
            else:
                self.ax.plot(t + t0, data, *args, **kwargs)
        self.ax.set_xlabel('Time (ns)')
        self.ax.set_ylabel('Intensity (arb. units)')
        np.show()

    def readasciiheader(self, verbose=False):
        """ read this first. """
        ##################################################################################
        #
        # ASCII file header
        #
        ##################################################################################

        self.Ident = self.fobj.read(16).split(b'\x00')[0].decode('ascii')
        if verbose:
            print(self.Ident)

        self.FormatVersion = self.fobj.read(6).split(b'\x00')[0].decode('ascii')  # the join/split deblanks the string
        if verbose:
            print(
            "PHD file format version:", self.FormatVersion)

        if self.FormatVersion != '2.0':
            raise TypeError("PicoQuantUtils.py is only able to load phd file version 2.0. Quitting.")

        self.CreatorName = self.fobj.read(18).split(b'\x00')[0].decode('ascii')
        if verbose:
            print(
            "File created by:", self.CreatorName)

        self.CreatorVersion = self.fobj.read(12).split(b'\x00')[0].decode('ascii')
        if verbose:
            print(
            "Program version:", self.CreatorVersion)

        self.fobjTime = self.fobj.read(18).split(b'\x00')[0].decode('ascii')
        if verbose:
            print(
            "Time of creation:", self.fobjTime)

        self.CRLF = self.fobj.read(2).decode('ascii')
        if verbose:
            print(
            self.CRLF)

        self.Comment = self.fobj.read(256).split(b'\x00')[0].decode('ascii')
        if verbose:
            print(
            "Comment:", self.Comment)

    def readbinaryheader(self, verbose=False):
        """ read this after the ascii header. """

        ##################################################################################
        #
        # Binary file header
        #
        ##################################################################################
        """
            I use the struct module to unpack the binary SPE data.
            Some useful formats for struct.unpack_from() include:
            fmt   c type          python
            c     char            string of length 1
            s     char[]          string (Ns is a string N characters long)
            h     short           integer 
            H     unsigned short  integer
            l     long            integer
            f     float           float
            d     double          float

            precede these with '=' to force usage of standard python sizes,
            not native sizes (to make usage the same on 32 and 64-bit systems)
        """

        binheader = self.fobj.read(208)  # should take up 208 bytes in memory...

        self.NumberOfCurves = struct.unpack_from("=l", binheader, offset=0)[0]
        if verbose:
            print(
            "Number of curves:", self.NumberOfCurves)

        self.BitsPerHistogramBin = struct.unpack_from("=l", binheader, offset=4)[0]
        if verbose:
            print(
            "Bits per histogram bin:", self.BitsPerHistogramBin)

        self.RoutingChannels = struct.unpack_from("=l", binheader, offset=8)[0]
        if verbose:
            print(
            "Number of routing channels:", self.RoutingChannels)

        self.NumberOfBoards = struct.unpack_from("=l", binheader, offset=12)[0]
        if verbose:
            print(
            "Number of boards:", self.NumberOfBoards)

        self.ActiveCurve = struct.unpack_from("=l", binheader, offset=16)[0]
        if verbose:
            print(
            "Active curve:", self.ActiveCurve)

        self.MeasurementMode = struct.unpack_from("=l", binheader, offset=20)[0]
        if verbose:
            print()
            "Measurement mode:", self.MeasurementMode

        self.SubMode = struct.unpack_from("=l", binheader, offset=24)[0]
        if verbose:
            print(
            "Sub mode:", self.SubMode)

        self.RangeNo = struct.unpack_from("=l", binheader, offset=28)[0]
        if verbose:
            print(
            "Range number:", self.RangeNo)

        self.Offset = struct.unpack_from("=l", binheader, offset=32)[0]
        if verbose:
            print(
            "Offset:", self.Offset)

        self.Tacq = struct.unpack_from("=l", binheader, offset=36)[0]
        if verbose:
            print(
            "Acquisition time (ms):", self.Tacq)

        self.StopAt = struct.unpack_from("=l", binheader, offset=40)[0]
        if verbose:
            print(
            "Stop at (counts):", self.StopAt)

        self.StopOnOverflow = struct.unpack_from("=l", binheader, offset=44)[0]
        if verbose:
            print(
            "Stop on overflow:", self.StopOnOverflow)

        self.Restart = struct.unpack_from("=l", binheader, offset=48)[0]
        if verbose:
            print(
            "Restart:", self.Restart)

        self.DispLinLog = struct.unpack_from("=l", binheader, offset=52)[0]
        if verbose:
            print(
            "Display lin/log:", self.DispLinLog)

        self.DispTimeAxisFrom = struct.unpack_from("=l", binheader, offset=56)[0]
        if verbose:
            print(
            "Time axis from (ns):", self.DispTimeAxisFrom)

        self.DispTimeAxisTo = struct.unpack_from("=l", binheader, offset=60)[0]
        if verbose:
            print(
            "Time axis to (ns):", self.DispTimeAxisTo)

        self.DispCountAxisFrom = struct.unpack_from("=l", binheader, offset=64)[0]
        if verbose:
            print(
            "Count Axis From:", self.DispCountAxisFrom)

        offset = 68
        self.DispCountAxisTo = struct.unpack_from("=l", binheader, offset=offset)[0]
        if verbose:
            print(
            "Count Axis To:", self.DispCountAxisTo)

        self.DispCurveMapTo = []
        self.DispCurveShow = []
        for i in range(8):
            offset += 4
            self.DispCurveMapTo.append(struct.unpack_from("=l", binheader, offset=offset)[0])
            offset += 4
            self.DispCurveShow.append(struct.unpack_from("=l", binheader, offset=offset + 4)[0])

        self.ParamStart = []
        self.ParamStep = []
        self.ParamEnd = []
        for i in range(3):
            offset += 4
            self.ParamStart.append(struct.unpack_from("=f", binheader, offset=offset)[0])

            offset += 4
            self.ParamStep.append(struct.unpack_from("=f", binheader, offset=offset)[0])

            offset += 4
            self.ParamEnd.append(struct.unpack_from("=f", binheader, offset=offset)[0])

        offset += 4
        self.RepeatMode = struct.unpack_from("=l", binheader, offset=offset)[0]
        if verbose:
            print(
            "Repeat Mode:", self.RepeatMode)

        offset += 4
        self.RepeatsPerCurve = struct.unpack_from("=l", binheader, offset=offset)[0]
        if verbose:
            print(
            "Repeat / Curve:", self.RepeatsPerCurve)

        offset += 4
        self.RepeatTime = struct.unpack_from("=l", binheader, offset=offset)[0]
        if verbose:
            print(
            "Repeat Time:", self.RepeatTime)

        offset += 4
        self.RepeatWaitTime = struct.unpack_from("=l", binheader, offset=offset)[0]
        if verbose:
            print(
            "Repeat Wait Time:", self.RepeatWaitTime)

        offset += 4
        self.ScriptName = struct.unpack_from("=l", binheader, offset=offset)[0]
        if verbose:
            print(
            "Script Name:", self.ScriptName)

    def readboardheader(self, verbose=False):
        """ read this after the ascii header and the binary header. """

        ##################################################################################
        #
        #          Header for each board
        #
        ##################################################################################

        boardheader = self.fobj.read(156)
        # I don't actually do anything with this at this point. Just get it out of the way...

        """
        for i = 1:NumberOfBoards
        fprintf(1,'-------------------------------------\n') 
        fprintf(1,'            Board No: #d\n', i-1)

        HardwareIdent(:,i) = char(fread(fid, 16, 'char'))
        fprintf(1,' Hardware Identifier: #s\n', HardwareIdent(:,i))

        HardwareVersion(:,i) = char(fread(fid, 8, 'char'))
        fprintf(1,'    Hardware Version: #s\n', HardwareVersion(:,i))    

        HardwareSerial(i) = fread(fid, 1, 'int32')
        fprintf(1,'    HW Serial Number: #d\n', HardwareSerial(i))

        SyncDivider(i) = fread(fid, 1, 'int32')
        fprintf(1,'        Sync divider: #d \n', SyncDivider(i))

        CFDZeroCross0(i) = fread(fid, 1, 'int32')
        fprintf(1,'     CFD 0 ZeroCross: #3i mV\n', CFDZeroCross0(i))

        CFDLevel0(i) = fread(fid, 1, 'int32')
        fprintf(1,'     CFD 0 Discr.   : #3i mV\n', CFDLevel0(i))

        CFDZeroCross1(i) = fread(fid, 1, 'int32')
        fprintf(1,'     CFD 1 ZeroCross: #3i mV\n', CFDZeroCross1(i))

        CFDLevel1(i) = fread(fid, 1, 'int32')
        fprintf(1,'     CFD 1 Discr.   : #3i mV\n', CFDLevel1(i))

        Resolution(i) = fread(fid, 1, 'float')
        fprintf(1,'          Resolution: #2.6g ns\n', Resolution(i))

        # below is new in format version 2.0

        RouterModelCode(i)      = fread(fid, 1, 'int32')
        RouterEnabled(i)        = fread(fid, 1, 'int32')

        # Router Ch1
        RtChan1_InputType(i)    = fread(fid, 1, 'int32')
        RtChan1_InputLevel(i)   = fread(fid, 1, 'int32')
        RtChan1_InputEdge(i)    = fread(fid, 1, 'int32')
        RtChan1_CFDPresent(i)   = fread(fid, 1, 'int32')
        RtChan1_CFDLevel(i)     = fread(fid, 1, 'int32')
        RtChan1_CFDZeroCross(i) = fread(fid, 1, 'int32')
        # Router Ch2
        RtChan2_InputType(i)    = fread(fid, 1, 'int32')
        RtChan2_InputLevel(i)   = fread(fid, 1, 'int32')
        RtChan2_InputEdge(i)    = fread(fid, 1, 'int32')
        RtChan2_CFDPresent(i)   = fread(fid, 1, 'int32')
        RtChan2_CFDLevel(i)     = fread(fid, 1, 'int32')
        RtChan2_CFDZeroCross(i) = fread(fid, 1, 'int32')
        # Router Ch3
        RtChan3_InputType(i)    = fread(fid, 1, 'int32')
        RtChan3_InputLevel(i)   = fread(fid, 1, 'int32')
        RtChan3_InputEdge(i)    = fread(fid, 1, 'int32')
        RtChan3_CFDPresent(i)   = fread(fid, 1, 'int32')
        RtChan3_CFDLevel(i)     = fread(fid, 1, 'int32')
        RtChan3_CFDZeroCross(i) = fread(fid, 1, 'int32')
        # Router Ch4
        RtChan4_InputType(i)    = fread(fid, 1, 'int32')
        RtChan4_InputLevel(i)   = fread(fid, 1, 'int32')
        RtChan4_InputEdge(i)    = fread(fid, 1, 'int32')
        RtChan4_CFDPresent(i)   = fread(fid, 1, 'int32')
        RtChan4_CFDLevel(i)     = fread(fid, 1, 'int32')
        RtChan4_CFDZeroCross(i) = fread(fid, 1, 'int32')

        # Router settings are meaningful only for an existing router:

        if RouterModelCode(i)>0


            fprintf(1,'-------------------------------------\n') 
            fprintf(1,'   Router Model Code: #d \n', RouterModelCode(i))
            fprintf(1,'      Router Enabled: #d \n', RouterEnabled(i))
            fprintf(1,'-------------------------------------\n') 

            # Router Ch1 
            fprintf(1,'RtChan1 InputType   : #d \n', RtChan1_InputType(i))
            fprintf(1,'RtChan1 InputLevel  : #4i mV\n', RtChan1_InputLevel(i))
            fprintf(1,'RtChan1 InputEdge   : #d \n', RtChan1_InputEdge(i))
            fprintf(1,'RtChan1 CFDPresent  : #d \n', RtChan1_CFDPresent(i))
            fprintf(1,'RtChan1 CFDLevel    : #4i mV\n', RtChan1_CFDLevel(i))
            fprintf(1,'RtChan1 CFDZeroCross: #4i mV\n', RtChan1_CFDZeroCross(i))
            fprintf(1,'-------------------------------------\n') 

            # Router Ch2
            fprintf(1,'RtChan2 InputType   : #d \n', RtChan2_InputType(i))
            fprintf(1,'RtChan2 InputLevel  : #4i mV\n', RtChan2_InputLevel(i))
            fprintf(1,'RtChan2 InputEdge   : #d \n', RtChan2_InputEdge(i))
            fprintf(1,'RtChan2 CFDPresent  : #d \n', RtChan2_CFDPresent(i))
            fprintf(1,'RtChan2 CFDLevel    : #4i mV\n', RtChan2_CFDLevel(i))
            fprintf(1,'RtChan2 CFDZeroCross: #4i mV\n', RtChan2_CFDZeroCross(i))
            fprintf(1,'-------------------------------------\n') 

            # Router Ch3
            fprintf(1,'RtChan3 InputType   : #d \n', RtChan3_InputType(i))
            fprintf(1,'RtChan3 InputLevel  : #4i mV\n', RtChan3_InputLevel(i))
            fprintf(1,'RtChan3 InputEdge   : #d \n', RtChan3_InputEdge(i))
            fprintf(1,'RtChan3 CFDPresent  : #d \n', RtChan3_CFDPresent(i))
            fprintf(1,'RtChan3 CFDLevel    : #4i mV\n', RtChan3_CFDLevel(i))
            fprintf(1,'RtChan3 CFDZeroCross: #4i mV\n', RtChan3_CFDZeroCross(i))
            fprintf(1,'-------------------------------------\n') 

            # Router Ch4
            fprintf(1,'RtChan4 InputType   : #d \n', RtChan4_InputType(i))
            fprintf(1,'RtChan4 InputLevel  : #4i mV\n', RtChan4_InputLevel(i))
            fprintf(1,'RtChan4 InputEdge   : #d \n', RtChan4_InputEdge(i))
            fprintf(1,'RtChan4 CFDPresent  : #d \n', RtChan4_CFDPresent(i))
            fprintf(1,'RtChan4 CFDLevel    : #4i mV\n', RtChan4_CFDLevel(i))
            fprintf(1,'RtChan4 CFDZeroCross: #4i mV\n', RtChan4_CFDZeroCross(i))
            fprintf(1,'-------------------------------------\n') 

        end
        end
    """

    def readcurveheaders(self, verbose=False):
        """ read this after the ascii header, the binary header, and the boards header. """

        ##################################################################################
        #
        #                Headers for each histogram (curve)
        #
        ##################################################################################

        MAXCURVES = 512
        binheader = self.fobj.read(150 * MAXCURVES)

        offset = 0
        self.curveheaders = []

        for i in range(self.NumberOfCurves):
            ch = dict()

            ch['CurveIndex'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Curve index:", ch['CurveIndex'])
            offset += 4

            ch['TimeOfRecording'] = struct.unpack_from("=l", binheader, offset=offset)[
                0]  # supposed to be unsigned long...
            if verbose:
                print(
                "Repeat Wait Time:", ch['TimeOfRecording'])
            #  The PicoHarp software saves the time of recording
            #  in a 32 bit serial time value as defined in all C libraries.
            #  This equals the number of seconds elapsed since midnight
            #  (00:00:00), January 1, 1970, coordinated universal time.
            #  The conversion to normal date and time strings is tricky...
            #  In matlab: (but we need it to be a uint32, which it's not, so I won't implement the conversion here)
            #  TimeOfRecording(i) = TimeOfRecording(i)/24/60/60+25569+693960
            #  fprintf(1,'  Time of Recording: #s \n', datestr(TimeOfRecording(i),'dd-mmm-yyyy HH:MM:SS'))
            offset += 4

            ch['HardwareIdent'] = struct.unpack_from("=16s", binheader, offset=offset)[0]
            if verbose:
                print(
                "Repeat Wait Time:", ch['HardwareIdent'])
            offset += 16

            ch['HardwareVersion'] = struct.unpack_from("=8s", binheader, offset=offset)[0]
            if verbose:
                print(
                "Hardware Version:", ch['HardwareVersion'])
            offset += 8

            ch['HardwareSerial'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print("HW Serial Number:", ch['HardwareSerial'])
            offset += 4

            ch['SyncDivider'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Sync divider:", ch['SyncDivider'])
            offset += 4

            ch['CFDZeroCross0'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "CFD 0 ZeroCross (mV):", ch['CFDZeroCross0'])
            offset += 4

            ch['CFDLevel0'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "CFD 0 Discr. (mV):", ch['CFDLevel0'])
            offset += 4

            ch['CFDZeroCross1'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "CFD 1 ZeroCross (mV):", ch['CFDZeroCross1'])
            offset += 4

            ch['CFDLevel1'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "CFD 1 Discr. (mV):", ch['CFDLevel1'])
            offset += 4

            ch['Offset'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Offset:", ch['Offset'])
            offset += 4

            ch['RoutingChannel'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Routing Channel:", ch['RoutingChannel'])
            offset += 4

            ch['ExtDevices'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "External Devices:", ch['ExtDevices'])
            offset += 4

            ch['MeasMode'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Measure mode:", ch['MeasMode'])
            offset += 4

            ch['SubMode'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Sub-Mode:", ch['SubMode'])
            offset += 4

            ch['P1'] = struct.unpack_from("=f", binheader, offset=offset)[0]
            if verbose:
                print(
                "P1:", ch['P1'])
            offset += 4

            ch['P2'] = struct.unpack_from("=f", binheader, offset=offset)[0]
            if verbose:
                print(
                "P2:", ch['P2'])
            offset += 4

            ch['P3'] = struct.unpack_from("=f", binheader, offset=offset)[0]
            if verbose:
                print(
                "P3:", ch['P3'])
            offset += 4

            ch['RangeNo'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Range No.:", ch['RangeNo'])
            offset += 4

            ch['Resolution'] = struct.unpack_from("=f", binheader, offset=offset)[0]
            if verbose:
                print(
                "Resolution (ns):", ch['Resolution'])
            offset += 4

            ch['Channels'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Channels:", ch['Channels'])
            offset += 4

            ch['Tacq'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Acquisition Time (ms):", ch['Tacq'])
            offset += 4

            ch['StopAfter'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Stop After (ms):", ch['StopAfter'])
            offset += 4

            ch['StopReason'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Stop Reason (ms):", ch['StopReason'])
            offset += 4

            ch['InpRate0'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Input Rate 0 (Hz):", ch['InpRate0'])
            offset += 4

            ch['InpRate1'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Input Rate 1 (Hz):", ch['InpRate1'])
            offset += 4

            ch['HistCountRate'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Hist. Count Rate (cps):", ch['HistCountRate'])
            offset += 4

            ch['IntegralCount'] = struct.unpack_from("=2l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Integral Count:", ch['IntegralCount'])
            offset += 8

            ch['Reserved'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Reserved:", ch['Reserved'])
            offset += 4

            ch['DataOffset'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            if verbose:
                print(
                "Data Offset relative to the start of the file:", ch['DataOffset'])
            offset += 4

            # below is new in format version 2.0

            ch['RouterModelCode'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            offset += 4
            ch['RouterEnabled'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            offset += 4
            ch['RtChan_InputType'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            offset += 4
            ch['RtChan_InputLevel'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            offset += 4
            ch['RtChan_InputEdge'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            offset += 4
            ch['RtChan_CFDPresent'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            offset += 4
            ch['RtChan_CFDLevel'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            offset += 4
            ch['RtChan_CFDZeroCross'] = struct.unpack_from("=l", binheader, offset=offset)[0]
            offset += 4

            self.curveheaders.append(ch)

    def readhistograms(self):

        ##################################################################################
        #
        #          Reads all histograms into a list of numpy arrays
        #
        ##################################################################################

        self.fobj.seek(0)  # go back to beginning because 'DataOffset' is measured from there.
        binarydata = self.fobj.read()

        self.curves = []

        for i, curve in enumerate(self.curveheaders):

            # This will typically be waaay too long and will be padded with zeros because it
            # can accomodate up to 2**16 histogram bins but our laser rep rate is ~76MHz, so
            # if you were set at 4ps resolution, that would only require 1/76MHz/4ps ~ 3281 bins
            #
            # It's worth noting that when we wrap the curve (move data from before laser to after),
            # there is going to be some small error in the timing because the number of bins will
            # not be an exact integer. This error will be at most the resolution, which is likely
            # to be either really small compared to the lifetime of the emitter or, if the lifetime
            # is really short, the fluorescence will have decayed before the end of the un-wrapped
            # curve. The only time this could be an issue is if the lifetime is really short and
            # the peak in lifetime occurrs at the very end of the un-wrapped curve. Then you should
            # insert enough BNC cable to bring the peak back toward the front of the un-wrapped curve.

            zeropadded = np.array(
                struct.unpack_from("=" + str(curve['Channels']) + "l", binarydata, offset=curve['DataOffset']),
                dtype=np.int
            )
            nbins = 1.0 / self.curveheaders[0]['InpRate0'] / self.curveheaders[0]['Resolution'] / 1.0e-9
            nfullbins = np.int(np.floor(nbins))
            npartialbins = np.mod(nbins, 1)
            if npartialbins > 0.0:
                # I think in this case (which is almost always the case), the first bin is sometimes
                # the 'partial' bin, and the last bin is sometimes the 'partial' bin. So we'll delete them.
                # (or uncomment other line to add them.)
                ###zeropadded[0] += zeropadded[ nfullbins ] # add the partial bin to the first bin
                self.curves.append(zeropadded[1:nfullbins])
            else:
                self.curves.append(zeropadded[:nfullbins])

        self.raw_curves = self.curves[:]

    def set_axes(self, axes):
        """ this allows you to plot the data to a particular axes
        """
        self.ax = axes

    def zero_except(self, tstart=None, tend=None):
        """ blank curve[0] of a trace except within the given window.
            Useful for removing background and reflections from IRF.
        """
        self.curves[0][np.find(self.t[0] < tstart)] = 0.0
        self.curves[0][np.find(self.t[0] > tend)] = 0.0

    def set_irf(self, irf=None, wraptime=None, dispersion=None):
        """
        The detector response isn't a delta-function, meaning that what
        you measure isn't the true time-dependence of the system you are
        measuring. It's the time dependence of the system convolved with
        the response of the detector. This method sets the measured
        trace of the detector response that will be used to convolve
        the mult-exponential model before fitting (thereby taking this
        convolution into account without doing nearly-impossible
        numerical deconvolution).
        """
        if isinstance(irf, Trace):
            self.irf = irf
        elif type(irf) == str:
            self.irf = Trace(irf)
            if wraptime is not None:
                self.irf.wrapcurves(wraptime)
            elif self.wraptime is not None:
                self.irf.wrapcurves(self.wraptime)

        self.irf_dispersion = dispersion
        if dispersion is not None:
            # this is meant to address chromatic dispersion within the setup
            # (e.g. optical fiber)
            # don't bother with normalization b/c it gets normalized to unit area below anyway.
            # original = self.irf.curves[0].copy()
            # self.irf.curves[0][dispersion:] += original[:-dispersion]
            # self.irf.curves[0][:-dispersion] += original[dispersion:]
            len1 = len(self.irf.curves[0])
            chain_of_three = np.zeros(
                3 * len1)  # stack three curves end-to-end so cspline1d_eval doesn't have to extrapolate beyond data
            chain_of_three[:len1] = self.irf.curves[0][:]
            chain_of_three[len1:2 * len1] = self.irf.curves[0][:]
            chain_of_three[-len1:] = self.irf.curves[0][:]
            g = cspline1d(chain_of_three)
            smoothed = np.zeros(len1)
            std_dev = dispersion / 1000.0
            for t0 in np.linspace(-2 * std_dev, 2 * std_dev, 50):
                weight = np.exp(-t0 ** 2 / 2.0 / std_dev ** 2)
                smoothed += weight * cspline1d_eval(g, self.irf.t[0] - t0, dx=self.irf.t[0][1], x0=-self.irf.t[0][-1])
            self.irf.curves[0] = smoothed

        normalized = self.irf.curves[0].astype(numpy.float) / float(
            sum(self.irf.curves[0]))  # normalize integral to 1, just like delta-function!!!
        self.irf.curves[0] = normalized.copy()

        self.irf_generator = cspline1d(self.irf.curves[0])
        self.irf_dt = self.irf.t[0][1] - self.irf.t[0][0]
        self.irf_t0 = self.irf.t[0][0]

        if False:
            """not sure this matters if we do interpolation
            """
            # difference in degree of binning (e.g. 8ps vs. 4ps is bin difference of 2)
            bin_difference = np.int(self.resolution / self.irf.resolution)
            if bin_difference != 1:
                raise ValueError("Have not yet tested deconvolution with different resolution than detector trace!!!")
                d = self.irf.curves[0]
                detector_binned = np.zeros(len(d) / bin_difference)
                for i in range(len(detector_binned)):
                    detector_binned[i] = sum(d[i * bin_difference: i * bin_difference + bin_difference])

    def wrapcurves(self, time, delete_firstpoints=0, delete_lastpoints=0, use_raw=False):
        """ Odds are, your pulse doesn't start at time 0ns.
            Instead, if your lifetime is comparable to your pulse
            spacing, your data wraps around and at 0ns you're
            actually near the end of the decay tail. This method
            is designed to take the data from before the pulse and
            move it where it should be: at the end.
            Usage:
            self.wrap( time, delete_points=None )
            where time is the threshold: all data earlier than this
            get moved to the end of the scan.

            This does all curves at once (though all my data sets
            seem to only have curve [0] anyway).

            The optional arguments `delete_firstpoints` and
            `delete_lastpoints` is for when the
            first and/or last couple bins have an abnormally low
            number of counts. I think this happens when the time
            resolution of the curve is not at the detector minimum,
            meaning that some binning takes place. If the curve window
            isn't evenly divisible by the bin size, then the first and
            last bins can end up with fewer points. For some reason,
            I've also seen a couple traces where this happened for the
            last two bins, which I don't really understand. Regardless,
            let's just delete the points in question (after assigning the
            rest of the points the proper time delay).
            usage:
            delete_firstpoints=n deletes the first n points of unwrapped trace
            delete_lastpoints=n deletes the last n points of unwrapped trace

            use_raw=False means it will just wrap the data stored in self.curves.
            If you want to ensure that you're using the raw data (for example,
            to enable easy re-wrapping in the HuPlot program), then pass
            use_raw=True
        """
        self.wraptime = time
        if self.irf is not None: self.irf.wrapcurves(self.wraptime)

        if use_raw:
            curves = self.raw_curves[:]
        else:
            curves = self.curves[:]

        for i, curve in enumerate(curves):
            time_per_channel = self.curveheaders[i]['Resolution']  # this is in ns
            points_before_threshold = np.find(time_per_channel * np.arange(len(curve)) < time)
            if len(points_before_threshold) == 0:
                self.curves = curves[:]
                self.t = self.raw_t[:]
                return True

            threshold = points_before_threshold[-1]
            wrapped = np.zeros(len(curve))
            wrapped[-threshold:] = curve[:threshold]
            wrapped[:-threshold] = curve[threshold:]
            self.curves[i] = wrapped
            if delete_firstpoints > 0 or delete_lastpoints > 0:
                shortened_curve = np.zeros(len(curve) - delete_firstpoints - delete_lastpoints)
                shortened_t = np.zeros(len(curve) - delete_firstpoints - delete_lastpoints)

                shortened_curve[:-threshold + delete_firstpoints] = self.curves[i][:-threshold - delete_lastpoints]
                shortened_curve[-threshold + delete_firstpoints:] = self.curves[i][-threshold + delete_firstpoints:]
                self.curves[i] = shortened_curve

                shortened_t[:-threshold + delete_firstpoints] = self.raw_t[i][:-threshold - delete_lastpoints]
                shortened_t[-threshold + delete_firstpoints:] = self.raw_t[i][-threshold + delete_firstpoints:]
                self.t[i] = shortened_t


import matplotlib as mpl
import scipy.fftpack as fftpack
import scipy.signal as signal
from scipy.optimize import curve_fit
#from scipy.signal import savgol_filter

if __name__ == '__main__':
    # example usage:
    os.chdir("/Users/gurudevdutt/Dropbox/Pittsburgh/Lab/Data/g2/")
    #d1 = Trace('microwave_cryo_18K_temp_optical_rabi_150uW_input.phd')  # doesn't actually exist in this directory...
    #d2 = Trace('microwave_cryo_18K_temp_optical_rabi.phd')
    d2 = Trace('microwave_cryo_18K_temp_optical_rabi.phd')
    # d.wrapcurves( 1.17 )
    # d.normalize_curves()
    # d.plot()
    # print numpy.size(d.t[0])
    #x1 = d1.t[0]
    x2 = d2.t[0]
    #z1 = d1.curves[0]
    z2 = d2.curves[0]
    #print(len(z1), len(z2))
    # create 3rd order butterworth filter with passband at 10% of Nyquist frequency
    b, a = signal.butter(3, 0.1)

    #y1=signal.filtfilt(b,a,z1,padlen=100)

    y2=signal.filtfilt(b,a,z2,padlen=100)
    #y2 = z2

    zoomlower  = 2210
    zoomupper = 2240
    # x1_zoom = x1[np.logical_and(x1 >= zoomlower, x1 < zoomupper)]
    # y1_zoom = y1[np.logical_and(x1 >= zoomlower, x1 < zoomupper)]
    x2_zoom = x2[np.logical_and(x2 >= zoomlower, x2 < zoomupper)]
    y2_zoom = y2[np.logical_and(x2 >= zoomlower, x2 < zoomupper)]

    fitlower = 2220
    fitupper =2240
    x2_fitdat = x2[np.logical_and(x2 >= fitlower, x2 < fitupper)]
    y2_fitdat= y2[np.logical_and(x2 >= fitlower, x2 < fitupper)]
    print(len(x2_fitdat), len(y2_fitdat))
    # def my_fitfunc(x,a1,a2,a3,a4,a5):
    #      return (a1 + a2 * np.cos(2*np.pi*(x-a4)/a3) * np.exp(-(x-a4)/a5))
    #
    #popt, pcov = curve_fit(my_fitfunc,x2_fitdat,y2_fitdat,p0=[200,20.0,5.0,2220,100000.0],maxfev=10000)
    #print("Fit parameters:", popt)
    # print("Fit uncertainties:", np.sqrt(np.diag(pcov)))
    x_fit = np.linspace(x2_fitdat[0], x2_fitdat[-1], 300)
    #y_fit = my_fitfunc(x_fit,*popt)
    #

    #use fft to filter
    sig_fft = fftpack.fft(y2_fitdat)
    N = len(x2_fitdat)
    f = fftpack.fftfreq(N, x2_fitdat[1] - x2_fitdat[0])
    power = np.abs(sig_fft)


    # w2[cutoff_idx] = 0
   # fig = plt.figure()
    # concentrate on the positive freq of the fft
    pos_mask = np.where(f > 0)
    freqs = f[pos_mask]
    peak_freq = freqs[power[pos_mask].argmax()]
    psd = power[pos_mask]
    print(('rabi frequency is:', peak_freq))

    # high_freq_fft = sig_fft.copy()
    # cutoff_idx = psd < (psd.max()/5) # np.abs(sample_freq) > peak_freq
    # high_freq_fft[cutoff_idx] = 0
    # filtered_sig = fftpack.ifft(high_freq_fft)
    mpl.rcParams['text.usetex'] = True
    fig, ax = plt.subplots(2,tight_layout='True')
    ax[0].plot(x2_zoom-2215, y2_zoom, 'bo')
    ax[1].plot(freqs[:20],psd[:20],'r.-',label=r'$|I(\omega)|^2$')
    ax[0].legend(loc=0)
    ax[1].legend(loc=0)
    ax[0].set_xlabel(r'Time delay(ns)', fontsize=16)
    ax[0].set_ylabel(r'Counts', fontsize=16)
    ax[1].set_xlabel(r'Frequency(GHz)', fontsize=16)
    ax[1].set_ylabel(r'Power', fontsize=16)
    ax[1].set_xlim(0.0,1.0)
    #os.chdir("/Users/gurudevdutt/Dropbox/Pittsburgh/Lab/Analyzed Data/")
    #fig.savefig("nv1_sample28_optical_rabi.pdf", bbox_inches='tight')

    # fig,axs = plt.subplots(2,2)
    #
    # axs[0,0].plot(x1, y1, 'b-', label='no Pi')
    # axs[0,0].legend()
    # axs[0,1].plot(x2, y2, 'r-', label='Pi')
    # axs[0,1].legend()
    # axs[1, 0].plot(x1_zoom, y1_zoom, 'b-', label='no Pi')
    # axs[1, 0].legend()
    # axs[1,1].plot(x2_zoom, y2_zoom, 'bo', label='Pi')
    # axs[1,1].legend()

    plt.show()
    # use fft to filter
    # w = fftpack.rfft(y1)
    # f = fftpack.rfftfreq(N, x[1] - x[0])
    # spectrum = w ** 2
    #
    # cutoff_idx = spectrum < (spectrum.max() / 5)
    # w2 = w.copy()
    # w2[cutoff_idx] = 0
    #
    # y2 = scipy.fftpack.irfft(w2)
