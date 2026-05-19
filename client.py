import xmlrpc.client
import os
import threading as th
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json

proxy = xmlrpc.client.ServerProxy('http://localhost:8000')
name = input("Enter your name: ")

def handlerUpload(file, fileUpload):
    with open(file, 'rb') as readFile:
        fileUpload.append([xmlrpc.client.Binary(readFile.read()), file.split('/')[-1]])

def uploadFile():
    listFile = []
    listThread = []
    done = 'y'

    while done.lower() == 'y':
        Tk().withdraw()
        path = askopenfilename()
        listFile.append(path)
        done = input("Upload file lagi? (y)/(n): ")
    
    fileUpload = []
    for file in listFile:
        t = th.Thread(target=handlerUpload, args=(file, fileUpload))
        listThread.append(t)
    
    for thread in listThread:
        thread.start()
    
    for thread in listThread:
        thread.join()
    
    print(proxy.uploadFile(fileUpload, name))

def handlerDownload(file):
    with open(file[1], 'wb') as writeFile:
        writeFile.write(file[0].data)

def downloadFile(fileDownload):
    listThread = []

    for file in fileDownload:
        t = th.Thread(target=handlerDownload, args=(file, ))
        listThread.append(t)

    for thread in listThread:
        thread.start()

    for thread in listThread:
        thread.join()

def menuDownload():
    no = 1  
    listFile = proxy.listFile()
    
    print("===========================================")
    print("List File")
    print("===========================================")
    for file in listFile:
        print(f"{no}. {file}")
        no += 1
    print("===========================================")
    print("Jika file yang akan di download lebih dari 1")
    print("Penulisan formatnya menggunakan spasi")
    print("*Contoh: 1 2 3")
    print("===========================================")
    
    selectedNo = input("Pilih no file: ")
    while selectedNo == "":
        selectedNo = input("Pilih no file: ")
    selectedNo = selectedNo.split(" ")

    selectedFile = [listFile[int(i) - 1] for i in selectedNo]
    fileDownload = proxy.downloadFile(selectedFile, name)
    downloadFile(fileDownload)

optionExit = 'n'

while optionExit.lower() == 'n':
    print(f"Welcome, {name}!")
    print("===========================================")
    print("1. Upload File")
    print("2. Download File")
    print("0. Exit")
    print("===========================================")
    pilihMenu = int(input("Pilih fitur: "))

    os.system("cls")
    if pilihMenu == 1:
        uploadFile()
    elif pilihMenu == 2:
        menuDownload()
    elif pilihMenu == 0:
        exit()
    else:
        input("Pilihan menu tidak ada, silahkan tekan enter untuk kembali ke menu...")
