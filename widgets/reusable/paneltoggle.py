from fabric.widgets.button import Button
from fabric.utils import exec_shell_command, exec_shell_command_async, invoke_repeater


class CommandSwitcher(Button):
    @staticmethod
    def cat_icon(text: str, icon: str):
        return f"{icon} {text}"

    def __init__(
        self,
        command: str,
        enabled_icon: str,
        disabled_icon: str,
        name="panel-button",
        enable_label=True,
        enable_tooltip=True,
        interval: int = 2000,
    ):
        self.command = command
        self.command_without_args = self.command.split(" ")[0]  # command without args

        print(self.command, self.command_without_args)

        super().__init__(label=self.cat_icon("On", ""), name=name)

        self.enabled_icon = enabled_icon
        self.disabled_icon = disabled_icon
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip

        self.connect("clicked", self.toggle)
        invoke_repeater(interval, self.update, initial_call=True)

    def is_active(self, *_):
        return (
            exec_shell_command(
                f"bash -c 'pgrep -x {self.command_without_args} > /dev/null && echo yes || echo no'"
            ).strip()
            == "yes"
        )

    def toggle(self, *_):
        if self.is_active():
            exec_shell_command(f"pkill {self.command_without_args}")
        else:
            exec_shell_command_async(f"bash -c '{self.command}&'", lambda *_: None)
        return self.update()

    def update(self, *_):
        if self.enable_label:
            self.set_label(
                self.cat_icon(
                    "On" if self.is_active() else "Off",
                    self.enabled_icon if self.is_active() else self.disabled_icon,
                )
            )
        if self.enable_tooltip:
            self.set_tooltip_text(
                f"{self.command_without_args} enabled"
                if self.is_active()
                else f"{self.command_without_args} disabled"
            )
        return True
