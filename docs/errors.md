# Error Codes
A detailed overview of possible errors that may occur. If any errors occur and cannot be found here, please raise an [https://github.com/asiangoldfish/PandaServer/issues] detailing the error.

## Error 1: Python3 Not Found
**Reason:** This error occurs because Python3 could not be found.  
panda-manager script directly uses the command `python3` to execite the *server.py* Python script. If this command cannot be found, then the script cannot be executed.

**Fix:** Install Python3 on your system.

## Error 2: Command curl not found
**Reason:** Curl was not found on the system  
panda-manager script uses the curl command to download files from the internet.

**Fix:** Install curl on your system.

## Error 3: Could not find server.py in the remote repository
**Reason:** The script in the remote repository is currently unavailable.  
The ICMP ECHO_REQUEST to the server failed to respond with the HTTP response code 200. The device either does not have internet connection, or the script was moved or renamed.

**Fix:** Manually go to the [github page](https://github.comasiangoldfish/PandaServer) and fetch the *server.py* script. Be sure to view the script as raw first before downloading file, or copy the content from the file and paste it in a new file *server.py* on the local machine in the project's root directory. Also raise an [issue](https://github.com/asiangoldfish/PandaServer/issues) to notify the contributors about this error.

## Error 4: Module pandahttp was not found
**Reason:** The server utilizes custom modules to keep the code clean and organized. The pandahttp module could not be found.

**Fix:** The module exists as a folder in the project's root directory. Ensure that it is named *pandahttp*. If the module does not exist at all, then use the following commands to download the files (make sure that you are in the project directory first): `bash panda-manager -d pandahttp`