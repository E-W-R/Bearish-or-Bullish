## Original Script, app was rewritten in Shiny.

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib
import os
import time
import yfinance as yf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from matplotlib import pyplot as plt


def safari():

    animals = ["Bear","Bull"]
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(1)
    print("Saved images:")

    for animal in animals:

        url = "https://www.google.com/search?tbm=isch&q=" + animal
        driver.get(url)
        time.sleep(3)

        start, end = 1, 250
        for i in range(start,end):
            try:
                driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' % i).click()
                time.sleep(1)
                s = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute("src")
                urllib.request.urlretrieve(s, "Documents/%ss/%s.png" % (animal,i))
                print("%ss/%s.png" % (animal,i))
            except:
                pass

    driver.close()


def mathify():

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
                            r, g, b = pix[i,j]
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
                    bound = height//50
                    for i in range(0,width):
                        regs = [averageColour(lop) for lop in [[pix[i,j+k] for k in range(bound)] for j in range(0,height-bound,bound)]]
                        for r in range(1,len(regs)):
                            if abs(regs[r-1][0]-regs[r][0]) > 50 or abs(regs[r-1][1]-regs[r][1]) > 50 or abs(regs[r-1][2]-regs[r][2]) > 50:
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
                f.write(animal + " " + str(width) + " " + str(height) + " " + s + '\n')
            
            except: continue
        
        f.close()

def duplicate():

    for species in ["Bear", "Bull"]:
        
        print("\n" + species + "s:")

        imgs = os.listdir("Documents/%ss" % species)
        for animal in imgs:

            if animal[0] != ".":

                print(animal)

                img = Image.open("Documents/%ss/%s" % (species, animal))
                img = ImageOps.mirror(img)
                img.save("Documents/%ss/-%s" % (species, animal))


def main():

    root = Tk()
    root.title("Bearish or Bullish?")
    root.configure(background='white')
    root.geometry('800x600')
    txtcol = '#%02x%02x%02x' % (51, 51, 51)

    text = StringVar()
    ticker = Entry(root, width=8, fg=txtcol, bg='white', textvariable=text, justify=CENTER)
    ticker.place(x=400, y=110, anchor=CENTER)
    
    bearMat = []
    f1, f2 = open("Documents/bearCurves.txt", 'r'), open("Documents/bullCurves.txt", 'r')
    fs = {0:f1,1:f2}
    bearMat, bullMat = [], []
    Mats = {0:bearMat,1:bullMat}
    for i in [0,1]:
        animals = fs[i].readlines()
        for animal in animals:
            info = animal.split()
            name, width, height = info[0], int(info[1]), int(info[2])
            curve = [[int(p) for p in s.split(",")] for s in info[3:]]
            Mats[i].append(curve + [(name, width, height)])
            Mats[i].append([[width-L[0],L[1]] for L in curve[::-1]] + [("-" + name, width, height)])
    f1.close()
    f2.close()

    def handler(e):
        try:    img.hide()
        except: pass
        s = text.get()
        stock = yf.Ticker(s).history(period="1y")["Close"]
        L = [stock[i] for i in range(len(stock))]
        l = len(L)
        sAv = sum(L)/l
        least = 1000000000
        leastName = "0.png"
        for curve in Mats[L[-1] > L[0]]:
            name, width, height = curve[-1]
            cAv = sum([p[1] for p in curve])/len(curve)
            ssd = 0
            for p in curve[:-1]:
                ssd += (p[1]-stock[p[0]*(l-1)//width]-(cAv-sAv))**2
            ssd = ssd/len(curve)
            if ssd < least:
                least = ssd
                leastName = name
        
        print(leastName)

        img = Image.open("Documents/" + ["Bears","Bulls"][L[-1] > L[0]] + "/" + leastName)
        fig, ax = plt.subplots()
        width, height = img.size
        img = img.resize((len(L), height*len(L)//width))
        ax.imshow(img)
        ax.plot(L)
        canvas = FigureCanvasTkAgg(fig, master = root)
        canvas.draw()
        canvas.get_tk_widget().place(x=400, y=370, anchor=CENTER)

    root.bind('<Return>', handler)

    lbl = Label(root, text="Bearish or Bullish?", font=("Product Sans", 50), fg=txtcol, bg='white')
    lbl.place(x=400, y=50, anchor=CENTER)

    root.mainloop()

main()
