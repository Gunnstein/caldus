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
    
    Converts temperature to resistance for platinum resistors by the Callendar 
    Van Dusen equations.

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
        If the temperature is out of bounds, i.e (T<-200C) or (T>850C) equation.
    """
    t = np.asfarray(t)
    if np.any(t<-200) or np.any(t>850):
        raise ValueError(
            "Resistance only defined for temperatures between -200C and 850C.")
    R = np.piecewise(t, 
                    [t<0., t>=0.],
                    [
                        lambda x: _cvd_neg(x, R0, A, B, C), 
                        lambda x: _cvd_pos(x, R0, A, B)
                    ],
                    )
    if R.size == 1:
        R = float(R)
    return R


def _solve_cubic(A2, A1, A0):
    """Find real root of a reduced form cubic equation.

    This function takes the coefficients of a cubic equation
    x³ + A2x² + A1x + A0 = 0 and returns its roots by employing
    Cardano's method.

    Parameters
    ----------
    A2, A1, A0 : float or 1darray
        Coefficients of the quadratic, linear and constant term.

    Returns
    -------
    float or 1darray
        Real root of the cubic equation. 
    
    Note
    ----
    This is a partial implementation of Cardano's method for solving a cubic
    equation arising in Ferrari's method for solving the quartic Callendar
    Van Dusen equation over the negative domain. This implementation should
    not be used for other purposes as it is neither stable, accurate or even
    correct for the general case.
    """
    q = A1/3.-A2**2./9.
    r = (A1*A2-3.*A0)/6.-A2**3./27.
    A =np.cbrt(np.abs(r)+np.sqrt(r**2.+q**3.))
    t1 = A-q/A
    return t1-A2/3.

def _solve_quartic(A3, A2, A1, A0):
    """Solve for the relevant root of Callendar-Van Dusen equation.

    This function takes the coefficients of quartic equation
    x⁴ + A3x³ + A2x² +  A1x + A0 = 0 and returns the root that is relevant 
    for solving the Callendar-Van Dusen equation over the netagive domain, i.e.
    t = [-200C, 0C> by employing Ferrari's method.

    Parameters
    ----------
    A3, A2, A1, A0 : float or 1darray
        Coefficients of the cubic, quadratic, linear and constant term.

    Returns
    -------
    float or 1darray
        Relevant root of Callendar-Van Dusen equation. 
        
    Note
    ----
    This is a partial implementation of Ferrari's method for solving the quartic 
    Callendar Van Dusen equation over the negative domain. This implementation 
    should not be used for other purposes as it is neither stable, accurate or 
    even correct for the general case.
    """
    C = A3/4.
    b = [A0-A1*C+A2*C**2.-3.*C**4., A1-2.*A2*C+8.*C**3., A2-6.*C**2.]
    m = _solve_cubic(b[2], b[2]**2./4.-b[0], -b[1]**2./8.)
    R = -np.sqrt(m**2.+b[2]*m+b[2]**2./4.-b[0])
    return np.sqrt(m/2)-C-np.sqrt(-m/2.-b[2]/2.-R)


def _inv_cvd_pos(R, R0, A, B):
    a = A/B
    b = (1-R/R0)/B
    return 0.5*(-a-np.sqrt(a**2-4*b))
    

def _inv_cvd_neg(R, R0, A, B, C):
    t = _solve_quartic(-100., B/C, A/C, 1/C*(1-R/R0))
    return t
    

def resistance2temperature(R, R0=100., A=3.9083e-3, B=-5.775e-7, C=-4.183e-12):
    """Convert resistance to temperature for platinum resistors.

    Converts resistance to temperature for platinum resistors by inverting Callendar-Van Dusen equations.
    This method uses Ferrari's method to solve the cubic equation.

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
        
    Raises
    ------
    ValueError
        If the temperature is out of bounds, i.e (t<-200C) or (t>850C) equation.
    """
    R = np.asfarray(R)
    if np.any(R<_cvd_neg(-200, R0, A, B, C)) or np.any(R>_cvd_pos(850, R0, A, B)):
        raise ValueError(
            "Resistance only defined for temperatures between -200C and 850C.")
    t = np.piecewise(R, 
                    [R<R0, R>=R0],
                    [
                        lambda x: _inv_cvd_neg(x, R0, A, B, C),
                        lambda x: _inv_cvd_pos(x, R0, A, B), 
                    ],
                    )
    if t.size == 1:
        t = float(t)
    return t


t2r = temperature2resistance
r2t = resistance2temperature