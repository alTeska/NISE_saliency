# development file, later on itti&koch class
import math
import numpy as np
import scipy.signal as signal
import matplotlib.image as mpimg

from .utils import *
from .itti_koch_features import *


class IttiKoch():
    '''
    Itti and Koch main model class.
    Inputs upon init: path to the image, changes to setup dict
    '''
    def __init__(self, path):
        super().__init__()

        # Load The Image
        self.img = mpimg.imread(path)

        self.mapwidth = 64
        self.outer_sigma = [3,6]
        self.inner_sigma = [1,1]

        pass

    def run(self):
        img = self.img

        gabor_kernels = create_gabor_kernels()

        # TODO convert to double if image is uint8

        # determine size and number of Center scales
        mapsize = (round(img.shape[0] * (self.mapwidth / img.shape[1])), self.mapwidth)
        scalars = [1, 2, 3]

        img_scales = downsample_image(img, mapsize[0], self.mapwidth, scalars)

        saliency_maps = []
        saliency_maps_o = []
        saliency_maps_c = []
        for img in img_scales:

            # TODO split to channels & compute salience in each

            # intensity
            intensity = compute_intensity([img])
            color = np.squeeze(compute_color([img]))
            orientation = convolve_kernels(np.squeeze(intensity), gabor_kernels)

            # each channel apply the center surround
            convolution_maps = convolve_receptive_field(intensity, self.inner_sigma, self.outer_sigma)
            convolution_maps_c = convolve_receptive_field(color, self.inner_sigma, self.outer_sigma)
            convolution_maps_o = convolve_receptive_field(orientation, self.inner_sigma, self.outer_sigma)

            # compute saliency map from single feature maps
            saliency_maps.append(compute_saliency_map(convolution_maps, mapsize))
            saliency_maps_c.append(compute_saliency_map(convolution_maps_c, mapsize))
            saliency_maps_o.append(compute_saliency_map(convolution_maps_o, mapsize))

        # sum across scales
        saliency_map = sum(saliency_maps)
        saliency_map_c = sum(saliency_maps_c)
        saliency_map_o = sum(saliency_maps_o)

        # TODO normalize channels
        

        # TODO sum together maps across channels


        return saliency_maps, saliency_map, saliency_maps_o, saliency_map_o, saliency_maps_c, saliency_map_c
