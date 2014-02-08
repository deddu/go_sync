__author__ = 'deddu'
# deals with files using Globus api transfer client
# see https://transfer.api.globusonline.org/v0.10/doc/index.html#terminology

from globusonline.transfer import api_client
import time, datetime



def transfer(what, where, ep1="go#ep1", ep2="go#ep2", submission_id = "ed41a2d6-9069-11e3-bce2-123139074522"):
    #code, message, data = api_client.SimpleTransfer().submission_id()
    #data["value"]
    deadline = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)#fetch this from a config file eventually
    #here we create a new transfer object.
    t = api_client.Transfer(submission_id,
                            ep1, #the local endpoint
                            ep2, #remote endpoint
                            deadline,
                            encrypt_data=True,
                            sync_level=3 # overwrites the destination if the checksum of the files is different
                            #preserve_timestamp=True # it is not clear whether it refers to the local or remote.. I want the remote to have the local timestamp.
    )
    if isinstance(what,list) and isinstance(where,list):
        if len(what) != len(where):
            raise Exception("the number of sources and destinations specified is not the same")

        [t.add_item(*x) for x in zip(what,where)] # is populated with the filenames
    elif isinstance(what,(unicode,str)) and isinstance(where,(unicode,str)):
        t.add_item(what,where)
    else:
        raise Exception('the formats of the source and destinations do not match.')

    #code, reason, data = api_client.transfer(t) # then sent
    #task_id = data["task_id"]
    print "t.items: ",t.items
    return t#task_id#code, reason, data

def delete(what, ep1="go#ep1", ep2="go#ep2",submission_id = "ed41a2d6-9069-11e3-bce2-123139074522"): #may change
    #code, message, data = api_client.SimpleTransfer().submission_id()
    submission_id = "ed41a2d6-9069-11e3-bce2-123139074522"#data["value"]
    deadline = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)#fetch this from a config file eventually
    #here we create a new Delete object.
    t = api_client.Delete(submission_id,
                            ep1, #the local endpoint
                            ep2, #remote endpoint
                            deadline
    )
    if isinstance(what,list):
        [t.add_item(x) for x in what] # is populated with the filename
    else:
        t.add_item(what)
    print("t.items = ",t.items)
    return t

def move(what,where, ep1="go#ep1", ep2="go#ep2",submission_id = "ed41a2d6-9069-11e3-bce2-123139074522"): #may change
    transfer(what,where, ep1, ep2, submission_id)#this is a little trickier, as we might want to wait for the response...
    delete(what,ep1,ep2,submission_id)