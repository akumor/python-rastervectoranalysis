#!/usr/bin/env python
import os
import sys
import unittest
sys.path.insert(0, os.path.abspath('..'))
from rastervectoreanalysis import RasterVectorAnalysis
import numpy as np
from osgeo import gdal
from osgeo import gdalconst


class TestRasterVectorAnalysis(unittest.TestCase):
    """
    Tests the method used to parse the CSV file and update the AppDeploymentListFile object.
    """

    def setUp(self):
        """
        Prepare to run test.
        """
        pass

    def tearDown(self):
        """
        Clean up after running test.
        """
        pass

    def test_plot_tif(self):
        """ Tests plot_tif function of the RasterVectorAnalysis class. """
        tif_path = os.path.dirname(os.path.realpath(__file__)) + '/test_data/chesapeaketry_1.tif'
        RasterVectorAnalysis.plot_tif(tif_path, cheap_cloud_mask=None)
        # Create numpy array to use for the cheap_cloud_mask
        source = gdal.Open(tif_path, gdalconst.GA_ReadOnly).ReadAsArray()
        mask = np.zeros(source.shape)
        for (x, y), value in np.ndenumerate(source):
            if source[x, y] > 30000:
                mask[x, y] = 1
        source = None
        RasterVectorAnalysis.plot_tif(tif_path, cheap_cloud_mask=mask)


if __name__ == '__main__':
    unittest.main()
