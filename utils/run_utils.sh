#!/bin/bash

# Get the current directory
current_directory=$(pwd)

# Function to run a Python script in a new tab within the same Terminal window
run_script_new_tab() {
  osascript -e "tell application \"Terminal\" to do script \"cd '$current_directory' && python3 '$1'\""
}

# Get a list of all Python files in the current directory and run them in new tabs, excluding files containing "test"
for script in *.py; do
  if [[ "$script" != *"test"* ]]; then
    run_script_new_tab "$script"
  fi
done
