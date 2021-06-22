import bitbaker_builder
import bitbaker_steamsdkmanager
import versioncontroldata
from importlib import *


reload(bitbaker_steamsdkmanager)
reload(bitbaker_builder)
reload(versioncontroldata)

build = bitbaker_builder.build()
# sdkformatter.upload_to_steam(build)
