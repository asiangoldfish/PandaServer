#!/usr/bin/bash

# Helper functions

download_modules() (
    # Activates virtual environment first to install all dependencies
    # locally in the project directory
    # Firstly, checks if the python3 binary exists in the project folder

    # if ! { [ -f "venv/bin/python3" ] || [ -f ".venv/bin/python3" ] || [ -f "env/bin/python3" ] || [ -f ".env/bin/python3" ]; }; then
    #     echo -n "Could not find Python executable in a virtual environment. Install virtual environment? [Y/n] "
    #     read -r venv_prompt
    #     if ! { [[ ${venv_prompt} == "" ]] || [[ ${venv_prompt} == "y" ]] || [[ ${venv_prompt} == "Y" ]]; }; then
    #         echo "No dependencies were installed"
    #         return 1
    #     else
    #         # Check if python3-venv is installed on the system
    #         command -v "python3" &>/dev/null || verify_cmd "python3" return

    #         # Creates virtual environment
    #         echo "Creating virtual environment..."
    #         python3 -m venv venv
    #     fi
    # fi
    if ! { [ -f "venv/bin/python3" ] || [ -f ".venv/bin/python3" ] || [ -f "env/bin/python3" ] || [ -f ".env/bin/python3" ]; }; then
        # Check if python3-venv is installed on the system
        command -v "python3" &>/dev/null || {
            printf "Package python version 3 could not be found\n"
            exit 1
        }

        printf "Creating virtual environment...\n"
        python3 -m venv venv || {
            printf "Could not create a virtual environment\n"
            exit 1
        }
    fi
    
    source "scripts/source_venv.sh" &>/dev/null || {
        printf "Could not activate Python virtual environment\n"
        printf "Removing virtual environment...\n"
        rm -r venv
        exit 1
    }
    
    # Download dependencies if requirements.txt file exists. If not, downloads requirements.txt from remote repository. If the file could not be found, then
    # output error message and abort
    if ! [[ -f "requirements.txt" ]]; then
        printf "Downloading 'requirements.txt' from remote repository...\n"
        { 
            curl -o "requirements.txt" "https://raw.githubusercontent.com/asiangoldfish/PandaServer/main/requirements.txt"
        } || {
            printf "Failed to install required dependencies: Could not find 'requirements.txt' in local or remote repository\n"
            printf "Removing virtual environment...\n"
            rm -r venv
            return 1
        }
    fi

    printf "Installing dependencies...\n"
    pip3 -q install -r requirements.txt

    deactivate
    return 0
)

download_pandahttp() (
    # Check if curl is installed on the system
    command -v "curl" &>/dev/null || verify_cmd "curl" return

    # Checks that the current directory is PandaServer to ensure that
    # files are downloaded in the correct location
    cwd=$(pwd) # Current directory
    dirname="$(echo "${cwd}" | rev | cut -d'/' -f 1 | rev)"
    if ! [[ ${dirname} == "PandaServer" ]]; then
        echo "Currently not in directory PandaServer. Please change to the project directory before proceeding."
        return 1
    fi

    # Pings all sites to scripts and directories and ensure their availability
    urls=(
        "https://raw.githubusercontent.com/asiangoldfish/PandaServer/main/pandahttp/__init__.py"
        "https://raw.githubusercontent.com/asiangoldfish/PandaServer/main/pandahttp/httpserver.py"
        "https://raw.githubusercontent.com/asiangoldfish/PandaServer/main/pandahttp/mysql.py"
        "https://raw.githubusercontent.com/asiangoldfish/PandaServer/main/pandahttp/terminal.py"
    )
    # Pings each url to see if they are online
    for url in "${urls[@]}"; do
        filename="$(echo "{$url}" | rev | cut -d'/' -f 1 | rev)"
        if curl -s --head --request GET "${url}" | grep "HTTP/2 200" >/dev/null; then
            # Splits the url to get the file name

            echo "Fetching ${filename}..."
        else
            echo "Error 3: Could not find $filename in the remote repository"
            return 1
        fi
    done

    # Creates a new pandahttp directory and also changes directory
    mkdir pandahttp
    cd pandahttp || (echo "Error 1: Directory pandahttp not found" && return)

    # Downloads all files in pandahttp module from remote repository
    echo ""
    for url in "${urls[@]}"; do
        filename="$(echo "${url}" | rev | cut -d'/' -f 1 | rev)"
        echo "Downloading ${filename}..."
        curl -o "${filename}" "${url}"
    done

    cd "${cwd}" || echo "Failed to return to original directory." && return # Change back to original directory
)

download_server() {
    # Pings to check if the script is still available

    if [[ -f "server.py" ]]; then
        printf "File 'server.py' was found"
        return 0
    fi

    printf "Downloading 'server.py' from remote repository...\n"

    serverpy_url="https://raw.githubusercontent.com/asiangoldfish/PandaServer/main/server.py"
    if curl -s --head --request GET $serverpy_url | grep "HTTP/2 200" >/dev/null; then
        curl -o ./server.py $serverpy_url
        return 0
    else
        printf "Could not find 'server.py' in the remote repository\n"
        return 1
    fi
}

download_system_dependencies() (
    source "$SCRIPT_PATH/scripts/system_dependencies.sh"
    return 0
)

usage() {
    echo "Usage: panda-manager --download [FILES]

Example: panda-manager -d server.py
Download missing dependencies automatically from the internet. This command 
also checks if the source is available and will return an error if it's not.

Arguments:
    server.py               downloads the main script of the server. With-
                            out this script, the engine will not work.
    pandahttp               downloads the custom module pandahttp that
                            the project relies on.
    modules                 installs all required python dependencies
    system_dependencies     installs all required system dependencies

An issue can be raised at https://github.com/asiangoldfish/PandaServer/issues"
}

if [[ $1 == "" ]]; then
    usage
    exit 0
fi

case $1 in
-h | --help | help)
    usage
    exit 0
    ;;
server.py)
    download_server || exit 1
    exit 0
    ;;
pandahttp)
    download_pandahttp || exit 1
    exit 0
    ;;
modules)
    download_modules || exit 1
    exit 0
    ;;
system_dependencies)
    download_system_dependencies || exit 1
    exit 0
    ;;
*)
    printf "invalid argument: %s\n" "$@"
    ;;
esac

exit 0
