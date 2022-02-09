from fileinput import filename
from bs4 import BeautifulSoup, SoupStrainer
import requests
from fpdf import FPDF
import os
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import shutil
newmanga = input("Do you want to add a new manga series? (y/n)\n")
newmanganame = ""
if newmanga == "y":
    newmanganame = input("What is the name of the series in the mangafreak url? (Format = 'Examble_Manga')\n")
    os.mkdir(f"{newmanganame}")
    os.mkdir(f"{newmanganame}/Chapter_scrap")
    os.mkdir(f"{newmanganame}/Chapters")
    os.mkdir(f"{newmanganame}/Volumes")
inputvolumes = int(input("How many volumes do you want to create?\n"))
if len(newmanganame) > 1:
    manganame = newmanganame
else:
    manganame = input("What is the name of the manga series folder?\n")
def volume_creator(manganame):
    url = []
    filenamecount = 1
    urlcount = 0
    repeat = input('Wich chapters do you want to combine? (give a range. Example: 1 4. This will combine chapters 1, 2, 3 and 4 into 1 pdf file\n')
    user_list = repeat.split()
    for i in range(len(user_list)):
        user_list[i] = int(user_list[i])
    rangechapterlist = range(user_list[0] , user_list[1] + 1)
    def manga_volume_maker(filename, filenamecount, urlcount): 
        for chapternum in rangechapterlist:
            pagecount = 1
            page = requests.get(url[urlcount])    
            data = page.text
            soup = BeautifulSoup(data, features="html.parser")
            os.mkdir(f"{manganame}/Chapter_scrap/{manganame}_{chapternum}")
            pages = []
            for link in soup.find_all('img'):
                link_src = link["src"]
                if "https://images.mangafreak.net" in link_src:
                    pages.append(link_src)
            img_list = []
            for i in pages:
                response = requests.get(i)
                file = open(f"{manganame}/Chapter_scrap/{manganame}_{chapternum}/page-{pagecount}.png", "wb")
                file.write(response.content)
                file.close()
                image = Image.open(f"{manganame}/Chapter_scrap/{manganame}_{chapternum}/page-{pagecount}.png")
                image1 = image.convert("RGB")
                img_list.append(image1)
                pagecount += 1
            image.save(f"{manganame}/Chapter_scrap/{manganame}_{chapternum}/scrap{filenamecount}.pdf",save_all=True, append_images=img_list)
            imglistlen = len(img_list)
            pages_to_keep = list(range(1, imglistlen+1))
            infile = PdfFileReader(f'{manganame}/Chapter_scrap/{manganame}_{chapternum}/scrap{filenamecount}.pdf', 'rb')
            output = PdfFileWriter()
            for i in pages_to_keep:
                p = infile.getPage(i)
                output.addPage(p)
            with open(f'{manganame}/Chapters/{manganame}_{chapternum}.pdf', 'wb') as f:
                output.write(f)
                shutil.rmtree(f"{manganame}/Chapter_scrap/{manganame}_{chapternum}")
                
            filenamecount += 1
            urlcount += 1
    filename = []
    for i in rangechapterlist:
            urllistinput = f"https://w12.mangafreak.net/Read1_{manganame}_{i}"
            url.append(urllistinput)
            filename.append(f"{manganame}_{i}")
    path, dirs, files = next(os.walk(f"{manganame}/Volumes"))
    volumecount = len(files)       
    manga_volume_maker(filename, filenamecount, urlcount)
    pdfs = []
    if user_list[1] > 1:
        for i in rangechapterlist:
            if i == 0:
                continue
            else:
                pdflocation = f"{manganame}/Chapters/{manganame}_{i}.pdf"
                pdfs.append(pdflocation)
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(f"{manganame}/Volumes/{manganame}_volume_{volumecount + 1}.pdf")
        merger.close() 
    print("PDF file successfully created")   
        

for i in range(0, inputvolumes):
    volume_creator(manganame)