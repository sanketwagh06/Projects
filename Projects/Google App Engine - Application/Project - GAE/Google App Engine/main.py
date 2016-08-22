import os
import urllib
import webapp2
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import memcache
from google.appengine.api import files

try:
    files.gs
except AttributeError:
    import gs
    files.gs = gs

SMALLFILESIZE = 10*1024                                 #Maximum size of file that can be stored in memcache
SETMEMCACHE = True                                      #Memcache flag(If true files less than 101KB will be stored in Memcache
BUCKET_PATH= "/gs/bigbloobucket"                        #Path of the bucket./gs tells blobstore to store on google cloud storage
class keymodel(db.Model):                               #Creating a database to store filekeys and their locations
    file_key = db.StringProperty()
    file_path = db.StringProperty()

def keylist():                                          
    return db.Key.from_path('key','keylocation')


class MainHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.response.out.write('<html><body>')


        self.response.out.write("""<form action="%s" method="POST" enctype="multipart/form-data">""" % upload_url)

        self.response.out.write("""Enter the key<input type="text" name="mykey" multiple>""")

        self.response.out.write("""Select the files to be uploaded<input type="file" name="file"></td><td align="left"><input type="submit" name="submit" value="Submit"></td>""")
        self.response.out.write("""</form>""")

        self.response.out.write("""<hr><form action="/check" method="post"><div>Enter the key to be searched<input type="text" name="check"></div><div><input type="submit" name="submit" value="Submit"></div></form><hr>""")

        self.response.out.write("""<hr><form action="/find" method="post"><div>Enter the key to open the file<input type="text" name="find"></div><div><input type="submit" name="submit" value="Submit"></div></form><hr>""")

        self.response.out.write("""<hr><form action="/remove" method="post"><div>Enter the key for the file to be removed<input type="text" name="remove"></div><div><input type="submit" name="submit" value="Submit"></div></form><hr>""")

        self.response.out.write("""<a href="/list">List</a>""")

        self.response.out.write("</body></html>")							#Front Page

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        mykey = self.request.get("mykey")                           #Key
        key1 = keymodel(key_name =mykey, parent=keylist())          #Saving the filenames as keys in database

        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        key1.file_key = str(blob_info.key())
        if blob_info.size <= SMALLFILESIZE and SETMEMCACHE:         #Checking if size of file is less than 101KB and
            memcache.add(key=mykey, value=blob_info)                #if setmemcache is enabled we store the files in
            key1.file_path = "memcache"                             #memcache
            self.response.out.write("</br> File in memcache")
        else:
            self.response.out.write("</br> File in cloud storage.")
            write_path = files.gs.create(BUCKET_PATH+"/"+key1.key().id_or_name(), mime_type='text/plain',
                                     acl='public-read')             #We are creating a file on Google cloud storage and
            with files.open(write_path, 'a') as gsfiles:            #writing the contents of uploaded file to that file
                init = 0                                            #using a buffer.
																	#The name of the file on GCS will be the key entered by the user
                filesize = blob_info.size
                fetchsize = blobstore.MAX_BLOB_FETCH_SIZE - 1
                while init < filesize:								
                    gsfiles.write( blobstore.fetch_data(blob_info, init, init+fetchsize))
                    init = init + fetchsize
            files.finalize(write_path)
            key1.file_path = "cloudstorage"							
            self.response.out.write("File in GCS.</br>")

        key1.put()

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, blob_key):
        blob_key = str(urllib.unquote(blob_key))
        if not blobstore.get(blob_key):
            self.error(404)
        else:
            self.send_blob(blobstore.BlobInfo.get(blob_key), save_as=True)

class CheckHandler(webapp2.RequestHandler):                             #To check if the uploaded exists
    def post(self):
        mykey = self.request.get("check")                               #User Input
        key1 = keymodel.all()                                           #Contains all the keys
        key1.filter('__key__ =', db.Key.from_path("keymodel", mykey, parent=keylist())) #If the entered key exists in database
        if key1.count() == 0:                                                           #count will be greater than 0
          self.response.out.write("Key(%s) does NOT exists." % mykey)                   #If key does not exist count wil be 0
        else:
          self.response.out.write("Key(%s) exists." % mykey)

class FindHandler(blobstore_handlers.BlobstoreDownloadHandler):                              #To check if file exists to display the contents
    def post(self):
        mykey = self.request.get("find")                                                     #UserInput
        key1 = keymodel.all()                                                                #Contains all the keys
        key1.filter('__key__ =', db.Key.from_path("keymodel", mykey, parent=keylist()))      #Check if key exists in database
        if key1.count() == 0:
          self.response.out.write("Key(%s) does NOT exists." % mykey)
        else:
          for i in key1:                                                                     #Check if file is in memcache
            if i.file_path == "memcache":                                                    #if file is in memecache return contents
              blob_info = memcache.get(i.key().id_or_name())
              self.send_blob(blob_info)
            else:
              with files.open(BUCKET_PATH+"/"+i.key().id_or_name(), 'r') as f:               #if file is not memcache file will be in GCS
                buf = f.read(1000000)                                                        #Buffer to read 1000MB
                while buf:                                                                   #buffer contains contents of file
                    self.response.out.write(buf)
                    buf = f.read(1000000)                                                    #Contents of the file are transfered to buffer
              self.response.out.write("From Google Cloud Storage file:" + i.key().id_or_name())

class RemoveHandler(webapp2.RequestHandler):                                                    #To remove the file
    def post(self):                                                                             #Check if file exists in memcache
        mykey = self.request.get("remove")
        key1 = keymodel.all()
        thekey = db.Key.from_path("keymodel", mykey, parent=keylist())
        key1.filter('__key__ =', thekey)
        if key1.count() == 0:
            self.response.out.write("Key(%s) does NOT exists." % mykey)
        else:
            f = db.get(thekey)
        if f.file_path == "memcache":
            memcache.delete(f.key().id_or_name())                                               #Search for key and delete from memcache
        else:
            files.delete(BUCKET_PATH+"/"+f.key().id_or_name())                                  #Search for key and delete from GCS
        db.delete(thekey)                                                                       #Delete the key from database
        self.response.out.write("Key(%s) removed." % mykey)

class ListHandler(webapp2.RequestHandler):                                                      #To display list of all the files present
    def get(self):
        key1 = keymodel.all()
        self.response.out.write("<b>List</b>:</br>")
        for i in key1:
            self.response.out.write(i.key().id_or_name())
            self.response.out.write('</br>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload',UploadHandler),
    ('/check',CheckHandler),
    ('/find',FindHandler),
    ('/remove',RemoveHandler),
    ('/list',ListHandler),
    ('/serve/([^/]+)?', ServeHandler)
], debug=True)
