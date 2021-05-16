import bitbake
import sdkformatter
from importlib import *

reload(sdkformatter)
reload(bitbake)


print("*"*40)

build = bitbake.build()
sdkformatter.upload_to_steam(build)
