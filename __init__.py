import bitbake
import sdkformatter


build = bitbake.build()
sdkformatter.upload_to_steam(build)
