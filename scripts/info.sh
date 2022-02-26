#!/usr/bin/bash

# Help page for the info command
info_help() (
    echo "Usage: panda-manager --info [OPTION]

This command provides additional info about the project.

Options:
    documentation link      to the project's documentation
    help                    this page
    license                 link to the project's license
    remote-repository       link to the remote repository
    version                 project version"
)
case $2 in
-h | --help)
    info_help
    ;;
-v | --version)
    echo "${version}"
    ;;
-d | --documentation)
    echo "${repo_baseurl}/wiki"
    ;;
-r | --remote-repository)
    echo "${repo_baseurl}"
    ;;
-l | --license)
    cat "LICENSE"
    ;;
*)
    if [[ $2 == "" ]]; then
        info_help
    else
        echo "Invalid argument: $2"
    fi
    ;;
esac
