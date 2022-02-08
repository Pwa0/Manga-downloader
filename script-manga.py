from fileinput import filename
from bs4 import BeautifulSoup, SoupStrainer
import requests
from fpdf import FPDF
import os
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
newmanga = input("Wil je een nieuwe manga downloaden? (y/n)")
if newmanga == "y":
    newmanganame = input("Wat is de naam van de manga? (Format = 'Examble_Manga')")
    os.mkdir(f"{newmanganame}")
inputvolumes = int(input("Hoeveel volumes wil je downloaden?"))
manganame = input("Wat is de mangas folder file?")

def volume_creator(manganame):
    
    url = []
    filenamecount = 1
    urlcount = 0
    repeat = input('Welke chapter t/m welke chapter wil je in een boek stoppen?')
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
            os.mkdir(f"{manganame}/{manganame}_{chapternum}")
            pages = []
            for link in soup.find_all('img'):
                link_src = link["src"]
                if "https://images.mangafreak.net" in link_src:
                    pages.append(link_src)
            img_list = []
            for i in pages:
                response = requests.get(i)
                file = open(f"{manganame}/{manganame}_{chapternum}/page-{pagecount}.png", "wb")
                file.write(response.content)
                file.close()
                image = Image.open(f"{manganame}/{manganame}_{chapternum}/page-{pagecount}.png")
                image1 = image.convert("RGB")
                img_list.append(image1)
                pagecount += 1
            image.save(f"{manganame}/{manganame}_{chapternum}/scrap{filenamecount}.pdf",save_all=True, append_images=img_list)
            imglistlen = len(img_list)
            pages_to_keep = list(range(1, imglistlen+1))
            infile = PdfFileReader(f'{manganame}/{manganame}_{chapternum}/scrap{filenamecount}.pdf', 'rb')
            output = PdfFileWriter()
            for i in pages_to_keep:
                p = infile.getPage(i)
                output.addPage(p)
            with open(f'{manganame}/{manganame}_{chapternum}/{manganame}_{chapternum}.pdf', 'wb') as f:
                output.write(f)
            filenamecount += 1
            urlcount += 1
    filename = []
    for i in rangechapterlist:
            urllistinput = f"https://w12.mangafreak.net/Read1_{manganame}_{i}"
            url.append(urllistinput)
            filename.append(f"{manganame}_{i}")
    path, dirs, files = next(os.walk(manganame))
    volumecount = len(files)       
    manga_volume_maker(filename, filenamecount, urlcount)
    pdfs = []
    if user_list[1] > 1:
        for i in rangechapterlist:
            if i == 0:
                continue
            else:
                pdflocation = f"{manganame}/{manganame}_{i}/{manganame}_{i}.pdf"
                pdfs.append(pdflocation)
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(f"{manganame}/{manganame}_volume_{volumecount}.pdf")
        merger.close() 
    print("PDF file successfully created")          

for i in range(0, inputvolumes):
    volume_creator(manganame)