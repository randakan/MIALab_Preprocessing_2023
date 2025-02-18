"""The pre-processing module contains classes for image pre-processing.

Image pre-processing aims to improve the image quality (image intensities) for subsequent pipeline steps.
"""
import warnings

import pymia.filtering.filter as pymia_fltr
import SimpleITK as sitk
import numpy as np


class ImageNormalization(pymia_fltr.Filter):
    """Represents a normalization filter."""

    def __init__(self):
        """Initializes a new instance of the ImageNormalization class."""
        super().__init__()

    def execute(self, image: sitk.Image, params: pymia_fltr.FilterParams = None) -> sitk.Image:
        """Executes a normalization on an image.

        Args:
            image (sitk.Image): The image.
            params (FilterParams): The parameters (unused).

        Returns:
            sitk.Image: The normalized image.
        """

        img_arr = sitk.GetArrayFromImage(image)

        # todo: normalize the image using numpy
        img_arr = (img_arr - np.min(img_arr)) / (np.max(img_arr) - np.min(img_arr))

        # warnings.warn('No normalization implemented. Returning unprocessed image.')

        img_out = sitk.GetImageFromArray(img_arr)
        img_out.CopyInformation(image)

        return img_out

    def __str__(self):
        """Gets a printable string representation.

        Returns:
            str: String representation.
        """
        return 'ImageNormalization:\n' \
            .format(self=self)


class SkullStrippingParameters(pymia_fltr.FilterParams):
    """Skull-stripping parameters."""

    def __init__(self, img_mask: sitk.Image):
        """Initializes a new instance of the SkullStrippingParameters

        Args:
            img_mask (sitk.Image): The brain mask image.
        """
        self.img_mask = img_mask


class SkullStripping(pymia_fltr.Filter):
    """Represents a skull-stripping filter."""

    def __init__(self):
        """Initializes a new instance of the SkullStripping class."""
        super().__init__()

    def execute(self, image: sitk.Image, params: SkullStrippingParameters = None) -> sitk.Image:
        """Executes a skull stripping on an image.

        Args:
            image (sitk.Image): The image.
            params (SkullStrippingParameters): The parameters with the brain mask.

        Returns:
            sitk.Image: The normalized image.
        """
        mask = params.img_mask  # the brain mask

        # todo: remove the skull from the image by using the brain mask
        mask = sitk.Cast(mask, sitk.sitkUInt8)
        image = sitk.Mask(image, mask)

        # warnings.warn('No skull-stripping implemented. Returning unprocessed image.')

        return image

    def __str__(self):
        """Gets a printable string representation.

        Returns:
            str: String representation.
        """
        return 'SkullStripping:\n' \
            .format(self=self)


class ImageRegistrationParameters(pymia_fltr.FilterParams):
    """Image registration parameters."""

    def __init__(self, atlas: sitk.Image, transformation: sitk.Transform, is_ground_truth: bool = False):
        """Initializes a new instance of the ImageRegistrationParameters

        Args:
            atlas (sitk.Image): The atlas image.
            transformation (sitk.Transform): The transformation for registration.
            is_ground_truth (bool): Indicates weather the registration is performed on the ground truth or not.
        """
        self.atlas = atlas
        self.transformation = transformation
        self.is_ground_truth = is_ground_truth


class ImageRegistration(pymia_fltr.Filter):
    """Represents a registration filter."""

    def __init__(self):
        """Initializes a new instance of the ImageRegistration class."""
        super().__init__()

    def execute(self, image: sitk.Image, params: ImageRegistrationParameters = None) -> sitk.Image:
        """Registers an image.

        Args:
            image (sitk.Image): The image.
            params (ImageRegistrationParameters): The registration parameters.

        Returns:
            sitk.Image: The registered image.
        """

        # todo: replace this filter by a registration. Registration can be costly, therefore, we provide you the
        #  transformation, which you only need to apply to the image!

        # warnings.warn('No registration implemented. Returning unregistered image')

        atlas = params.atlas
        transform = params.transformation
        is_ground_truth = params.is_ground_truth  # the ground truth will be handled slightly different

        """image = sitk.Resample(image1=image, referenceImage=atlas, transform=transform,
                              interpolator=sitk.sitkNearestNeighbor)  # """

        if is_ground_truth:
            image = sitk.Resample(image1=image, transform=transform,
                                  interpolator=sitk.sitkNearestNeighbor,
                                  defaultPixelValue=0.0, outputPixelType=image.GetPixelIDValue())
        else:
            # FIXME : using "referenceImage = atlas," gives error for not matching shapes in ITK-SNAP
            image = sitk.Resample(image1=image, transform=transform,
                                  interpolator=sitk.sitkBSpline,
                                  defaultPixelValue=0.0, outputPixelType=image.GetPixelIDValue())  # """

        # note: if you are interested in registration, and want to test it, have a look at
        # pymia.filtering.registration.MultiModalRegistration. Think about the type of registration, i.e.
        # do you want to register to an atlas or inter-subject? Or just ask us, we can guide you ;-)
        return image

    def __str__(self):
        """Gets a printable string representation.

        Returns:
            str: String representation.
        """
        return 'ImageRegistration:\n' \
            .format(self=self)


