from __future__ import print_function
import unittest
import pickle
import os.path
import io,sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ''
CLIENT_SECRET_FILE =''

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.service = service
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

            self.service = build('drive', 'v3', credentials=creds)
            return self.service
        

    def test_listAllFiles(self.service, size):
        '''Using Drive API list all the files in drive pass the size'''
        
        results = self.service.files().list(
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
                
    def test_downloadFiles(self.service, file_id,filepath):
        '''Using Drive API download all the files. Please call in listAllFiles fuction to download or take File_id and
    call saperataly'''
        
        request = self.service.files().get_media(fileId=file_id)
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
                
    def test_searchFile(self.service,size,query):
        '''Using Drive API Search the google drive '''
        results = self.service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(item)
                print('{0} ({1})'.format(item['name'], item['id']))

    def test_uploadFile(self.service, filename,filepath,mimetype):
        '''Using Drive API upload to google drive '''
        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath,
                                mimetype=mimetype)
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))

    def test_createFolder(self.service, name):
        file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.service.files().create(body=file_metadata,
                                            fields='id').execute()
        print ('Folder ID: %s' % file.get('id'))

if __name__ == '__main__':
    unittest.main()

    #listAllFiles(10)
    #createFolder( 'Image')
    #downloadFiles('1kVbr4e2DnWPxP4UamcX3r4Or_ABiq9_F','IMG_2143.JPG')
    #searchFile(10,"IMG_2143.JPG")
    #uploadFile('ENEO0943.jpg','ENEO0943.jpg','image/jpeg')
