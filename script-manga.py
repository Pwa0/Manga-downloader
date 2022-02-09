from bs4 import BeautifulSoup
import requests
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
if inputvolumes > 0:
    if len(newmanganame) > 1:
        manganame = newmanganame
    else:
        manganame = input("What is the name of the manga series folder?\n")
else:
    print("0 or lower is an invalid input")

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
            pngloc = f"{manganame}/Chapter_scrap/{manganame}_{chapternum}/page-{pagecount}.png"
            pdfloc = f"{manganame}/Chapter_scrap/{manganame}_{chapternum}/scrap{filenamecount}.pdf"
            pdfchapfinal = f"{manganame}/Chapters/{manganame}_{chapternum}.pdf"
            pngscrap = f"{manganame}/Chapter_scrap/{manganame}_{chapternum}"
            page = requests.get(url[urlcount])    
            data = page.text
            soup = BeautifulSoup(data, features="html.parser")
            os.mkdir(f"{pngscrap}")
            pages = []
            for link in soup.find_all('img'):
                link_src = link["src"]
                if "https://images.mangafreak.net" in link_src:
                    pages.append(link_src)
            img_list = []
            for i in pages:
                response = requests.get(i)
                file = open(f"{pngloc}", "wb")
                file.write(response.content)
                file.close()
                image = Image.open(f"{pngloc}")
                image1 = image.convert("RGB")
                img_list.append(image1)
                pagecount += 1
            image.save(f"{pdfloc}",save_all=True, append_images=img_list)
            imglistlen = len(img_list)
            pages_to_keep = list(range(1, imglistlen+1))
            infile = PdfFileReader(f'{pdfloc}', 'rb')
            output = PdfFileWriter()
            for i in pages_to_keep:
                p = infile.getPage(i)
                output.addPage(p)
            with open(f'{pdfchapfinal}', 'wb') as f:
                output.write(f)
                shutil.rmtree(f"{pngscrap}")
            filenamecount += 1
            urlcount += 1
    filename = []
   

    for i in rangechapterlist:
            urllistinput = f"https://w12.mangafreak.net/Read1_{manganame}_{i}"
            url.append(urllistinput)
            filename.append(f"{manganame}_{i}")
    path, dirs, files = next(os.walk(f"{manganame}/Volumes"))
    volumecount = len(files)       
    if user_list[0] > 0 and user_list[1] > 0:
        manga_volume_maker(filename, filenamecount, urlcount)
    else: 
        print("0 or lower is an invalid input")
        exit()
    pdfs = []
    print(user_list)
    for i in rangechapterlist:
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
