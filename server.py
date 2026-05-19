from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
from os import listdir
from os.path import isfile, join
import threading as th
import json

def handleDownloader(file, downloader):
    with open(f"file_server/{file}", "rb") as readFile:
        downloader.append([xmlrpc.client.Binary(readFile.read()), file])

def handleUpload(file):
    with open(f"file_server/{file[1]}", "wb") as writeFile:
        writeFile.write(file[0].data)

def read_user_activities():
    try:
        with open("user_activity_log.txt", "r") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}

def save_user_activities(data):
    with open("user_activity_log.txt", "w") as file:
        json.dump(data, file, indent=4)

def log_activity(username, activity_type, nFile):
    data = read_user_activities()
    
    if username not in data:
        data[username] = {"upload": 0, "download": 0, "exit": 0}

    data[username][activity_type] += nFile
    save_user_activities(data)

    return data[username]

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2', )

with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    @server.register_function
    def listFile():
        return [f for f in listdir("file_server") if isfile(join("file_server", f))]

    @server.register_function
    def downloadFile(files, username):
      listThread = []
      downloader = []

      for file in files:
        t = th.Thread(target=handleDownloader, args=(file, downloader, ))
        listThread.append(t)
      
      for thread in listThread:
        thread.start()

      for thread in listThread:
        thread.join()
        
      log_activity(username, "download", len(files))  

      return downloader
        
    @server.register_function
    def uploadFile(fileUpload, username):
      listThread = []

      for file in fileUpload:
        t = th.Thread(target=handleUpload, args=(file, ))
        listThread.append(t)
      
      for thread in listThread:
        thread.start()

      for thread in listThread:
        thread.join()
      
      log_activity(username, "upload", len(fileUpload))  
      return "Upload berhasil"

    print("Server is ready to serve...")
    server.serve_forever()
