
"""
duplicate.py (step 3)

Uses Python Imaging Library to save a mirrored version of each image
in the database.
"""

from PIL import Image, ImageOps
import os

for species in ["Bear", "Bull"]:
    
    print("\n" + species + "s:")

    imgs = os.listdir("Documents/%ss" % species)
    for animal in imgs:

        if animal[0] != ".":

            print(animal)

            img = Image.open("Documents/%ss/%s" % (species, animal))
            img = ImageOps.mirror(img)
            img.save("Documents/%ss/-%s" % (species, animal))
