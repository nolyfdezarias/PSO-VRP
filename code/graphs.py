import os 


files = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) ]
files = [ f for f in files if f.__contains__('.txt')]

versions = ['V1','V2']

files_v0 = [f for f in files if not f.__contains__(versions[0]) and not f.__contains__(versions[1])]
files_v1 = [f for f in files if f.__contains__(versions[0])]
files_v1 = [f for f in files if f.__contains__(versions[1])]

print(files_v0)
