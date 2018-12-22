import collections

from i3custom import CustomHandler


class WorkspaceHistoryToggle:
    """
    Maintains a workspace history and registers the workspace_toggle custom
    command to allow for toggling back to a workspace by history index
    """

    def __init__(self, handler: CustomHandler):
        self.workspace_history = collections.deque(maxlen=10)
        current_workspace = handler.get_tree().find_focused().workspace().name
        self.workspace_history.appendleft(current_workspace)

        self.handler = handler

        # Keep track of our workspace history
        handler.on('workspace::focus', self.on_workspace_focus)

        # Register our custom command
        handler.on('#workspace_toggle', self.on_workspace_toggle)

    def on_workspace_focus(self, i3, event):
        """
        Record a workspace history item
        """
        if event.current:
            workspace_name = event.current.name
            self.workspace_history.appendleft(workspace_name)

    def on_workspace_toggle(self, command):
        """
        Parse and execute a workspace_toggle command
        """
        args = command.split()
        assert args[0].strip() == "workspace_toggle"

        try:
            self.toggle(int(args[1]))
        except ValueError as err:
            raise ValueError(
                "While parsing workspace_toggle args, expected an int but got "
                "'" + args[1] + "'"
            )

    def toggle(self, history_distance):
        """
        Toggle to the workspace the specified distance back in the history
        """
        # Make sure we don't try to go beyond recorded history
        if history_distance < len(self.workspace_history):
            # Get and delete the relevant history item
            previous_workspace = self.workspace_history[history_distance]
            del self.workspace_history[history_distance]

            # Switch back to the previous workspace
            self.handler.command('workspace "' + previous_workspace + '"')
