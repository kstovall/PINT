#!/usr/bin/python
from __future__ import absolute_import

import unittest
import numpy as np
import os
import pint.models
import pint.toa
from pint.residuals import resids
from pinttestdata import testdir, datadir

from astropy import units as u

parfile = os.path.join(datadir, 'NGC6440E.par')
timfile = os.path.join(datadir, 'zerophase.tim')

class TestAbsPhase(unittest.TestCase):
    def test_phase_zero(self):
        # Check that model phase is 0.0 for a TOA at exactly the TZRMJD
        model = pint.models.get_model(parfile)
        toas = pint.toa.get_TOAs(timfile)

        ph = model.phase(toas,abs_phase=True)
        # Check that integer and fractional phase values are very close to 0.0
        self.assertAlmostEqual(ph[0].value,0.0)
        self.assertAlmostEqual(ph[1].value,0.0)


