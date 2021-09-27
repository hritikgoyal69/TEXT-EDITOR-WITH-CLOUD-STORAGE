from os import mkdir
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
import tkinter
from Gdrive import *

Folder_Name = 'Text-Editor (By-Sourabh)'
def new_file(text):
    text.delete(0.0,END)

def open_file(text):
    file1 = filedialog.askopenfile(mode='r')
    data = file1.read()
    text.delete(0.0,END)
    text.insert(0.0,data)

def save_file(text):
    filename = "Untitled.txt"
    data = text.get(0.0,END)
    file1 = open(filename, mode='w')
    file1.write(data)

def save_as(text):
    file1 = filedialog.asksaveasfile(mode='w')
    data = text.get(0.0,END)
    print(file1)
    file1.write(data)
    # for i in range(len(file1.name)-1,0,-1):
    #     if file1.name[i] is '/':
    #         return file1.name[i+1:]

def open_from_drive(text):
    service = get_Gdrive_service()
    query = "mimeType='application/vnd.google-apps.folder' and name='"+Folder_Name+"' and trashed = false"
    response = search(service,query) 
    if response:
        folder_id = response[0][0]
    if len(response)==0:
        folder_id = createFolder(service)
    
    webbrowser.open("https://drive.google.com/drive/folders/"+folder_id)
    file_id = simpledialog.askstring("Open Google Drive File","Enter Your File ID of Google Drive")
    file_name = download_files(service,file_id,folder_id)
    file1 = open('./Google_Drive_Files/'+file_name,mode='r')
    data = file1.read()
    text.delete(0.0,END)
    text.insert(0.0,data)
    file1.close()

    
    


def save_to_drive(text):
    service = get_Gdrive_service()
    query = "mimeType='application/vnd.google-apps.folder' and name='"+Folder_Name+"' and trashed = false"
    response = search(service,query) 
    if response:
        folder_id = response[0][0]
    if len(response)==0:
        folder_id = createFolder(service)
    
    # get input user for file to check it on drive
    # filename = filedialog.asksaveasfilename(confirmoverwrite=False)
    filename = simpledialog.askstring("Save File on Google Drive","Enter Your File Name To Save.")
    data = text.get(0.0,END)
    file = open('./Google_Drive_Files/'+filename,mode='w')
    file.write(data)
    file.close()
    # name = save_as(text)
    # name = simpledialog.askstring("File Name?","Enter Your File name with extension to save on Google Drive")
    if filename is not '':
        upload_files(service,filename,folder_id)
        
    else:
        messagebox.showinfo("Error !!","You had not entered any name !!!", icon='info')






# filename = filedialog.asksaveasfilename(confirmoverwrite=False)
#     print(filename)
#     data = text.get(0.0,END)
#     print(data)
    # try:
    #     file1 = open(filename,'r')
    #     file1.close()
    #     print("yes")
    #     messagebox.showerror("Error !!","File with this name already exists.")
    # except:
    #     file1 = open(filename,'w')
    #     data = text.get(0.0,END)
    #     file1.write(data)
    #     file1.close()
    #     messagebox.showerror("Done","New File with this name created.")
        
    # file1 = filedialog.asksaveasfile(mode='w')
    # data = text.get(0.0,END)
    # print(file1)
    # file1.write(data)
    # for i in range(len(file1.name)-1,0,-1):
    #     if file1.name[i] is '/':
    #         return file1.name[i+1:]