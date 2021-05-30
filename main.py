from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import os
import random
import string

separator = (
    '<ulauncher-tmux-sep-' +
    ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)) +
    '>'
)

class PassExtension(Extension):

    def __init__(self):
        super(PassExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        search = event.get_argument() or ""
        session_description = extension.preferences['session_description'] or ""
        pipe = os.popen("if tmux ls > /dev/null 2>&1; then tmux ls -F '#S%s%s'; else echo none; fi" % (separator, session_description))
        terminal_binary = extension.preferences['terminal_binary']
        console_parameters_attach = extension.preferences['console_parameters_attach']
        console_parameters_new = extension.preferences['console_parameters_new']
        output = pipe.read()
        if output.splitlines()[0] != "none":
            for line in output.splitlines():
                if not search or search.lower() in line.split(separator)[0].lower():
                    item = ExtensionResultItem(
                        icon='images/tmux.png',
                        name=line.split(separator)[0],
                        description=line.split(separator)[1],
                        on_enter=RunScriptAction(terminal_binary + ' ' + console_parameters_attach % line.split(separator)[0], None)
                    )
                    if search == line.split(separator)[0]:
                        items.insert(0, item)
                    else:
                        items.append(item)
        else:
            items.append(
                ExtensionResultItem(
                    icon='images/tmux.png',
                    name='Create a new tmux session',
                    description='No active tmux sessions found',
                    on_enter=RunScriptAction(terminal_binary + ' ' + console_parameters_new, None)
                )
            )

        return RenderResultListAction(items)

if __name__ == '__main__':
    PassExtension().run()
