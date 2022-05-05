# uavsar_pytools

<img src="https://github.com/SnowEx/uavsar_pytools/blob/main/title_figure.png" width="1600">

Python tools to download and convert binary Uavsar images from the Alaska Satellite Facility and Jet Propulsion Laboratory databases. Developed by Zachary Keskinen and Jack Tarricone with guidance from Dr. Hans Peter Marshall of Boise State University, Micah Johnson with m3works, and Micah Sandusky with m3works.

## Installing

This package is installable with pip. In the terminal enter the following command:

```console
pip install uavsar_pytools
```

## Authorization

You will need a [.netrc file](https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html) in your home directory. This is a special file that stores passwords and usernames to be accessed by programs. If you are already registered at either the alaska satellite facility or jet propulsion laboratory skip step 1. Otherwise:

1. If you need a username and password register at [link](https://search.asf.alaska.edu/). Please ensure you have signed the end user agreement for Uavsar.

2. In a python terminal or notebook enter:
```python
from uavsar_pytools.uavsar_tools import create_netrc
create_netrc()
```

You will be asked to prompted to enter your username and password and a netrc file will be automatically generated for you. This file will be accessed during downloading and searching for Uavsar images. You will only need to generate this file once on your computer.

## Usage

The fundamental class of uavsar_pytools is the `UavsarScene`. This class is used for downloading, unzipping, and converting binary UAVSAR files into Geotiffs in WGS84. In order to use the class you will need to instantiate an instance of the class to hold your specific url and the image data. Please see the included tutorial and code snippet below. After instantiating the class you can call `scene.url_to_tiffs()` to fully download and convert the Uavsar images into analysis ready tiffs. The two required inputs are a url to an ASF or JPL zip file (if looking to download a single image see `UavsarImage` in the included notebooks) and that has been ground referenced (must have a .grd or \_grd in the name) along with a directory that you want to store the image files in.

```python
from uavsar_pytools import UavsarScene
## Example url. Use vertex to find other urls: https://search.asf.alaska.edu/ ##
zip_url = 'https://datapool.asf.alaska.edu/INTERFEROMETRY_GRD/UA/lowman_05208_21019-019_21021-007_0006d_s01_L090_01_int_grd.zip'

## Change this variable to a directory you want to download to ##
image_directory = '~/directory/to/store/images/'

#instantiating an instance of the UavsarScene class.
scene = UavsarScene(url = zip_url, work_dir= image_directory)
scene.url_to_tiffs()
```

You will now have a folder of analysis ready tiff images in WGS84 from the provided url in your specificed work directory.

If you are interested in working with each image's numpy array the class has an `scene.images` property that contains the type, description, and numpy array for each image in the zip file. This is available after running `scene.url_to_tiffs()`.

```python
print(scene.image[0]['type'] # figure out the type of the first image
scene.images[0]['array'] # get the first image numpy array for analysis
```

For quick checks to visualize the data there is also a convenience method `scene.show(i = 1)` that allows you to quickly visualize the first image, or by iterating on i = 2,3,4, etc all the images in the zip file. This method is only available after converting binary images to array with `scene.url_to_tiffs()`.

## Downloading whole collections

Uavsar_pytools can now take a collection name and a start and end date and find, download, and process an entire collection of uavsar images. Collection names can be found at [campaign list](https://api.daac.asf.alaska.edu/services/utils/mission_list). Once you know your campaign name and the date range you can give the package a working directory along with the name and dates and it will do the rest. For example if you want to download all uavsar images for Grand Mesa, Colorado from November 2019 to April 2020 and wanted to save it to your documents folder you would use:

```python
from uavsar_pytools import UavsarCollection
collection = UavsarCollection(collection = 'Grand Mesa, CO', work_dir = '~/Documents/collection_ex/', dates = ('2019-11-01','2020-04-01'))
# to keep binary files use `clean = False`, to download incidence angles with each image use `inc = True`, for only certain pols use `pols = ['VV','HV']`
collection.collection_to_tiffs()
```

Each image pair found will be placed in its own directory with its Alaska Satellite Facility derived name as the directory name. Unlike for UavsarScene this functionality will automatically delete the downloaded binary and zip files after converting them to tiffs to save space.

## Finding URLs for your images

The provided jupyter notebook tutorial in the notebooks folder will walk you through generating a bounding box for your area of interest and finding urls through the [asf_search api](https://github.com/asfadmin/Discovery-asf_search). However if you can also use the [vertex website](https://search.asf.alaska.edu/). After drawing a box and selecting UAVSAR from the platform selection pane (circled in red below) you will get a list of search results. Click on the ground projected image you want to download and right click on the download link (circled in orange below). Select ```copy link``` and you will have copied your relevant zip url.

<img src="https://github.com/SnowEx/uavsar_pytools/blob/main/vertex_example.png">

## Need more help?

The notebook folder in this repository has example notebooks for how to utilize this repository or reach out with questions, features, bugs, or anything else.
