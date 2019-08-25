from __future__ import print_function
import pickle
import os.path
import io,sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import Auth
CLIENT_SECRET_FILE =''

SCOPES = list(sys.argv[1])

if sys.argv[2].endswith('.json'):
    CLIENT_SECRET_FILE = 'client_secret.json'
else:
    print ("Please pass the .json")
    
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE)
credentials = authInst.getCredentials()
service = discovery.build('drive', 'v3', credentials=credentials)

def listAllFiles(size,service):
    '''Using Drive API list all the files in drive pass the size'''
    
    results = service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            # Use only when you need to download all files 
            #downloadFile(service, item['id'],'IMG_2143.JPG')
            
def downloadFiles(service, file_id,filepath):
    '''Using Drive API download all the files. Please call in listAllFiles fuction to download or take File_id and
call saperataly'''
    
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))
        if filepath.endswith('.JPG') or filepath.endswith('.PNG'):
            print ("File type is images ")
        else:
            print ("Doc files ",filepath.endswith('.docx'))
            
def searchFile(service,size,query):
    '''Using Drive API Search the google drive '''
    results = service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))

def uploadFile(service, filename,filepath,mimetype):
    '''Using Drive API upload to google drive '''
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))

def createFolder(service, name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))

#listAllFiles(10)
#createFolder( 'Image')
#downloadFiles('1kVbr4e2DnWPxP4UamcX3r4Or_ABiq9_F','IMG_2143.JPG')
#searchFile(10,"IMG_2143.JPG")
#uploadFile('ENEO0943.jpg','ENEO0943.jpg','image/jpeg')
