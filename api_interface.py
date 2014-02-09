__author__ = 'deddu'
# deals with files using Globus api transfer client
# see https://transfer.api.globusonline.org/v0.10/doc/index.html#terminology

from globusonline.transfer import api_client
import time, datetime



def transfer(what, where, ep1="go#ep1", ep2="go#ep2", submission_id = ""):
    deadline = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)#fetch this from a config file eventually
    #here we create a new transfer object.
    t = api_client.Transfer(submission_id,
                            ep1, #the local endpoint
                            ep2, #remote endpoint
                            deadline,
                            encrypt_data=True,
                            sync_level=3 # overwrites the destination if the checksum of the files is different
    )
    if isinstance(what,list) and isinstance(where,list):
        if len(what) != len(where):
            raise Exception("the number of sources and destinations specified is not the same")

        [t.add_item(*x) for x in zip(what,where)] # is populated with the filenames
    elif isinstance(what,(unicode,str)) and isinstance(where,(unicode,str)):
        t.add_item(what,where)
    else:
        raise Exception('the formats of the source and destinations do not match.')
    return t

def delete(what, ep1="go#ep1", ep2="go#ep2",submission_id = ""):
    deadline = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)#fetch this from a config file eventually
    #here we create a new Delete object.
    t = api_client.Delete(submission_id,
                            ep2, #remote endpoint
                            deadline=deadline,
    )
    if isinstance(what,list):
        [t.add_item(x) for x in what] # is populated with the filename
    else:
        t.add_item(what)
    return t

#def move(what,where, ep1="go#ep1", ep2="go#ep2",submission_id = ""): #may change
    #
    #transfer(what,where, ep1, ep2, submission_id)#this is a little trickier, as we might want to wait for the response...
    #delete(what,ep1,ep2,submission_id)