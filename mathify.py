
"""
mathify.py (step 2)

Uses os and Python Imaging Library to open each image of a bear or bull
which is then analyzed to determine at where the back of the animal is.
The information is written to a file.
"""


from PIL import Image
import os


for species in ["Bear", "Bull"]:

    print("\n" + species + "s:")

    f = open("Documents/%sCurves.txt" % species.lower(), 'w')

    imgs = os.listdir("Documents/%ss" % species)

    def isBear(r,g,b):
        total = r + g + b + 1
        return 0.35 <= r/total <= 0.7 and 0.2 <= g/total <= 0.35 \
            and 0.2 <= b/total <= 0.4 and total <= 720 or total <= 200

    for animal in imgs:

        try:

            print(animal)

            im = Image.open("Documents/%ss/%s" % (species, animal))
            width, height = im.size
            pix = im.load()

            B = [[False for j in range(height)] for i in range(width)]

            if species == "Bear":
                for i in range(width):
                    for j in range(height):
                        r, g, b = pix[i, j]
                        if isBear(r, g, b):
                            B[i][j] = True

            def averageColour(lop):
                r, g, b = 0, 0, 0
                for p in lop:
                    r, g, b = r + p[0], g + p[1], b + p[2]
                r, g, b = r/len(lop), g/len(lop), b/len(lop)
                return r, g, b

            curve = []
            if species == "Bull":
                bound = height // 50
                for i in range(0,width):
                    regs = [averageColour(lop) for lop in [[pix[i,j+k]
                    for k in range(bound)] for j in range(0,height-bound,bound)]]
                    for r in range(1,len(regs)):
                        if abs(regs[r-1][0]-regs[r][0]) > 50 or \
                        abs(regs[r-1][1]-regs[r][1]) > 50 or \
                        abs(regs[r-1][2]-regs[r][2]) > 50:
                            curve.append([i,r*bound])
                            break

            if species == "Bear":
                bound = height//18
                for i in range(bound,width-bound,width//100):
                    for j in range(height-bound):
                        if B[i][j]:
                            total = 0
                            for wshift in range(-bound,bound,max(bound//10,2)):
                                for hshift in range(0,bound,max(bound//20,1)):
                                    total += B[i + wshift][j + hshift]
                            if total > 0.8 * min(400,bound**2):
                                curve.append([i,j])
                                break
            s = " ".join([str(L[0]) + "," + str(L[1]) for L in curve])
            f.write("%s %s %s %s\n" % (animal, width, height, s))
        
        except: continue
    
    f.close()
