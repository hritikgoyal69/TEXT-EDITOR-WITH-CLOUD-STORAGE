from os import link, name
import os.path
from tkinter import messagebox
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
import webbrowser
import io

# SCOPES = ['https://www.googleapis.com/auth/drive']
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']

Folder_Name = 'Text-Editor (By-Sourabh)'

def get_Gdrive_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def search(service,query):
    result = []
    response = service.files().list(q=query,spaces='drive',
                                          fields='nextPageToken, files(id, name)').execute()
    
    # print(response)
    for file in response.get('files', []):
        result.append((file["id"], file["name"]))
        # print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
    
    return result
    
def searchFromList(files_list,searchValue,searchFor):
    
    for i in range(len(files_list)):
        if files_list[i][searchFor] == searchValue:
            result = files_list[i][1]
            return result
    
def createFolder(service):
    folder_metadata = {'name':Folder_Name,'mimeType':'application/vnd.google-apps.folder'}
    folder = service.files().create(body=folder_metadata,fields='id').execute()
    folder_id = folder.get('id')
    return folder_id

def upload_files(service,name,folder_id):
    query = "parents in '"+folder_id+"' and trashed = false"
    files_list = search(service,query)
    file_name=searchFromList(files_list,name,1)  #passing 1 to search for name
    if file_name!=None:
        selected = messagebox.askyesno(title="Warning",message="File with the same name is already on drive. Still, do you want to save it on drive along with that?")
        if selected is False:
            return 0
    metadata = {'name':name,'parents':[folder_id]}
    media = MediaFileUpload("./Google_Drive_Files/"+name)
    service.files().create(
        body=metadata,
        media_body= media,
        fields='id'
    ).execute()

def download_files(service,file_id,folder_id):
    request = service.files().get_media(fileId=file_id)
    # file_name = service.files().get(fileId=file_id,fields='files(id, name)')
    query = "parents in '"+folder_id+"' and trashed = false"
    files_list = search(service,query)
    file_name=searchFromList(files_list,file_id,0)  #passing 0 to search for id 
    try:
        fh = io.FileIO(os.path.join("./Google_Drive_Files",file_name), "wb")
    except:
        os.mkdir("./Google_Drive_Files")
        fh = io.FileIO(os.path.join("./Google_Drive_Files",file_name), "wb")
        
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    return file_name
        # print("Download %d%%." % int(status.progress() * 100))
# If modifying these scopes, delete the file token.json.

def main():
    service = get_Gdrive_service()
    query = "mimeType='application/vnd.google-apps.folder' and name='"+Folder_Name+"' and trashed = false"
    response = search(service,query) 
    if response:
        folder_id = response[0][0]
    if len(response)==0:
        folder_id = createFolder(service)
    name='sourabh.txt'
    upload_files(service,name,folder_id)

    # open_files(service,folder_id)
    print("Running")

if __name__ == '__main__':
    main()