"""Conversion of resistance measurements from platinum thermometers to temperatures values.

This package implements Callendar-Van Dusen equations for converting resistance values measured from
platinum resistors.The implementation and terminology is based on the following resources:

    `IEC 60751, Industrial platinum resistance thermometers and platinum temperature sensors.`
"""
import numpy as np


__all__ = ["temperature2resistance", "resistance2temperature", "r2t", "t2r"]

def _cvd_pos(t, R0, A, B):
    return R0*(1+A*t+B*t**2)

def _cvd_neg(t, R0, A, B, C):
    return R0*(1+A*t+B*t**2+C*(t-100)*t**3)

def temperature2resistance(t, R0=100., A=3.9083e-3, B=-5.775e-7, C=-4.183e-12):
    """Convert temperature to resistance for platinum resistors.
    
    Converts temperature to resistance for platinum resistors by the Callendar Van Dusen equations.

    Arguments
    ---------
    t : float or 1darray
        Temperature to convert to resistance.
    R0 : float, optional
        Resistance at 0C, for example 100ohm for Pt100 or 1000ohm for Pt1000.
    A,B,C : float, optional
        Coefficients for platinum resistors, see e.g. IEC60751.

    Returns
    -------
    1darray
        Resistance values for corresponding temperature. 

    Raises
    ------
    ValueError
        If the temperature is out of bounds for the defined equation.
    """
    if np.any(t<-200) or np.any(t>850):
        raise ValueError(
            "Resistance only defined for temperatures between -200C and 850C.")
    return np.piecewise(t, 
                        [t<0, t>=0],
                        [
                            lambda x: _cvd_neg(x, R0, A, B, C), 
                            lambda x: _cvd_pos(x, R0, A, B)
                        ],
                       )

def resistance2temperature(R, R0=100., A=3.9083e-3, B=-5.775e-7, C=-4.183e-12, precision=3):
    """Convert resistance to temperature for platinum resistors.

    Converts resistance to temperature for platinum resistors by inverting Callendar-Van Dusen equations.

    Arguments
    ---------
    R : float or 1darray
        Resistance to convert to temperature.
    R0 : float, optional
        Resistance at 0C, for example 100ohm for Pt100 or 1000ohm for Pt1000.
    A,B,C : float, optional
        Coefficients for platinum resistors, see e.g. IEC60751.

    Returns
    -------
    1darray
        Temperature values for corresponding resistance. 
    """
    dt = 10**-precision
    t = np.arange(-200, 850+dt, dt)
    t[0] = -200
    t[-1] = 850
    return np.interp(R, temperature2resistance(t), t)


t2r = temperature2resistance
r2t = resistance2temperature