# i3custom

An easy way to create and invoke new functionality with i3. Makes use of the i3 
IPC interface and allows for the registration of custom i3 commands.

## Usage

Clone the repository to a location of your choice

    git clone https://github.com/ow97/i3custom

Add the following line to your i3 config

    exec_always "/path/to/..../i3custom/start.py"

## Adding new functionality

The core of the project is `i3custom.py` which provides `CustomHandler` a class 
derived from `i3ipc.Connection`. This class overrides the `on` and `command` 
methods to allow for the registration and execution of custom functionality.

For an example usage see `commands/workspace_toggle.py`.
