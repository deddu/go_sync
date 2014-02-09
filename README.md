#go_sync 0.1.0
keep a remote folder synchronized with the desired local folder using globus.apiclient. 

##Usage:
`./go_sync <GO user name> <local endpoint name> <local path> <remote ep name> <remote path> <OAuth token file>`

- username = the Globus user name
- local_endpoint = name of the local endpoint
- local_path = path to sync on the local machine
- remote_endpoint = name of the remote endpoint
- remote_path = path on the remote machine
- oauth_token = authorization token        

##ToDo:

- add "moving" logic . the lines are commented out due to the requests going out of sync. which means that the move fails. requires 1-2h of work
- add "mkdir" I'm not sure how it should be implemented, adding the files recursively doesn't really cut it. requires 1-2h
- add a comparison between snaphsot, when the program starts between the local and the server, and apply them automatically 1-2h

##known issues:
- check writing permissions on the remote endpoint

