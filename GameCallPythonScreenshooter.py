import unreal
from datetime import datetime


@unreal.uclass()
class AutomationLib(unreal.AutomationLibrary):
    pass

datetimeNowSuffix = datetime.now().strftime("%d%m%Y%H%M")
AutomationLib.take_high_res_screenshot(1280, 720, "myFancyPictureAtRuntime"+"_"+datetimeNowSuffix+".png", None, False, False,
                                       unreal.ComparisonTolerance.LOW, "")
