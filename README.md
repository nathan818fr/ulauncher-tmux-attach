# Ulauncher Tmux Attach

Ulauncher Tmux Attach is an extension for [Ulauncher](https://ulauncher.io/)
that allows you to easily attach to or create new [tmux](https://github.com/tmux/tmux/wiki)
sessions.

![Extension preview](./screenshot.png?raw=true)

## Installation

1. Open Ulauncher
2. Open the Extension settings
3. Click on the "Add extension" button
4. Paste the following URL:
   ```
   https://github.com/nathan818fr/ulauncher-tmux-attach
   ```
5. Click on the "Add" button

## Usage

1. Open Ulauncher
2. Type `tmux` followed by a space
3. Select the desired action from the list of available options

## Terminal Configuration

This extension uses gnome-terminal by default.
If you want to use another terminal, you can change it in the extension
settings.

| Terminal                   | Command (new tab)                               | Command (new window)   |
| -------------------------- | ----------------------------------------------- | ---------------------- |
| GNOME Terminal _(default)_ | `gnome-terminal --tab -e %s`                    | `gnome-terminal -e %s` |
| Konsole                    | `konsole --new-tab -e %s`                       | `konsole -e %s`        |
| Tilix                      | `tilix -a app-new-session --focus-window -e %s` | `tilix -e %s`          |
| Terminator                 | -                                               | `terminator -e %s`     |

Note: In the commands, `%s` will be replaced by a POSIX-escaped shell argument,
so don't add quotes around it!

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE)
file for details.
