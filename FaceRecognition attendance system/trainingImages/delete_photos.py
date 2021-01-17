import sys
import os

# this program removes all png files in the folder or directory
directory = os.getcwd()
test = os.listdir(directory)

for item in test:
    if item.endswith(".png") or item.endswith(".jpg"):
        os.remove(os.path.join(directory, item))





