#!/usr/bin/env python
__author__ = 'deddu'

import time, datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler



class GlobusFileWatcherHandler(PatternMatchingEventHandler):
    def on_any_event(self, event):
        thefiles.append({"type":event.event_type,
                         "src_path":event.src_path, #file/dir generating the event
                         "dest_path": event.dest_path if event.event_type=="moved" else None  # only moving files has a source and a destination.
        })

def addremotes(files_dict,remote):
    from os.path import join, dirname
    for f in files_dict:
        f['remote_path'] = remote + f['src_path'] #make sure it works as expected for relative/absolute paths.
    return files_dict

def process(files,trans_api, ep1="ep1",ep2="ep2"):
      '''
      process the different files for the different events they registered.
      '''
      from api_interface import transfer,delete,move
      # define few filter predicates
      def modified_or_created(x):
          return x.get('type') in ["modified","created"]
      def deleted(x):
          return x.get('type')=="deleted"
      def moved(x):
          return x.get('type')=="moved"

      totransfer = filter(modified_or_created, thefiles)
      todel = filter(deleted,thefiles)
      tomove = filter(moved,thefiles)

      if totransfer:
        _,_,data = trans_api.submission_id()
        subid = data['value']
        task=transfer([x['src_path'] for x in totransfer],[x['remote_path'] for x in totransfer],ep1,ep2, subid)
        print "READY TO SUBMIT TASK: -----------\n",task.as_json()
        code,reason,data=transfer_api_client.transfer(task)

        print "code:\t{0}\nreason:\t{1}\ndata:\t{2}".format(code,reason,data)
      if todel:
        _,_,data = trans_api.submission_id()
        subid = data['value']
        task=delete([x['src_path'] for x in todel],ep1,ep2,subid)
        code,reason,data=transfer_api_client.transfer(task)
        print "code:\t{0}\nreason:\t{1}\ndata:\t{2}".format(code,reason,data)
      if tomove:
        _,_,data = trans_api.submission_id()
        subid = data['value']
        task=move([x['src_path'] for x in totransfer],[x['remote_path'] for x in totransfer],ep1,ep2,subid)
        code,reason,data=transfer_api_client.transfer(task)
        print "code:\t{0}\nreason:\t{1}\ndata:\t{2}".format(code,reason,data)


if __name__ == "__main__":
    import sys
    from globusonline.transfer import api_client
    #FIXME: add a decent param parsing;
    try:
        username = sys.argv[1]
        local_endpoint = sys.argv[2]
        local_path = sys.argv[3]
        remote_endpoint= sys.argv[4]
        remote_path = sys.argv[5]
        oauth_token = sys.argv[6]
    except Exception as e:
        print e.message, """
go_sync
observe for changes in the current folder (recursively) and updates the remote accordingly.
usage:
go_sync <GO user name> <local endpoint name> <local path> <remote ep name> <remote path> <OAuth token file>

username = the Globus user name
local_endpoint = name of the local endpoint
local_path = path to sync on the local machine
remote_endpoint= name of the remote endpoint
remote_path = path on the remote machine
oauth_token = authorization token
     """
        local_path = "."
        remote_path = "/home/giggi"
        oauth_token = "un=cadeddu|tokenid=486d4340-90d3-11e3-8ab8-1231391ccf32|expiry=1423408287|client_id=cadeddu|token_type=Bearer|SigningSubject=https://nexus.api.globusonline.org/goauth/keys/491c851c-90d3-11e3-8ab8-1231391ccf32|sig=2246530f0d6c47e85a0e6dcf5413f8c84671a62896d18510ecbea648a5fccddc643c17c35da81a81270236315b0ec7d946037b800a064fe58bb914c069d1dede14c54e84b316853b328dd764791914bdddd02465a8d1b8ba2c24f8de433ebab4b5dfb69db04e2009e62e65e155b1cb19dabc3bacc05aa753539f1cd9e7b1bac4"
        #exit()

    #FIXME: if there's time read from a .gitignore like file the stuff to exclude from the syncing.
    event_handler = GlobusFileWatcherHandler(ignore_patterns = ['.*', '*.pyc'], ignore_directories=['.git','.idea'])
    observer = Observer()
    observer.schedule(event_handler, path=local_path, recursive=True)
    observer.start()
    thefiles =[]

    #we create a transfer_api_client
    transfer_api_client= api_client.TransferAPIClient('cadeddu', goauth=oauth_token)

    try:
        while True:
            time.sleep(10) #

            if thefiles:
                #print ("im pushing " + str(thefiles))
                process(addremotes(thefiles,remote_path),transfer_api_client)
                thefiles=[]
            else:
                print "tick"

    except KeyboardInterrupt:
        observer.stop()
    observer.join()