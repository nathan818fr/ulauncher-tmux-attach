from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import os
import random
import string

tmux_ls_cmd = "if tmux ls >/dev/null 2>&1; then tmux ls -F %s; fi"
separator = "<ulauncher-tmux-sep-%s>" % "".join(
    random.choices(string.ascii_letters + string.digits, k=8)
)


class TmuxExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        pref_session_description = extension.preferences["session_description"] or ""
        pref_terminal_cmd = extension.preferences["terminal_cmd"]
        pref_tmux_attach_cmd = extension.preferences["tmux_attach_cmd"]
        pref_tmux_new_cmd = extension.preferences["tmux_new_cmd"]
        pref_new_session_name = extension.preferences["new_session_name"]
        search = event.get_argument() or ""
        items = []

        # List existing sessions
        pipe = os.popen(
            format_cmd(tmux_ls_cmd, "#S" + separator + pref_session_description)
        )
        for line in pipe.read().splitlines():
            line = line.split(separator)
            name, description = line[0], line[1] if len(line) > 1 else ""

            # Skip sessions that don't match the search query
            if search and search.lower() not in name.lower():
                continue

            # Create an item to attach to the session
            # If the search query matches the session name exactly, insert the item at the beginning
            # Otherwise, append the item at the end
            item = ExtensionResultItem(
                icon="images/tmux.png",
                name=name,
                description=description,
                on_enter=RunScriptAction(
                    format_cmd(
                        pref_terminal_cmd, format_cmd(pref_tmux_attach_cmd, name)
                    ),
                    None,
                ),
            )
            if search == name:
                items.insert(0, item)
            else:
                items.append(item)

        # Add an item to create a new session
        # Ensure that the new session name is unique by appending a number to the end if necessary
        new_session_name_prefix = search or pref_new_session_name
        new_session_name = new_session_name_prefix
        new_session_index = 1
        while new_session_name in [item._name for item in items]:
            new_session_index += 1
            new_session_name = "%s-%d" % (new_session_name_prefix, new_session_index)
        items.append(
            ExtensionResultItem(
                icon="images/tmux.png",
                name=new_session_name,
                description="Create %s" % new_session_name,
                on_enter=RunScriptAction(
                    format_cmd(
                        pref_terminal_cmd,
                        format_cmd(pref_tmux_new_cmd, new_session_name),
                    ),
                    None,
                ),
            )
        )

        # Return the list of items
        return RenderResultListAction(items)


def posix_shell_escape(arg):
    """
    Escape a string for use as a single argument in a POSIX shell command line.

    This function takes a string argument and returns a new string with any
    characters that have special meaning in a POSIX shell context escaped.

    Args:
        arg (str): The string to escape.

    Returns:
        str: The escaped string.
    """
    return "'" + arg.replace("'", "'\\''") + "'"


def format_cmd(cmd, *args):
    """
    Formats a command string with the given arguments, escaping each argument with `posix_shell_escape`.

    Example:
        format_cmd("echo %s %s", "hello world", "!") => "echo 'hello world' '!'"

    Args:
        cmd (str): The command string to format.
        *args: The arguments to insert into the command string.

    Returns:
        str: The formatted command string.
    """
    return cmd % tuple(map(posix_shell_escape, args))


if __name__ == "__main__":
    TmuxExtension().run()
