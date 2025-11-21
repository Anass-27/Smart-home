import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Smart Home Controller"
    page.window_width = 900
    page.window_height = 700
    page.padding = 0
    page.bgcolor = "#F3F4F6"  # UPDATED: Light dashboard background

    # Device states
    light_on = ft.Ref[bool]()
    light_on.current = False
    
    door_locked = ft.Ref[bool]()
    door_locked.current = False
    
    temperature = ft.Ref[float]()
    temperature.current = 22.0
    
    thermostat_on = ft.Ref[bool]()
    thermostat_on.current = False
    
    fan_speed = ft.Ref[int]()
    fan_speed.current = 0
    
    # Action log list
    action_log = []
    
    # Power consumption history (stores power for each hour)
    power_history = [0] * 24
    
    # Calculate current power consumption
    def calculate_power():
        power = 0
        if light_on.current:
            power += 60
        if door_locked.current:
            power += 5
        if thermostat_on.current and temperature.current is not None:
            temp_diff = abs(temperature.current - 20)
            power += 50 + (temp_diff * 10)
        if fan_speed.current is not None:
            power += fan_speed.current * 30
        return round(power, 1)
    
    # Update power history
    def update_power_history():
        current_hour = datetime.now().hour
        current_power = calculate_power()
        power_history[current_hour] = current_power
    
    # Function to add action to log
    def add_action(device, action):
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        action_log.insert(0, {
            "time": time_str,
            "device": device,
            "action": action,
            "user": "User"
        })
        update_power_history()
        update_action_log_table()
    
    # Create action log table
    action_log_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Time", weight=ft.FontWeight.BOLD, color="#3B82F6")),  # BLUE
            ft.DataColumn(ft.Text("Device", weight=ft.FontWeight.BOLD, color="#3B82F6")),
            ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.BOLD, color="#3B82F6")),
            ft.DataColumn(ft.Text("User", weight=ft.FontWeight.BOLD, color="#3B82F6")),
        ],
        rows=[],
        heading_row_color="#FFFFFF",   # WHITE HEADER
        data_row_color={"hovered": "#E5E7EB"},   # LIGHT GREY
    )
    
    def update_action_log_table():
        action_log_table.rows.clear()
        for log in action_log[:10]:
            action_log_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(log["time"], color="#111827")),   # DARK TEXT
                        ft.DataCell(ft.Text(log["device"], color="#111827")),
                        ft.DataCell(ft.Text(log["action"], color="#111827")),
                        ft.DataCell(ft.Text(log["user"], color="#111827")),
                    ]
                )
            )
        page.update()
    
    # Light status text
    light_status = ft.Text("Status: OFF", size=14, color="#111827")
    light_button = ft.ElevatedButton(
        "OFF", 
        bgcolor="#EF4444",     # RED (OFF)
        color=ft.Colors.WHITE,
        width=80
    )
    
    # Door status text
    door_status = ft.Text("Door: UNLOCKED", size=14, color="#111827")
    door_button = ft.ElevatedButton(
        "OFF", 
        bgcolor="#EF4444",   # RED
        color=ft.Colors.WHITE,
        width=80
    )
    
    # Temperature display
    temp_display = ft.Text(f"Set point: {temperature.current:.1f} °C", size=14, color="#111827")
    temp_slider = ft.Slider(
        min=15, 
        max=30, 
        value=22, 
        divisions=30, 
        label="{value}°C",
        active_color="#3B82F6",    # BLUE
        inactive_color="#E5E7EB"   # LIGHT GREY
    )
    
    # Thermostat button
    thermostat_button = ft.ElevatedButton(
        "OFF", 
        bgcolor="#EF4444",  # RED
        color=ft.Colors.WHITE,
        width=80
    )
    
    # Fan speed display
    fan_display = ft.Text(f"Fan speed: {fan_speed.current}", size=14, color="#111827")
    fan_slider = ft.Slider(
        min=0, 
        max=3, 
        value=0, 
        divisions=3, 
        label="{value}",
        active_color="#3B82F6",
        inactive_color="#E5E7EB"
    )
    
    # Current power display
    current_power_display = ft.Text(
        f"Current Power: {calculate_power():.0f}W", 
        size=20, 
        weight=ft.FontWeight.BOLD,
        color="#2563EB"   # BLUE
    )
    
    # Toggle light function
    def toggle_light(e):
        light_on.current = not light_on.current
        if light_on.current:
            light_status.value = "Status: ON"
            light_button.text = "ON"
            light_button.bgcolor = "#22C55E"  # GREEN
            add_action("light1", "Turn ON")
        else:
            light_status.value = "Status: OFF"
            light_button.text = "OFF"
            light_button.bgcolor = "#EF4444"  # RED
            add_action("light1", "Turn OFF")
        current_power_display.value = f"Current Power: {calculate_power():.0f}W"
        page.update()
    
    # Toggle door function
    def toggle_door(e):
        door_locked.current = not door_locked.current
        if door_locked.current:
            door_status.value = "Door: LOCKED"
            door_button.text = "ON"
            door_button.bgcolor = "#22C55E"
            add_action("door1", "Lock")
        else:
            door_status.value = "Door: UNLOCKED"
            door_button.text = "OFF"
            door_button.bgcolor = "#EF4444"
            add_action("door1", "Unlock")
        current_power_display.value = f"Current Power: {calculate_power():.0f}W"
        page.update()
    
    # Change temperature function
    def change_temperature(e):
        temperature.current = e.control.value
        temp_display.value = f"Set point: {temperature.current:.1f} °C"
        add_action("thermostat", f"Set to {temperature.current:.1f}°C")
        current_power_display.value = f"Current Power: {calculate_power():.0f}W"
        page.update()
    
    # Toggle thermostat function
    def toggle_thermostat(e):
        thermostat_on.current = not thermostat_on.current
        if thermostat_on.current:
            thermostat_button.text = "ON"
            thermostat_button.bgcolor = "#22C55E"
            add_action("thermostat", "Turn ON")
        else:
            thermostat_button.text = "OFF"
            thermostat_button.bgcolor = "#EF4444"
            add_action("thermostat", "Turn OFF")
        current_power_display.value = f"Current Power: {calculate_power():.0f}W"
        page.update()
    
    # Change fan speed function
    def change_fan_speed(e):
        fan_speed.current = int(e.control.value)
        fan_display.value = f"Fan speed: {fan_speed.current}"
        add_action("fan", f"Speed set to {fan_speed.current}")
        current_power_display.value = f"Current Power: {calculate_power():.0f}W"
        page.update()
    
    # Show device details
    def show_light_details(e):
        page.controls.clear()
        
        light_actions = [log for log in action_log if log["device"] == "light1"]
        
        actions_column = ft.Column()
        if light_actions:
            for log in light_actions[:5]:
                actions_column.controls.append(
                    ft.Text(f"{log['time']} - {log['action']} ({log['user']})", size=14, color="#111827")
                )
        else:
            actions_column.controls.append(ft.Text("No recent actions", color="#6B7280"))
        
        details_view = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color="#3B82F6",
                        on_click=lambda e: show_overview(e)
                    ),
                    ft.Text("Smart Home Controller", size=16, color="#111827")
                ], spacing=10),
                ft.Text("Living Room Light Details", size=28, weight=ft.FontWeight.BOLD, color="#2563EB"),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Living Room Light details", size=22, weight=ft.FontWeight.BOLD, color="#3B82F6"),
                        ft.Divider(color="#E5E7EB"),
                        ft.Text(f"ID: light1", size=14, color="#111827"),
                        ft.Text(f"Type: light", size=14, color="#111827"),
                        ft.Text(f"State: {'ON' if light_on.current else 'OFF'}", size=14, color="#2563EB"),
                        ft.Divider(height=20, color="#E5E7EB"),
                        ft.Text("Recent actions", size=18, weight=ft.FontWeight.BOLD, color="#3B82F6"),
                        actions_column,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Back to overview",
                            bgcolor="#3B82F6",
                            color=ft.Colors.WHITE,
                            on_click=lambda e: show_overview(e)
                        ),
                    ]),
                    bgcolor="#FFFFFF",   # LIGHT CARD
                    padding=20,
                    border_radius=10,
                    border=ft.border.all(1, "#E5E7EB"),
                ),
            ]),
            padding=20,
            bgcolor="#F3F4F6",
            expand=True,
        )
        page.add(details_view)
        page.update()
    
    # Assign button click handlers
    light_button.on_click = toggle_light
    door_button.on_click = toggle_door
    thermostat_button.on_click = toggle_thermostat
    temp_slider.on_change = change_temperature
    fan_slider.on_change = change_fan_speed
    
    # Navigation functions
    def show_overview(e):
        page.controls.clear()
        page.add(overview_view)
        page.update()
    
    def show_statistics(e):
        update_chart_view()
        page.controls.clear()
        page.add(statistics_view)
        page.update()
    
    # Chart bars container
    chart_bars = ft.Row([], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.END, height=200)
    
    # Function to update chart
    def update_chart_view():
        chart_bars.controls.clear()
        max_power = max(power_history) if max(power_history) > 0 else 1
        current_hour = datetime.now().hour
        
        for hour_idx, hour_power in enumerate(power_history):
            height = (hour_power / max_power) * 180 if max_power > 0 else 5
            
            if hour_power == 0:
                color = "#22C55E"  # GREEN
            elif hour_power < 50:
                color = "#22C55E"
            elif hour_power < 100:
                color = "#F5A623"   # YELLOW
            elif hour_power < 150:
                color = "#FCD34D"   # LIGHT GOLD
            else:
                color = "#EF4444"   # RED
            
            border = ft.border.all(3, "#3B82F6") if hour_idx == current_hour else None
            
            chart_bars.controls.append(
                ft.Container(
                    width=30,
                    height=max(height, 5),
                    bgcolor=color,
                    border_radius=3,
                    border=border,
                    tooltip=f"Hour {hour_idx}: {hour_power:.0f}W"
                )
            )
    
    # Overview View
    overview_view = ft.Container(
        content=ft.Column([
            # Header
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.HOME, color="#3B82F6", size=32),
                    ft.Text("Smart Home Controller", size=26, weight=ft.FontWeight.BOLD, color="#2563EB"),
                    ft.Container(expand=True),
                    ft.TextButton(
                        "Overview", 
                        on_click=show_overview, 
                        style=ft.ButtonStyle(color="#3B82F6")
                    ),
                    ft.TextButton(
                        "Statistics", 
                        on_click=show_statistics, 
                        style=ft.ButtonStyle(color="#6B7280")
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=ft.border_radius.only(top_left=10, top_right=10),
                border=ft.border.all(1, "#E5E7EB"),
            ),
            
            ft.Container(
                content=ft.Column([
                    # Current Power Display
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.BOLT, color="#2563EB", size=32),
                            current_power_display,
                        ]),
                        bgcolor="#FFFFFF",
                        padding=15,
                        border_radius=10,
                        border=ft.border.all(1, "#E5E7EB"),
                    ),
                    
                    ft.Container(height=10),
                    
                    # On/Off Devices
                    ft.Text("On/Off Devices", size=20, weight=ft.FontWeight.BOLD, color="#111827"),
                    ft.Row([
                        # Living Room Light
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.LIGHTBULB, color="#2563EB", size=28),
                                    ft.Text("Living Room Light", weight=ft.FontWeight.BOLD, color="#111827", size=15),
                                ]),
                                light_status,
                                ft.Text("60W when ON", size=12, color="#6B7280"),
                                ft.Row([
                                    ft.TextButton("Details", on_click=show_light_details, style=ft.ButtonStyle(color="#3B82F6")),
                                    light_button,
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ]),
                            bgcolor="#FFFFFF",
                            padding=15,
                            border_radius=10,
                            border=ft.border.all(1, "#E5E7EB"),
                            expand=True,
                        ),
                        
                        # Front Door
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.DOOR_BACK_DOOR, color="#3B82F6", size=28),
                                    ft.Text("Front Door", weight=ft.FontWeight.BOLD, color="#111827", size=15),
                                ]),
                                door_status,
                                ft.Text("5W when locked", size=12, color="#6B7280"),
                                ft.Row([
                                    ft.TextButton("Details", style=ft.ButtonStyle(color="#3B82F6")),
                                    door_button,
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ]),
                            bgcolor="#FFFFFF",
                            padding=15,
                            border_radius=10,
                            border=ft.border.all(1, "#E5E7EB"),
                            expand=True,
                        ),
                    ], spacing=10),
                    
                    ft.Container(height=10),
                    
                    # Slider Controlled Devices
                    ft.Text("Slider Controlled Devices", size=20, weight=ft.FontWeight.BOLD, color="#111827"),
                    ft.Row([
                        # Thermostat
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.THERMOSTAT, color="#3B82F6", size=28),
                                    ft.Text("Thermostat", weight=ft.FontWeight.BOLD, color="#111827", size=15),
                                ]),
                                temp_display,
                                ft.Text("Base 50W + 10W per °C diff", size=12, color="#6B7280"),
                                temp_slider,
                                ft.Row([
                                    ft.TextButton("Details", style=ft.ButtonStyle(color="#3B82F6")),
                                    thermostat_button,
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ]),
                            bgcolor="#FFFFFF",
                            padding=15,
                            border_radius=10,
                            border=ft.border.all(1, "#E5E7EB"),
                            expand=True,
                        ),
                        
                        # Ceiling Fan
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.AIR, color="#3B82F6", size=28),
                                    ft.Text("Ceiling Fan", weight=ft.FontWeight.BOLD, color="#111827", size=15),
                                ]),
                                fan_display,
                                ft.Text("30W per speed level", size=12, color="#6B7280"),
                                fan_slider,
                                ft.TextButton("Details", style=ft.ButtonStyle(color="#3B82F6")),
                            ]),
                            bgcolor="#FFFFFF",
                            padding=15,
                            border_radius=10,
                            border=ft.border.all(1, "#E5E7EB"),
                            expand=True,
                        ),
                    ], spacing=10),
                ], scroll=ft.ScrollMode.AUTO),
                padding=20,
                expand=True,
            ),
        ]),
        bgcolor="#F3F4F6",
        expand=True,
    )
    
    # Statistics View
    statistics_view = ft.Container(
        content=ft.Column([
            # Header
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.HOME, color="#3B82F6", size=32),
                    ft.Text("Smart Home Controller", size=26, weight=ft.FontWeight.BOLD, color="#2563EB"),
                    ft.Container(expand=True),
                    ft.TextButton(
                        "Overview", 
                        on_click=show_overview, 
                        style=ft.ButtonStyle(color="#6B7280")
                    ),
                    ft.TextButton(
                        "Statistics", 
                        on_click=show_statistics, 
                        style=ft.ButtonStyle(color="#3B82F6")
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=ft.border_radius.only(top_left=10, top_right=10),
                border=ft.border.all(1, "#E5E7EB"),
            ),
            
            ft.Container(
                content=ft.Column([
                    # Power Consumption Chart
                    ft.Text("Power Consumption (24 hours)", size=20, weight=ft.FontWeight.BOLD, color="#111827"),
                    ft.Container(
                        content=ft.Column([
                            chart_bars,
                            ft.Row([
                                ft.Text("1h", size=10, color="#6B7280"),
                                ft.Text("2h", size=10, color="#6B7280"),
                                ft.Text("3h", size=10, color="#6B7280"),
                                ft.Text("4h", size=10, color="#6B7280"),
                                ft.Text("5h", size=10, color="#6B7280"),
                                ft.Text("6h", size=10, color="#6B7280"),
                                ft.Text("7h", size=10, color="#6B7280"),
                                ft.Text("8h", size=10, color="#6B7280"),
                                ft.Text("9h", size=10, color="#6B7280"),
                                ft.Text("10h", size=10, color="#6B7280"),
                                ft.Text("11h", size=10, color="#6B7280"),
                                ft.Text("12h", size=10, color="#6B7280"),
                                ft.Text("13h", size=10, color="#6B7280"),
                                ft.Text("14h", size=10, color="#6B7280"),
                                ft.Text("15h", size=10, color="#6B7280"),
                                ft.Text("16h", size=10, color="#6B7280"),
                                ft.Text("17h", size=10, color="#6B7280"),
                                ft.Text("18h", size=10, color="#6B7280"),
                                ft.Text("19h", size=10, color="#6B7280"),
                                ft.Text("20h", size=10, color="#6B7280"),
                                ft.Text("21h", size=10, color="#6B7280"),
                                ft.Text("22h", size=10, color="#6B7280"),
                                ft.Text("23h", size=10, color="#6B7280"),
                                ft.Text("0h", size=10, color="#6B7280"),
                            ], spacing=5, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([
                                ft.Container(width=15, height=15, bgcolor="#22C55E", border_radius=3),
                                ft.Text("Low (<50W)", size=10, color="#111827"),
                                ft.Container(width=15, height=15, bgcolor="#F5A623", border_radius=3),
                                ft.Text("Medium (50–100W)", size=10, color="#111827"),
                                ft.Container(width=15, height=15, bgcolor="#FCD34D", border_radius=3),
                                ft.Text("High (100–150W)", size=10, color="#111827"),
                                ft.Container(width=15, height=15, bgcolor="#EF4444", border_radius=3),
                                ft.Text("Very High (>150W)", size=10, color="#111827"),
                                ft.Container(width=20, height=15, border=ft.border.all(3, "#3B82F6"), border_radius=3),
                                ft.Text("Current Hour", size=10, color="#111827"),
                            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, wrap=True),
                        ]),
                        bgcolor="#FFFFFF",
                        border=ft.border.all(2, "#3B82F6"),
                        border_radius=10,
                        padding=15,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Action Log
                    ft.Text("Action Log", size=20, weight=ft.FontWeight.BOLD, color="#111827"),
                    ft.Container(
                        content=ft.Column([action_log_table], scroll=ft.ScrollMode.AUTO, height=250),
                        bgcolor="#FFFFFF",
                        border=ft.border.all(2, "#3B82F6"),
                        border_radius=10,
                        padding=10,
                    ),
                ], scroll=ft.ScrollMode.AUTO, spacing=10),
                padding=20,
                expand=True,
            ),
        ]),
        bgcolor="#F3F4F6",
        expand=True,
    )
    
    # Initialize
    add_action("system", "Initialized - All devices OFF")
    update_power_history()
    
    # Show overview by default
    page.add(overview_view)

# Run the app
ft.app(target=main)
