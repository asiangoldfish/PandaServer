#!/usr/bin/bash

# Help page for the info command
info_help() (
    echo "Usage: panda-manager --info [OPTION]

This command provides additional info about the project.

Options:
    -h, --help              help page for the --info command
    -v, --version           project version
    -p, --path              path to the project directory
    -d, --documentation     link to the project's documentation
    -r, --remote-repository link to the remote repository
    -l, --license           link to the project's license"
)
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
case $2 in
-h | --help)
    info_help
    ;;
-v | --version)
    echo "${version}"
    ;;
-p | --path)
    echo "Project directory path:"
    echo "${SCRIPT_DIR}"
    ;;
-d | --documentation)
    echo "${repo_baseurl}"
    ;;
-r | --remote-repository)
    echo "${repo_baseurl}"
    ;;
-l | --license)
    cat "${SCRIPT_DIR}/LICENSE"
    ;;
*)
    if [[ $2 == "" ]]; then
        info_help
    else
        echo "Invalid argument: $2"
    fi
    ;;
esac
