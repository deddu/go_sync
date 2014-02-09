#!/usr/bin/env python
__author__ = 'deddu'

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class GlobusFileWatcherHandler(PatternMatchingEventHandler):
    def on_any_event(self, event):
        thefiles.append({"type":event.event_type,
                         "src_path":event.src_path, #file/dir generating the event
                         "dest_path": event.dest_path if event.event_type=="moved" else None  # only moving files has a source and a destination.
        })

def addremotes(files_dict,remote):
    from os import path
    for f in files_dict:
        f['remote_path'] = path.join(remote,path.split(f['src_path'])[1])
    return files_dict

def process(files,trans_api, ep1="ep1",ep2="ep2"):
      '''
      process the different files for the different events they registered.
      '''
      from api_interface import transfer,delete#,move
      # define few filter predicates
      def modified_or_created(x):
          return x.get('type') in ["modified","created"]
      def deleted(x):
          return x.get('type')=="deleted"
      #def moved(x):
      #    return x.get('type')=="moved"
      #TODO: few possible improvements are dir creation, etc.
      totransfer = filter(modified_or_created, thefiles)
      todel = filter(deleted,thefiles)
      #tomove = filter(moved,thefiles)
      if totransfer:
        _,_,data = trans_api.submission_id()
        subid = data['value']
        task=transfer([x['src_path'] for x in totransfer],[x['remote_path'] for x in totransfer],ep1,ep2, subid)
        #print "READY TO SUBMIT TASK: -----------\n",task.as_json()
        code,reason,data=transfer_api_client.transfer(task)
        print "code:\t{0}\nreason:\t{1}\ndata:\t{2}".format(code,reason,data)
      if todel:
        _,_,data = trans_api.submission_id()
        subid = data['value']
        task=delete([x['src_path'] for x in todel],ep1,ep2,subid)
        code,reason,data=transfer_api_client.delete(task)
        print "code:\t{0}\nreason:\t{1}\ndata:\t{2}".format(code,reason,data)
      #if tomove:
      #  _,_,data = trans_api.submission_id()
      #  subid = data['value']
      #  task=move([x['src_path'] for x in totransfer],[x['remote_path'] for x in totransfer],ep1,ep2,subid)
      #  code,reason,data=transfer_api_client.transfer(task)
      #  print "code:\t{0}\nreason:\t{1}\ndata:\t{2}".format(code,reason,data)

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
        print sys.argv, e.message, """
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
        exit(1)

    #FIXME: if there's time read from a .gitignore like file the stuff to exclude from the syncing.
    event_handler = GlobusFileWatcherHandler()#(ignore_patterns = ['.*', '*.pyc'], ignore_directories=['.git','.idea'])
    observer = Observer()
    observer.schedule(event_handler, path=local_path, recursive=True)
    observer.start()
    thefiles =[]

    #we create a transfer_api_client
    transfer_api_client= api_client.TransferAPIClient(username, goauth=oauth_token)
    _,_,req = transfer_api_client.endpoint_activation_requirements(local_endpoint)
    print req.as_json()
    transfer_api_client.endpoint_autoactivate(local_endpoint, if_expires_in="10")

    _,_,req = transfer_api_client.endpoint_activation_requirements(remote_endpoint)
    transfer_api_client.endpoint_autoactivate(remote_endpoint, if_expires_in="10")

    try:
        while True:
            time.sleep(5*60) #every 5 minutes
            if thefiles:
                try:
                    process(addremotes(thefiles,remote_path),transfer_api_client,local_endpoint,remote_endpoint)
                except api_client.APIError as e:
                    print "Error: %s" % e.message
                thefiles=[]

    except KeyboardInterrupt:
        observer.stop()
    observer.join()