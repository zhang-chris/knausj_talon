import os
import re
import time

import talon
from talon import Context, Module, app, imgui, ui, fs, actions
from glob import glob
from itertools import islice

# Construct at startup a list of overides for application names (similar to how homophone list is managed)
# ie for a given talon recognition word set  `one note`, recognized this in these switcher functions as `ONENOTE`
# the list is a comma seperated `<Recognized Words>, <Overide>`
# TODO: Consider put list csv's (homophones.csv, app_name_overrides.csv) files together in a seperate directory,`knausj_talon/lists`
cwd = os.path.dirname(os.path.realpath(__file__))
overrides_directory = os.path.join(cwd, "app_names")
override_file_name = f"app_name_overrides.{talon.app.platform}.csv"
override_file_path = os.path.join(overrides_directory, override_file_name)


mod = Module()
mod.list("running", desc="all running applications")
mod.list("launch", desc="all launchable applications")
ctx = Context()

# a list of the current overrides
overrides = {}

# a list of the currently running application names
running_application_dict = {}


mac_application_directories = [
    "/Applications",
    "/Applications/Utilities",
    "/System/Applications",
    "/System/Applications/Utilities",
]

windows_application_directories = [
    "%AppData%/Microsoft/Windows/Start Menu/Programs",
    "%ProgramData%/Microsoft/Windows/Start Menu/Programs",
    "%AppData%/Microsoft/Internet Explorer/Quick Launch/User Pinned/TaskBar",
]

words_to_exclude = [
    "and",
    "zero",
    "one",
    "two",
    "three",
    "for",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "windows",
    "Windows",
]


@mod.capture(rule="{self.running}")  # | <user.text>)")
def running_applications(m) -> str:
    "Returns a single application name"
    try:
        return m.running
    except AttributeError:
        return m.text


@mod.capture(rule="{self.launch}")
def launch_applications(m) -> str:
    "Returns a single application name"
    return m.launch


def split_camel(word):
    return re.findall(r"[0-9A-Z]*[a-z]+(?=[A-Z]|$)", word)


def get_words(name):
    words = re.findall(r"[0-9A-Za-z]+", name)
    out = []
    for word in words:
        out += split_camel(word)
    return out


def update_lists():
    global running_application_dict
    running_application_dict = {}
    running = {}
    for cur_app in ui.apps(background=False):
        name = cur_app.name

        if name.endswith(".exe"):
            name = name.rsplit(".", 1)[0]

        words = get_words(name)
        for word in words:
            if word and word not in running:
                running[word.lower()] = cur_app.name

        running[name.lower()] = cur_app.name
        running_application_dict[cur_app.name] = True

    for override in overrides:
        running[override] = overrides[override]

    lists = {
        "self.running": running,
        # "self.launch": launch,
    }

    # batch update lists
    ctx.lists.update(lists)


def update_overrides(name, flags):
    """Updates the overrides list"""
    global overrides
    overrides = {}

    if name is None or name == override_file_path:
        # print("update_overrides")
        with open(override_file_path, "r") as f:
            for line in f:
                line = line.rstrip()
                line = line.split(",")
                if len(line) == 2:
                    overrides[line[0].lower()] = line[1].strip()

        update_lists()


pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d|[+]")

# todo: this is garbage
def create_spoken_forms(name, max_len=30):
    result = " ".join(list(islice(pattern.findall(name), max_len)))

    result = (
        result.replace("0", "zero")
        .replace("1", "one")
        .replace("2", "two")
        .replace("3", "three")
        .replace("4", "four")
        .replace("5", "five")
        .replace("6", "six")
        .replace("7", "seven")
        .replace("8", "eight")
        .replace("9", "nine")
        .replace("+", "plus")
    )
    return result


@mod.action_class
class Actions:
    def get_running_app(name: str) -> ui.App:
        """Get the first available running app with `name`."""
        # We should use the capture result directly if it's already in the list
        # of running applications. Otherwise, name is from <user.text> and we
        # can be a bit fuzzier
        if name in running_application_dict:
            for app in ui.apps():
                if app.name == name and not app.background:
                    return app
            raise RuntimeError(f'App not running: "{name}"')
        else:
            # Don't process silly things like "focus i"
            if len(name) < 3:
                raise RuntimeError(
                    f'Skipped getting app: "{name}" has less than 3 chars.'
                )

            for running_name, app in ctx.lists["self.running"].items():
                if running_name == name or running_name.lower().startswith(
                    name.lower()
                ):
                    return app

            raise RuntimeError(f'Could not find app "{name}"')

    def switcher_focus(name: str):
        """Focus a new application by  name"""
        app = actions.self.get_running_app(name)
        app.focus()

        # Hacky solution to do this reliably on Mac.
        timeout = 5
        t1 = time.monotonic()
        if talon.app.platform == "mac":
            while ui.active_app() != app and time.monotonic() - t1 < timeout:
                time.sleep(0.1)

    def switcher_launch(path: str):
        """Launch a new application by path"""
        if app.platform == "windows":
            # print("path: " + path)
            os.startfile(path)
        else:
            ui.launch(path=path)

    def switcher_toggle_running():
        """Shows/hides all running applications"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def switcher_hide_running():
        """Hides list of running applications"""
        gui.hide()


@imgui.open(software=app.platform == "linux")
def gui(gui: imgui.GUI):
    gui.text("Names of running applications")
    gui.line()
    for line in ctx.lists["self.running"]:
        gui.text(line)


def update_launch_list():
    launch = {}
    if app.platform == "mac":
        for base in "/Applications", "/Applications/Utilities":
            for name in os.listdir(base):
                path = os.path.join(base, name)
                name = name.rsplit(".", 1)[0].lower()
                launch[name] = path
                words = name.split(" ")
                for word in words:
                    if word and word not in launch:
                        if len(name) > 6 and len(word) < 3:
                            continue
                        launch[word] = path

    elif app.platform == "windows":
        for base in windows_application_directories:
            path = os.path.expandvars(base)

            shortcuts = glob(path + "/**/*.lnk", recursive=True)

            for path in shortcuts:
                # print(name)
                name = create_spoken_forms(
                    path.rsplit("\\")[-1].split(".")[0]
                ).lower()  # =  path.rsplit("\\")[-1].split(".")[0].lower()
                if "install" not in name:
                    # print(name)
                    launch[name] = path
                    words = name.split(" ")
                    for word in words:
                        # print(word)
                        if word not in words_to_exclude and word not in launch:
                            if len(name) > 6 and len(word) < 3:
                                continue
                            launch[word] = path

    ctx.lists["self.launch"] = launch


def ui_event(event, arg):
    if event in ("app_launch", "app_close"):
        update_lists()


# Currently update_launch_list only does anything on mac, so we should make sure
# to initialize user launch to avoid getting "List not found: user.launch"
# errors on other platforms.
ctx.lists["user.launch"] = {}
ctx.lists["user.running"] = {}

# Talon starts faster if you don't use the `talon.ui` module during launch
def on_ready():
    update_overrides(None, None)
    fs.watch(overrides_directory, update_overrides)
    update_launch_list()
    ui.register("", ui_event)


# NOTE: please update this from "launch" to "ready" in Talon v0.1.5
app.register("launch", on_ready)
# app.register("ready", on_ready)
