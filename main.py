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
        default_new_session_name = extension.preferences['new_session_name']
        new_session_name = default_new_session_name
        current_new_session_index = 1
        output = pipe.read()
        lines = output.splitlines()
        if lines and lines[0] != "none":
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
                if new_session_name == line.split(separator)[0]:
                    current_new_session_index += 1
                    new_session_name = "%s-%d" % (default_new_session_name, current_new_session_index)

        if search and (not items or items[0]._name != search):
            new_session_name = search

        items.append(
            ExtensionResultItem(
                icon='images/tmux.png',
                name=new_session_name,
                description='Create %s' % new_session_name,
                on_enter=RunScriptAction(terminal_binary + ' ' + (console_parameters_new % new_session_name), None)
            )
        )

        return RenderResultListAction(items)

if __name__ == '__main__':
    PassExtension().run()
