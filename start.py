#!/usr/bin/env python3

"""
Open a new custom handler connection to i3 and register the desired custom
functionality with the handler
"""

from commands.workspace_toggle import WorkspaceHistoryToggle
from i3custom import CustomHandler

if __name__ == '__main__':
    handler = CustomHandler()

    WorkspaceHistoryToggle(handler)

    handler.main()
