#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

#pragma warning(disable : 4996) // this isn't important, just disables an annoying warning

void remove_spaces(char* s) {
    char* d = s;
    do {
        while (*d == ' ') {
            ++d;
        }
    } while (*s++ = *d++);

}

int main() {
    char lockFileData[256];  // This is a string we'll use to store credentials found in a game file (we'll use them later for api access)

    char* lockfile_dir = getenv("LocalAppData"); // Get the localappdata folder
    strcat(lockfile_dir, "\\Riot Games\\Riot Client\\Config\\Lockfile"); // then add the path to the file that has the data we need

    FILE* lockfile; 
    lockfile = fopen(lockfile_dir, "rt"); // open the file to read it

    fgets(lockFileData, sizeof(lockFileData), lockfile); // then we'll store the contents of the file 
    remove_spaces(lockFileData); // we need to remove the spaces from the data so that it doesn't seperate into multiple arguments when we pass into the command line
    fclose(lockfile); 


    char lib_command[256] = "lib -clientinfo "; // Here we'll create the base command used to run lib.exe (compiled python), with the -clientinfo argument because we want it to find CLIENT INFO
    strcat(lib_command, lockFileData);          // For it to do that though, it needs the data from the lockfile we collected earlier (it contains a password neccessary for the script to fetch more credentials, which is explained more in the python code)
    system(lib_command);                        // run the command

    // At this point, the python is handling the data we gave it by sending a http request to a local server run by the valorant client, in order to get more info about the client itself. (all we gave it was the port to the server, and the password needed to get into it)

    Sleep(5000);   // Wait a few seconds so the python has time to write the client info to a file

    char* clientInfoDir = getenv("LocalAppData");              // Get the localappdata folder
    strcat(clientInfoDir, "\\valassistant\\clientInfo.json");  // then append the path to the file python used to output it's data.

    FILE *clientInfoFile; 
    clientInfoFile = fopen(clientInfoDir, "rt"); // open it with text reading permissions

    char clientInfo[256]; // variable for storing the client info 

    fgets(clientInfo, sizeof(clientInfo), clientInfoFile); // store it

    fclose(clientInfoFile); // close the file

    printf("\n\nGot client info:\n%s\n\n", clientInfo); // then print it (the next step here is to hopefully parse the data, then use the api again to get things like match data, player info, etc, then display it on a UI)
                                                        // the seperate python library is necessary because C is needed for the UI, and python is needed for the much easier http requests

    system("pause");

    return 0;
}

