import os
exe = 'chromedriver.exe'
#if the exe just in current dir
print (os.path.abspath(exe))
# output
# D:\python\note\something.exe

#if we need find it first
for root, dirs, files in os.walk(r'D:\python'):
    for name in files:
        if name == exe:
            print (os.path.abspath(os.path.join(root, name)))

