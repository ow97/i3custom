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

## Calling your custom commands

Custom command names must be called with a preceding '#' from the i3 config.
For example, one may register a handler for the ``#workspace_toggle`` custom
command, this could then be bound to a key combination with any of the
following lines in the i3 config file:

    bindsym $Mod+h nop; #workspace_toggle
    bindsym $Mod+h workspace History; #workspace_toggle
    bindsym $Mod+h mode default; #workspace_toggle; workspace History
    bindsym $Mod+h workspace History; #workspace_toggle; mode default 

Notice that the first command invoked must be a native one, so if only a custom
command is to be executed after a key press then `nop` should be used as the 
first command in a chain.
