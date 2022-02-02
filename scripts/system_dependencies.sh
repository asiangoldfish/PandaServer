#!/usr/bin/bash

cwd="$(dirname "${BASH_SOURCE[0]}")"
unipack="$cwd/../unipack/unipack.sh"

source "$unipack" && printf "All system dependencies have successfully been installed" \
|| { printf "Failed to install system dependencies"; exit 1; }