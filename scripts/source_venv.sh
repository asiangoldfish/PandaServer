#!/usr/bin/bash

# Activate virtual environment
# Searches through all directories in project directory to find a
# virtual environment directory.
valid_dirnames=("venv" ".venv" "env" ".env")
for name in "${valid_dirnames[@]}"; do
    if [[ -d "${name}" ]] && [[ -f "${name}/bin/activate" ]]; then
        source "${name}/bin/activate"
        return 0
    fi
done

# If no virtual environments were found, return 1
return 1
