# Computer Networks Project
## Peer-To-Peer file sharing system with Tkinter for GUI, sockets, threads etc.

## How to run main redirecting server [FT]:
```python
python3 server.py
```
## How to run a client:
```python
python client.py
```
## Here is the description of the used protocol:

The IP address of FT and the port number on which the application is running
should be public, i.e., users should know the IP address and port number of FT.
* When a peer A connects to FT, A should automatically send information about its
shared files (up to 5 files) as a list of records to FT in the following format: <file
name, file type (e.g., text, jpg, etc), file size, file last modified date (DD/MM/YY),
IP address, port number>. A should send “HELLO” and receive “HI” before sending the information.
* If A does not send any file information to FT while joing the system, i.e., if A does
not share any file, then FT should not accept A. FT should not respond to A.
* Only accepted peers should be able to use the services offered by this system.
* When A wants to download a file with the name “File Name”, A requests the file
from FT by sending “SEARCH: ” + “File Name”.
* When FT receives “SEARCH: ” + “File Name”, it tries to find the file in a hash
table where ‘key’ is filename and ‘value’ is a list which contains records of this
format: <file type, file size, file last modified date (DD/MM/YY), IP address, port
number>.
– If FT finds the file, it should send “FOUND: ” + list of records.
– If FT does not find the file, it should send “NOT FOUND”.
* After receiving a list of records, A should choose one of the peers (records) from the
list, say B, and connect to B (using IP and port number) to request and download
the file. For that A should send “DOWNLOAD: ” + “FileName, type, size” to B.
* When B receives a “DOWNLOAD” message from A, it should send “FILE: ”+file
to A.
* When A wants to leave the system, A should notify FT about this so that FT can
update the list of online users. A should send “BYE” to FT to do so.
