import bitbake
import sdkformatter
from importlib import *

reload(sdkformatter)
reload(bitbake)

build = bitbake.build()
sdkformatter.upload_to_steam(build)
