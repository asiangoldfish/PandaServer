#!/usr/bin/bash

# Installation script for PandaServer's dependencies

supported_os=(
    debian
    arch
)

install_cmd=(
    apt
    pacman
)

# Uses lsb_release to find the name of the Linux distribution. Prompts to install it if the command was not found
if command -v lsb_release &> /dev/null; then
    read -p "Install missing dependency lsb_release? [Y/n]" yn

    # Proceeds to install dependencies if the prompt was accepted.
    case "$yn" in
        [Yy]* | "")
            # Loops through all supported package managers to figure out which of the commands are valid on the system.
            for cmd in "${install_cmd[@]}"; do
                if command -v "$cmd" &> /dev/null; then
                    echo "Command $cmd is valid!"
                    break
                fi
            done

            # Exits the script if a supported package manager could not be found
            echo "Your system does not have a supported package manager. Visit the documentation for more details."
            exit 1

            ;;
        *)
            exit 0
            ;;
    esac
fi

exit 0