#!/usr/bin/bash

function launch_browser() {
    browser="$1" # Browser to launch    # Opens browser if appropriate argument is passed
    if ! [[ ${browser} == "" ]]; then
        # Checks if command is available
        command -v "${browser}" &>/dev/null || (verify_cmd "${browser}" && exit 1)
        # Run the browser
        ${browser} http://"${host}":"${port}" >/dev/null 2>&1
    fi

    # Opens browser if appropriate argument is passed
    if ! [[ ${browser} == "" ]]; then
        # Checks if command is available
        command -v "${browser}" &>/dev/null || (verify_cmd "${browser}" && exit 1)
        # Run the browser
        ${browser} http://"${host}":"${port}" >/dev/null 2>&1
    fi
}

function launch_server() { 
    local live_reload="$1" # Whether to activate live reload server

    # Enables live-reload if enabled
    if [[ $live_reload == "true" ]]; then
        # Checks if nodemon is globally installed
        verify_cmd "entr" || return 1
        # nodemon server.py "$port"
        # ls -I "venv" -I "__pycache__" "$SCRIPT_PATH"/*
        find "$PWD" -name ".*" -prune -o -print | entr -r python "src/main.py" "--port=$port"
    else
        python3 src/main.py --port="$port"
    fi
    return 0
}

####
# Help page
####
function start_usage() {
    echo "Usage: panda-manager --start [OPTION]

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
Some errors may occur. Visit the documentation to troubleshoot them."

    return 0
}

function verify_portnum() {
    port="$1"

    # Verifies port number
    if [[ "$port" =~ ^[0-9]+$ ]] && (("$port" >= 1024 && "$port" <= 65536)); then
        # port="${port}"
        :
    elif [[ "$port" == "" ]]; then
        :
    else
        echo "Port number must be an integer between 1024 and 65536"
        exit 1
    fi
}

function start_main() {
    activate_venv || return 1 # Activate Python3 virtual environment

    # Checks for a second argument, which will tell the script to
    # open a new tab in a chosen browser and what command to open
    # the browser with.
    # Runs through each argument passed and checks for flags and value accordingly
    # Default values
    browser=""
    port="$("$INIPARSER" --file settings.ini --value --section Default --key port)"
    live_reload="false"
    host="localhost"

    # The loop will break if no commands was passed or the command does not start with the sign -
    while ! [[ ${2} == "" ]] && [[ ${2:0:1} == "-" ]]; do
        case ${2} in
        "-b" | "--browser")
            if ! [[ $3 == "" ]]; then
                browser="${3}"
            fi
            ;;
        "-p" | "--port")
            if ! [[ $3 == "" ]]; then
                port="${3}"
            else
                # Interrupts program because port was specified but not passed
                echo "Missing port number"
                return 1
            fi
            ;;
        "-h" | "--host")
            if ! [[ $3 == "" ]]; then
                host="${3}"
            fi
            ;;
        "-l" | "--live-reload")
            live_reload="true"
            ;;
        *)
            start_usage
            exit
            ;;
        esac
        shift
    done

    verify_portnum "$port" # Port number is between 1 and 65536
    launch_browser "$browser"
    launch_server "$live_reload"
}
