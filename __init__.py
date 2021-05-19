import bitbake
import sdkformatter
import plasticscm
from importlib import *

reload(sdkformatter)
reload(bitbake)
reload(plasticscm)

build = bitbake.build()
sdkformatter.upload_to_steam(build)
