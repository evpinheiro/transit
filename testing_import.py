
from .venv.standard_workday import *

swImport = StandardWorkday()
sw_list = swImport.importing_standard_workday("sunday", "/home/eder/py-workspace/rostering/atual-domingo")
print(sw_list[0])
