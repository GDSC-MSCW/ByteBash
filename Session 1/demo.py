from Google import Create_Service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import pandas as pd
import io
import os

CLIENT_SECRET_FILE='client_secret_GoogleCloudDemo.json'
API_NAME="drive"
API_VERSION="v3"
SCOPES=['https://www.googleapis.com/auth/drive']

service=Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)




def create_folder():
    folders=['Music', 'Study Material', 'Pictures']
    for i in folders:
        try:
            file_metadata={
                'name':i,
                'mimeType':'application/vnd.google-apps.folder'
                #'parents':[]
            }
   
            service.files().create(body=file_metadata).execute()
            print('Folder '+i+' creation  Successful!')
        except:
            print("An exception occurred, couldn't create the folders")

# create_folder()
    
def store_folder_id():
    print(service.Files.Get("root").Execute())
    
    # root_folder_id="root"
    # query=f"parents='{root_folder_id}"

    # response=service.files().list(q=query).execute()
    # files=response.get('files')
    # nextPageToken=response.get('nextPageToken')

    # while nextPageToken:
    #     response=service.files().list(q=query).execute()
    #     files.extend(response.get('files'))
    #     nextPageToken=response.get('nextPageToken')
    # df=pd.DataFrame(files)
    # print(df)


def upload_files():
    folder_id="1qKgVXRahlcIarjhoQdmbLySclxa7YE13"
    file_names=['sample-3s.mp3']
    mime_types=['audio/mpeg']

    for i,j in zip(file_names,mime_types):
        file_metadata={
            'name':i,
            'parents':[folder_id]
        }

        try:
            media=MediaFileUpload('./file_samples/{0}'.format(i),mimetype=j)
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
        except():
             print("An exception occurred, couldn't upload the files")


# upload_files()


def download_files():
    file_ids=['1t-1L-mHdzqbN6Ek5BVdvz11sDAaZ2BsC']
    file_names=['puppy.jpeg']

    for i,j in zip(file_ids,file_names):
        request= service.files().get_media(fileId=i)
        fh=io.BytesIO()
        downloader=MediaIoBaseDownload(fd=fh,request=request)

        done=False
        while not done:
            status, done= downloader.next_chunk()
            print('Download progress {0}'.format(status.progress()*100))
        fh.seek(0)

        with open(os.path.join('.\\file_samples', j),'wb' ) as f:
            f.write(fh.read())
            f.close()

# download_files()

def copy_files():
    source_file_id='1EvayAfolO7nroSHeUtWvnokpWc9nL5IU'
    folders_id=['1qKgVXRahlcIarjhoQdmbLySclxa7YE13']

    file_metadata={
        'name':'PoemFile',
        'parents':folders_id,
        'starred':True,
        'description':'An english poem'

    }

    # service.files().copy(
    #     fileId=store_folder_id,
    #     body=file_metadata
    # ).execute()

    #file is linked
   

    #file isn't linked

    for i in folders_id:
        file_metadata={
            'name':'PoemFile',
            'parents':[i],
            'starred':True,
            'description':'An english poem'
        }

        service.files().copy(
            fileId=source_file_id,
            body=file_metadata
        ).execute()

# copy_files()


def move_files():
    source_folder_id='1qKgVXRahlcIarjhoQdmbLySclxa7YE13'
    target_folder_id='1GP5zbCDqrpEYLJtV574xi0uLzWkKPzrv'
    query=f"parents= '{source_folder_id}'"

    response=service.files().list(q=query).execute()
    files=response.get('files')
    nextPageToken=response.get('nextPageToken')

    while nextPageToken:
        response=service.files().list(q=query, pageToken=nextPageToken).execute()
        files.extend(response.get('files'))
        nextPageToken=response.get('nextPageToken')

    for f in files:
        if f['mimeType']!='application/vnd.google-apps.folder':
            service.files().update(
                fileId=f.get('id'),
                addParents =target_folder_id,
                removeParents=source_folder_id
            ).execute()

move_files()


