"""Various tests to assess the performance of parfile writing."""
import pint.models.model_builder as mb
import pint.models.parameter as mp
import pint.toa as toa
import astropy.units as u
from pint.residuals import resids
import numpy as np
import numbers
import os, unittest
import test_derivative_utils as tdu
import logging

from pinttestdata import testdir, datadir

os.chdir(datadir)


class TestParfileWriting(unittest.TestCase):
    """This is a unit test class for parfile writing.
    """
    @classmethod
    def setUpClass(self):
        self.parfileB1855 = 'B1855+09_NANOGrav_9yv1.gls.par'
        self.timB1855 = 'B1855+09_NANOGrav_9yv1.tim'
        self.toasB1855 = toa.get_TOAs(self.timB1855, ephem="DE421",
                                      planets=False, include_bipm=False)
        self.modelB1855 = mb.get_model(self.parfileB1855)
        self.out_parfile = 'test_parfile_write.par'

    def test_write(self):
        # change parameter value
        for p in self.modelB1855.params:
            par = getattr(self.modelB1855, p)
            # Change value for 20%
            if isinstance(par.value, numbers.Number):
                ov = par.value
                if isinstance(par, mp.MJDParameter):
                    continue
                else:
                    par.value = ov * 0.8
        self.res = resids(self.toasB1855, self.modelB1855, False).time_resids.to(u.s)
        f = open(self.out_parfile, 'w')
        f.write(self.modelB1855.as_parfile())
        f.close()
        read_model = mb.get_model(self.out_parfile)
        read_res = resids(self.toasB1855, read_model, False).time_resids.to(u.s)
        assert np.all(np.abs(read_res.value - self.res.value) < 1e-15), 'Output parfile did not produce same residuals.'
        for pp in self.modelB1855.params:
            par_ori = getattr(self.modelB1855, pp)
            par_read = getattr(read_model, pp)
            if par_ori.uncertainty_value is not None:
                unc_diff = par_ori.uncertainty_value - par_read.uncertainty_value
                assert np.abs(unc_diff) < 1e-15, pp + 'uncertainty does not keep the precision. at' + str(np.abs(unc_diff)) 
