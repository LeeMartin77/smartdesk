import urllib.request
import zipfile
import os
from distutils.dir_util import copy_tree
from shutil import copyfile

rootfiles = ["adafruit_ssd1306.mpy", "adafruit_framebuf.mpy"]
rootdirs = [] #eg adafruit_hid

releases_root = 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download'
release_date = '20211015'
release_name = 'adafruit-circuitpython-bundle-7.x-mpy-20211015'
bundle_zip = '/tmp/circuitpythonbundle.zip'
bundle_tmp = '/tmp/circuitpythonbundle'

urllib.request.urlretrieve(
    os.path.sep.join([releases_root, release_date, release_name]) + '.zip',
    bundle_zip
)

with zipfile.ZipFile(bundle_zip, 'r') as zip_ref:
    zip_ref.extractall(bundle_tmp)

for dir in rootdirs:
    copy_tree(
        os.path.sep.join([bundle_tmp, release_name, 'lib', dir]), 
        os.path.sep.join(['.', 'lib', dir])
        )

for file in rootfiles:
    copyfile(
        os.path.sep.join([bundle_tmp, release_name, 'lib', file]),
        os.path.sep.join(['.', 'lib', file])
        )

# Extras
copyfile(
    os.path.sep.join([bundle_tmp, release_name, 'examples', 'font5x8.bin']),
    os.path.sep.join(['.', 'font5x8.bin'])
    )