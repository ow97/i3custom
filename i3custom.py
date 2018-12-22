from typing import Callable
import subprocess

import i3ipc


class CustomHandler(i3ipc.Connection):
    """
    Provides an i3 connection with the ability to register handlers for non
    native commands which can be bound to key combinations just like native i3
    commands.

    Custom command names must be called with a preceding '#' from the i3 config.
    For example, one may register a handler for the ``show_history`` custom
    command, this could then be bound to a key combination with any of the
    following lines in the i3 config file:

    ::

        bindsym $Mod+h #show_history
        bindsym $Mod+h nop; #show_history
        bindsym $Mod+h workspace History; #show_history
        bindsym $Mod+h #show_history; workspace History
    """

    def __init__(self):
        super().__init__()

        self.custom_handlers = {}

        self.on('binding', self.__on_binding)

    def on(self, event: str, handler: Callable):
        """
        Add a handler for a custom i3 command. If a handler is already
        registered for the specified command it will be replaced.

        :rtype: object
        :param event: The native detailed event or custom base command for which
            a handler is to be registered
        :param handler: A function taking the full command as its only parameter
        """
        command = event.strip()
        if command.startswith('#'):
            self.custom_handlers[command[1:]] = handler
        else:
            super().on(event, handler)

    def __on_binding(self, i3, event):
        """
        Execute the commands due to be run as a result of the binding event that

        """
        full_command = event.binding.command

        if '#' not in full_command:
            # There are no custom commands for us to handle and so i3 will
            # have taken care of everything
            return

        # Get the commands that will not have been processed by i3 itself
        unprocessed_commands = full_command[full_command.index("#"):]

        self.command(unprocessed_commands)

    def command(self, command: str):
        """
        Parse a command string and execute all the custom and native commands
        """
        for command in command.split(';'):
            command = command.strip()

            if not command.startswith('#'):
                super().command(command)
                continue

            try:
                self.__custom_command(command[1:])
            except (NotImplementedError, ValueError) as err:
                # Show a nagbar with error details
                if len(err.args) > 0:
                    _show_nagbar(err.args[0])
                else:
                    _show_nagbar(err)

    def __custom_command(self, complete_command: str):
        """
        Execute the supplied custom command by invoking the registered handler

        :param complete_command the command, including args, to be executed

        :raises NotImplementedError if there is no handler register for the
                supplied command
        """
        base_command = complete_command.split(maxsplit=1)[0]
        if base_command not in self.custom_handlers:
            raise NotImplementedError(
                "There is no handler registered for the command "
                "'" + base_command + "'"
            )

        self.custom_handlers[base_command](complete_command)


def _show_nagbar(message: str):
    """
    Show the supplied message with the i3 nagbar
    """
    subprocess.call(
        ["i3-nagbar", "-m", message],
        stdout=None,
        stderr=None
    )
