1.



Generate dummy file:
```python
make genfile
```

File will be put in `./data/bigfile.dat`

Install some FTP server, We used an android app called ["primitive ftp"]().

Upload the file to the ftp server in the root of the ftp tree.

Set the username and password on FTP server:
- `admin`
- `admin`

Take note of the ports used by the FTP server.

In our case:
- `12345` used for FTP protocol
- `5678` used as passive port

Take note of the device's IP, in our case it was 192.168.0.139

healthy:
![alt text](image.png)

ACK flood:
![alt text](image-1.png)

healthy:
![alt text](image-2.png)

RST flood:
![alt text](image-3.png)