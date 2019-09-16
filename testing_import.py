import workday as wk

sw_list = wk.import_workdays("sunday", "/home/eder/py-workspace/rostering/atual-domingo.csv")
for wkd in sw_list:
    print(wkd.show_workday_description())
