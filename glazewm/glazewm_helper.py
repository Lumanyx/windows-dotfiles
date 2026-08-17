import json
import subprocess
import sys


# A Python script for making GlazeWM behave like my previous komorebi setup.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def scan_child(child):
    # Skip any non-window children
    if child["type"] != "window":
        return False
    if not child["hasFocus"]:
        return False
    return True

def recursively_scan_children(child):
    if child["type"] == "split":
        for child in child["children"]:
            if recursively_scan_children(child):
                return True
    elif child["type"] == "window":
        if scan_child(child):
            return True
    return False

# Returns the active monitor ID & workspace ID
def query_active_window():
    # Find the ID of the monitor that currently has focus
    #json_output = subprocess.check_output(['glazewm', 'query', 'monitors'])
    #data = json.loads(json_output)
    #monitors = data["data"]["monitors"]
    #for monitor in monitors:
    #    for workspace in monitor["children"]:
    #        # Skip any non-workspace children
    #        if workspace["type"] != "workspace":
    #            continue
    #        for child in workspace["children"]:
    #            if not recursively_scan_children(child):
    #                continue
    #            monitor_name = workspace["name"]
    #            return [int(monitor_name.split("-")[0]), int(monitor_name.split("-")[1])]

    json_output = subprocess.check_output(['glazewm', 'query', 'workspaces'])
    data = json.loads(json_output)
    workspaces = data["data"]["workspaces"]
    for workspace in workspaces:
        if not workspace["hasFocus"]: continue
        monitor_name = workspace["name"]
        return [int(monitor_name.split("-")[0]), int(monitor_name.split("-")[1])]
    return []

# Workspace IDs are kept between 0 and 9 (10 workspaces per monitor)
def clamp_workspace_id(workspace_id):
    if workspace_id < 0:
        return 9
    elif workspace_id > 9:
        return 0
    else:
        return workspace_id

def focus_workspace(workspace_id):
    data = query_active_window()
    if len(data) == 0:
        print("No active window")
        return None
    monitor_id = data[0]
    workspace_id = clamp_workspace_id(workspace_id)
    target_workspace = format_workspace_id(monitor_id, workspace_id)

    print(subprocess.check_output(["glazewm", "command", "focus", "--workspace", target_workspace]))
    return None

def focus_workspace_relative(direction):
    data = query_active_window()
    if len(data) == 0:
        print("No active window")
        return None
    monitor_id = data[0]
    workspace_id = clamp_workspace_id(data[1] + direction)
    target_workspace = format_workspace_id(monitor_id, workspace_id)
    print("goto ", target_workspace)

    print(subprocess.check_output(["glazewm", "command", "focus", "--workspace", target_workspace]))
    return None

def move_active_window_to_workspace_relative(direction):
    data = query_active_window()
    if len(data) == 0:
        print("No active window")
        return None

    current_monitor = data[0]
    current_workspace = data[1]

    target_workspace_id = current_workspace + direction
    target_workspace_id = clamp_workspace_id(target_workspace_id)
    target_workspace = format_workspace_id(current_monitor, target_workspace_id)
    print("Moving active window to", target_workspace)

    subprocess.check_output(["glazewm", "command", "move", "--workspace", target_workspace])
    subprocess.check_output(["glazewm", "command", "focus", "--workspace", target_workspace])
    return None

def format_workspace_id(monitor_id, workspace_id):
    return str(monitor_id) + "-" + str(workspace_id)

def move_active_window_to_workspace(workspace_id):
    data = query_active_window()
    if len(data) == 0:
        print("No active window")
        return None

    monitor_id = data[0]
    target_workspace = format_workspace_id(monitor_id, workspace_id)

    subprocess.check_output(["glazewm", "command", "move", "--workspace", target_workspace])
    subprocess.check_output(["glazewm", "command", "focus", "--workspace", target_workspace])
    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    command = sys.argv[1]
    print("Running command", command)

    if command == "move_active_window_to_workspace":
        move_active_window_to_workspace(clamp_workspace_id(int(sys.argv[2])))
    elif command == "move_active_window_to_workspace_relative":
        move_active_window_to_workspace_relative(int(sys.argv[2]))
    elif command == "focus_workspace":
        focus_workspace(clamp_workspace_id(int(sys.argv[2])))
    elif command == "focus_workspace_relative":
        focus_workspace_relative(int(sys.argv[2]))
