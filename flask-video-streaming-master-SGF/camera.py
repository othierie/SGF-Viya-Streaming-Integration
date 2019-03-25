import queue
import threading
import time
from base_camera import BaseCamera
import os
import sched


class DirectoryHandler(object):
    readEvent  = threading.Event()
    streamEvent = threading.Event()
    readQueue = queue.Queue()
    timer = 0

    def findFilesInFolder(self, path, pathList, extension):
        """  Recursive function to find all files of an extension type in a folder (and optionally in all subfolders too)

        path:        Base directory to find files
        pathList:    A list that stores all paths
        extension:   File extension to find
        subFolders:  Bool.  If True, find files in all subfolders under path. If False, only searches files in the specified folder
        """
        #print("find in Folder")
        try:   # Trapping a OSError:  File permissions problem I believe
            for entry in os.scandir(path):
                if entry.is_file() and entry.path.endswith(extension):
                    pathList.append(entry.path)
                else:
                    pass
        except OSError:
            print('Cannot access ' + path +'. Probably a permissions error')

        return pathList

    def operation_read(self): #this will read directories and put them in queue
        self.readEvent.wait()
        while self.readEvent.is_set():
            print("read stream accessed")
            #This should be the same path as you use in the python consumer
            pathList = self.findFilesInFolder("images",list(),"jpg")
            for path in pathList:
                print(path)
                self.readQueue.put(path)

            self.readEvent.clear()


    def operation_stream(self,streamQueue):
        self.streamEvent.wait()
        while self.streamEvent.is_set():
            print("operation stream accessed")
            while not self.readQueue.empty():
                self.timer +=1
                file = self.readQueue.get()
                stream = open(file , 'rb').read()
                streamQueue.put(stream)
                print("value of timer: "+str(self.timer))
                if not "default" in file:
                    print("removing")
                    os.remove(file)
            self.streamEvent.clear()


    def setup(self,streamQueue):

        while True:
            self.timer = 0
            print("begin of loop")
            self.readEvent.set()
            a = threading.Thread(target=self.operation_read)
            a.start()
            a.join()
            time.sleep(1)
            self.streamEvent.set()
            b = threading.Thread(target=self.operation_stream, args=(streamQueue,))
            b.start()
            b.join()
            #time.sleep(self.timer)
            time.sleep(1)
            print("end of loop")



    def run(self, streamQueue):
        setupThread = threading.Thread(target=self.setup, args=(streamQueue,))
        setupThread.start()




class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    #imgs = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    print("hey, i got initiated")

    imgs = None
    streamQueue = queue.Queue()


    @staticmethod
    def frames():

        DirectoryHandler().run(Camera.streamQueue)

        while True:
            files = []
            counter = 0
            while not Camera.streamQueue.empty():
                files.append(Camera.streamQueue.get())


            files = list(set(files))
            Camera.imgs= list(set(files))

            while counter < len(Camera.imgs):

                print("files: "+str(len(files)))

                print(len(Camera.imgs))
                for i in range(len(Camera.imgs)):
                    yield Camera.imgs[i]
                    time.sleep(1)
                    #if(i > 1):

                    counter +=1
                Camera.imgs = []
                print("*******************")
                print(counter)
                print(len(files))