class FilteringParameters(pymia_fltr.FilterParams):
    """Skull-stripping parameters."""

    def __init__(self, atlas: sitk.Image):
        """Initializes a new instance of the SkullStrippingParameters

        Args:
            atlas (sitk.Image): The brain mask image.
        """
        self.atlas = atlas


class Filtering(pymia_fltr.Filter):
    """Represents a preprocessing filter."""

    def __init__(self):
        """Initializes a new instance of the filtering class."""
        super().__init__()

    def execute(self, image: sitk.Image, params: FilteringParameters = None) -> sitk.Image:
        """Executes a filtering on an image.

        Args:
            image (sitk.Image): The image.
            params (FilteringParams): The parameters for the filter.

        Returns:
            sitk.Image: The filtered image.
        """

        """meanfilter = sitk.MeanImageFilter()
        meanfilter.SetRadius(1)
        image = meanfilter.Execute(image)"""
        """
        # Create referece for Histogrammatching
        atlas = params.atlas
        atlas_image = sitk.Cast(atlas, sitk.sitkFloat64)

        meanfilter = sitk.MeanImageFilter()
        meanfilter.SetRadius(1)
        #image = meanfilter.Execute(image)

        gaussian = sitk.SmoothingRecursiveGaussianImageFilter()
        gaussian.SetSigma(float(0.5))
        image = gaussian.Execute(image)

        normfilter = sitk.NormalizeImageFilter()
        #image = normfilter.Execute(image)

        hist_matching_filter = sitk.HistogramMatchingImageFilter()
        hist_matching_filter.SetNumberOfHistogramLevels(256)
        hist_matching_filter.SetNumberOfMatchPoints(7)
        #image = hist_matching_filter.Execute(image=image, referenceImage=atlas_image)
        """
        #print("using bilateral filter")
        #bilatfilter = sitk.BilateralImageFilter()
        #bilatfilter.SetRadius(1)
        #image = bilatfilter.Execute(image)
        #print("usiBLUBr")

        # TODO : add random noise?

        """ 2023-12-13-09-09-31 
        grayscaleConnClosingFilter = sitk.GrayscaleConnectedClosingImageFilter()
        image = grayscaleConnClosingFilter.Execute(image)
        """

        """ 2023-12-13-10-14-16
        fillholeImageFilter = sitk.GrayscaleFillholeImageFilter()
        image = fillholeImageFilter.Execute(image)"""

        """ 2023-12-13-10-37-00
        grayscaleOpening = sitk.GrayscaleMorphologicalOpeningImageFilter()
        image = grayscaleOpening.Execute(image)  # """

        """ 2023-12-13-13-36-54
        grayscaleClosing = sitk.GrayscaleMorphologicalClosingImageFilter()
        image = grayscaleClosing.Execute(image)  # """

        """ 2023-12-13-09-45-13
        minMaxCurvatureFilter = sitk.MinMaxCurvatureFlowImageFilter()
        image = minMaxCurvatureFilter.Execute(image)"""

        """# seems almost like bilateral?
        # 2023-12-13-11-07-01 (default), 2023-12-13-14-04-13 (numOfIterations = 10)
        curvatureFlowImageFilter = sitk.CurvatureFlowImageFilter()
        curvatureFlowImageFilter.SetNumberOfIterations(10)
        image = curvatureFlowImageFilter.Execute(image)  # """

        """# took too long ... (Alpha 0.5, Beta 0.5, Radius 20), 2023-12-13-15-04-31 (Alpha 0.5, Beta 0.5, Radius 5)
        adaptiveHistoEqual = sitk.AdaptiveHistogramEqualizationImageFilter()
        adaptiveHistoEqual.SetAlpha(0.5)
        adaptiveHistoEqual.SetBeta(0.5)
        adaptiveHistoEqual.SetRadius(10)
        image = adaptiveHistoEqual.Execute(image)  # """

        """#  2023-12-17-08-56-12 
        sharpenImgFilter = sitk.LaplacianSharpeningImageFilter()
        image = sharpenImgFilter.Execute(image)  # """

        return image

    def __str__(self):
        """Gets a printable string representation.

        Returns:
            str: String representation.
        """
        return 'Filtering:\n' \
            .format(self=self)

