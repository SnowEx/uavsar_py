import matplotlib.pyplot as plt
import os
from os.path import basename
import numpy as np
import logging

from uavsar_pytools.download.download import download_image, download_zip
from uavsar_pytools.convert.file_control import unzip
from uavsar_pytools.convert.tiff_conversion import grd_tiff_convert
from uavsar_pytools.UavsarImage import UavsarImage

log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(logging.DEBUG)

class UavsarScene():
    """
    Class to handle uavsar zip directories. Methods include downloading and converting images.

    Args:
        url (str): ASF or JPL url to a zip uavsar directory
        work_dir (str): directory to download images into
        overwrite (bool): Do you want to overwrite pre-existing files [Default = False]
        debug (str): level of logging (not yet implemented)

    Attributes:
        zipped_fp (str): filepath to downloaded zip directory. Created automatically after downloading.
        binary_fps (str): filepaths of downloaded binary images. Created automatically after unzipping.
        ann_fp: file path to annotation file. Created automatically after unzipping.
        arr (array): processed numpy array of the image
        desc (dict): description of image from annotation file.
    """

    zipped_fp = None
    ann_fp = None
    binary_fps = []
    images = []

    def __init__(self, url, work_dir, debug = False):
        self.url = url
        self.work_dir = os.path.expanduser(work_dir)
        self.debug = debug


    def download(self, sub_dir = 'tmp/', ann = True):
        """
        Download an uavsar image or zip file from a ASF or JPL url.
        Args:
            download_dir (str): directory to download image to. Will be created if it doesn't exists.
            ann (bool): download associated annotation file? [default = True]
        """
        out_dir = os.path.join(self.work_dir, sub_dir)

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        if self.url.split('.')[-1] == 'zip':
            self.zipped_fp = download_zip(self.url, out_dir)
        else:
            log.warning('UavsarScene for zip files. Using UavsarImage for single images.')

    def unzip(self, in_dir = None, sub_dir = 'tmp/bin_imgs/'):
        """
        Unpack a zipped directory.
        Args:
            in_dir (str): directory to unzip frin
            sub_dir (str): sub-directory in working directory to unzip into
        """
        if not in_dir:
            if not self.zipped_fp:
                log.warning('No known zip file for this scene. Please provide.')
            else:
                in_dir = self.zipped_fp

        out_dir = os.path.join(self.work_dir, sub_dir)

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        self.binary_fps = unzip(in_dir, out_dir)

    def binary_to_tiffs(self, sub_dir = 'tiffs/', binary_dir = None, ann_fp = None):
        """
        Convert a set of binary images to WGS84 geotiffs.
        Args:
            sub_dir (str): sub-directory in working directory to put tiffs
            binary_dir (str): directory containing binary files. Autogenerated from unzipping.
        """
        pols = ['VV','VH','HV','HH']
        if not binary_dir:
            if self.binary_fps:
                binary_fps = self.binary_fps
            if not self.binary_fps:
                Exception('No binary files or directory known')
        else:
            binary_fps = os.listdir(binary_dir)

        out_dir = os.path.join(self.work_dir, sub_dir)

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        if not ann_fp:
            ann_fps = [a for a in binary_fps if '.ann' in a]
            ann_dic = {}
            for pol in pols:
                ann_dic[pol] = [fp for fp in ann_fps if pol in fp][0]
            if not ann_fps:
                log.warning('No annotation file found for binary files.')

        binary_img_fps = [f for f in binary_fps if '.ann' not in f]

        for f in binary_img_fps:
            f_pol = [pol for pol in pols if pol in basename(f)][0]
            ann_fp = ann_dic[f_pol]ß
            desc, array, type = grd_tiff_convert(f, out_dir, ann_fp = ann_fp, overwrite = True)
            self.images.append({'description': desc, 'array':  array, 'type': type})

    def url_to_tiffs(self):
        self.download()
        self.unzip()
        self.binary_to_tiffs()


    def show(self, i):
        """
        Convenience function for checking a few images within the zip file for successful conversion.
        """
        if len(self.images) > i:
            array =self.images[i]['array']
            if len(array.dtype) == 1:
                d = array['real']
            else:
                d = (array['real']**2 + array['imaginary']**2)**0.5
            std_low = np.nanmedian(d) - np.nanstd(d)
            std_high = np.nanmedian(d) + np.nanstd(d)
            plt.imshow(d, vmin = std_low ,vmax = std_high)
            plt.title(os.path.basename(self.url))
            plt.colorbar()
            plt.show()







