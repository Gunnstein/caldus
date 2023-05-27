caldus: Platinum Resistor Conversion Python Package
===================================================

Introduction
------------

`caldus` is a user-friendly, robust Python package specifically designed to facilitate the 
conversion between resistance values and temperatures of platinum resistors. It is based on the 
Callender-Van Dusen equations (thus the name `caldus`) and the IEC 60751:2022 standard.


Key Features
------------

1. **Supports Various Platinum Resistors:** The package supports a broad range of platinum resistors including PT100, PT500, PT1000, and more.

2. **Easy to Use:** Simply input the resistance or the temperature and the corresponding value will be returned.

3. **Flexible Integration:** Written in Python, `caldus` can be easily integrated with other Python applications or used for data analysis.


Installation
------------

To install `caldus` from PyPI, run:

.. code-block:: bash

    pip install caldus

To install the latest development version from Github, run:

.. code-block:: bash

    pip install git+https://github.com/gunnstein/caldus.git


Usage
-----

Below is a simple usage example:

.. code-block:: python

    import caldus

    # Convert resistance to temperature
    temp = caldus.resistance2temperature(110)

    # Convert temperature to resistance
    res = caldus.temperature2resistance(25)
    
    # alternatively you can use the wrapper functions `r2t` and `t2r` to achieve the same.
    res = caldus.r2t(110)
    temp = caldus.t2r(25)

    print(temp) # output: ~25.68
    print(res)  # output: ~109


Support and Contribution
------------------------

Please report issues via the GitHub issue tracker. 

To contribute, please fork this repository, make your changes, and issue a pull request.


