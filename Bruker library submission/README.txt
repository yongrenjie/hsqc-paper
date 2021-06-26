==============================================================================

Raw data and figures for "Increasing Sensitivity and Versatility in NMR
Supersequences with New HSQC-based Modules"

Jonathan R. J. Yong, Alexandar L. Hansen, Eriks Kupce, Tim D. W. Claridge
J. Magn. Reson. 2021, accepted

==============================================================================

Pulse programmes
----------------

All pulse programmes (for Bruker instruments) can be found in the `pp`
directory. They are named according to the 'module codes' described in the
paper, but if this is not clear enough, please refer to the header of the pulse
programme: there is more information there.

Although it is possible to create almost arbitrary NOAH supersequences, we have
only attached a limited subset here. We have been working on a tool which
allows users to choose a set of modules and automatically produces an
appropriate pulse sequence, which will be reported in the near future.


Processing scripts
------------------

All AU programmes and Python scripts for use in TopSpin have been attached in
the `au` and `py` directories respectively.

For NUS acquisition, please note that the attached NUS script is different from
the original `noah_nus.py` script (hence the different name), and will not work
older versions of NOAH pulse programmes (e.g. those found in the SI of previous
publications). It will only work with the pulse programmes attached here. To set
up NUS, please follow these steps:

 1. Set up the NOAH experiment normally without NUS first, with the full value
    for TD1. Don't change any other parameters, such as FnTYPE. Setting FnTYPE
    to 'non-uniform sampling' doesn't work with NOAH experiments.
 
 2. Specify the parameter NUSAmount and then run the command `noah_nus2` in
    TopSpin.

 3. To disable NUS on a dataset where it was previously enabled, run
    `noah_nus2 off`.

Please note that NUS is not compatible with the k-scaling presented in the
paper, and if cnst39 (i.e. k) is set to be greater than 1, the NUS script will
change it to 1 automatically. NUS is also not compatible with the magnitude-mode
('QF') COSY module.