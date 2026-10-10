#Requires AutoHotkey v2.0

; Any Win + Any Shift + Mouse Wheel Up
#+WheelUp:: {
    Run('glaze_ext_client.exe move_active_window_to_workspace_relative -1')
}

; Any Win + Any Shift + Mouse Wheel Down
#+WheelDown:: {
    Run('glaze_ext_client.exe move_active_window_to_workspace_relative 1')
}