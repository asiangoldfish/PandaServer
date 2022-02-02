#!/usr/bin/bash

if [[ $2 == "--help" ]] || [[ $2 == "-h" ]]; then
    echo """Usage: panda-manager --start [OPTION]

Starts the PandaServer. The server is run with the script server.py. This command also
takes optional arguments.

Arguments:
    -b, --browser [VALUE]   right after --start, enter a browser name and open
                            a new tab in it.
    -p, --port [VALUE]      open another the server in another port. This
                            option will override any port settings in the 
                            settings.ini config file.
    -l, --live-reload       enable live reload. Disabled by default.

For more about the command in detail, visit the documentation at
https://github.com/asiangoldfish/PandaServer.

Due to the way that the commands are parsed, incorrect arguments will be ignored and default
values will be applied.

Errors:
Some errors may occur. Visit the documentation for help with troubleshooting them."""

    exit 0
fi

# Enables virtual environment
source "source_venv.sh"
source_val=$?
if [ ${source_val} -eq 1 ]; then
    echo "No virtual environment was found. Use the following command to setup one up:"
    echo "panda-manager --download modules"
    exit 1
fi

# Check if Python3 is installed on the system
command -v "python3" &>/dev/null || verify_cmd "python3" exit

# Checks that the main file exists
if ! [ -f server.py ]; then
    echo -n "File server.py does not exist. "
    echo "Download the file using the following command:"
    echo "bash panda-manager -d server.py"
    exit 1
fi

# Checks for a second argument, which will tell the script to
# open a new tab in a chosen browser and what command to open
# the browser with

# Runs through each argument passed and checks for flags and value accordingly
# Default values
browser=""
port=""
live_reload="false"
host="localhost"

# The loop will break if no commands was passed or the command does not start with the sign -
while ! [[ ${2} == "" ]] && [[ ${2:0:1} == "-" ]]; do
    case ${2} in
    -b | --browser)
        if ! [[ $3 == "" ]]; then
            browser="${3}"
        fi
        ;;
    -p | --port)
        if ! [[ $3 == "" ]]; then
            port="${3}"
        else
            # Interrupts program because port was specified but not passed
            echo "Missing port number"
            exit 1
        fi
        ;;
    -h | --host)
        if ! [[ $3 == "" ]]; then
            host="${3}"
        fi
        ;;
    -l | --live-reload)
        live_reload="true"
        ;;
    *)
        echo "Invalid command: ${2}"
        exit
        ;;
    esac
    shift
done
# Verifies port number
if [[ "${port}" =~ ^[0-9]+$ ]] && (("${port}" >= 1024 && "${port}" <= 65536)); then
    # port="${port}"
    :
elif [[ "${port}" == "" ]]; then
    :
else
    echo "Port number must be an integer between 1024 and 65536"
    exit 1
fi

# Opens browser if appropriate argument is passed
if ! [[ ${browser} == "" ]]; then
    # Checks if command is available
    command -v "${browser}" &>/dev/null || (verify_cmd "${browser}" && exit 1)
    # Run the browser
    ${browser} http://"${host}":"${port}" >/dev/null 2>&1
fi

# Enables live-reload if enabled
if [[ ${live_reload} == "true" ]]; then
    # Checks if nodemon is globally installed
    command -v "nodemon" &>/dev/null || verify_cmd "nodemon" exit 1

    nodemon server.py "${port}"
else
    python3 server.py "${port}"
fi
