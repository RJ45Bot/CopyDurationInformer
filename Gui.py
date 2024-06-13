import PySimpleGUI as sg
import json
from Data import loadData

brands, models, os, durations, brands_list, data_list = loadData()


# Window layout
layout = [
    [
        sg.Column(
            [
                [sg.Text("Brand"), sg.Combo(brands, key="-BRAND-", enable_events=True)],
                [sg.Text("Model"), sg.Combo([], key="-MODEL-", enable_events=True)],
                [sg.Text("OS"), sg.Combo([], key="-OS-", enable_events=True)],
                [sg.Text("Duration"), sg.Text("", key="-DURATION-"), sg.Text("minutes")],
                [sg.Button("Add", key="-ADD-", enable_events=True), sg.Button('Custom', key="-SETTINGS-", enable_events=True)]
            ]
        ),
        sg.VerticalSeparator(),
        sg.Column(
            [
                [sg.Table(values=[], headings=["Brand", "Model", "OS", "Duration"], display_row_numbers=False, key="-TABLE-")],
                [sg.Text("Total Duration: "), sg.Text("", key="-TOTAL-"), sg.Text("minutes")]
            ]
        ),
    ]
]

# Create the window
window = sg.Window("CopyDurationInformer", layout)

table_data = []
# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "-BRAND-":
        window["-MODEL-"].update(values=models[values["-BRAND-"]])
    elif event == "-MODEL-":
        window["-OS-"].update(values=[os[values["-MODEL-"]]])
        window["-DURATION-"].update(value=durations[values["-MODEL-"]])
    elif event == "-ADD-":
        table_data.append([values["-BRAND-"], values["-MODEL-"], values["-OS-"], durations[values["-MODEL-"]]])
        window["-TABLE-"].update(values=table_data)
        total_duration = sum([int(row[3]) for row in table_data])
        window["-TOTAL-"].update(value=f"{total_duration}")
    elif event == "-SETTINGS-":
        # Recreate the popup layout
        playout = [
                        [sg.Text('Brand'), sg.Combo(brands, key="-POPUP_BRAND-")],
                        [sg.Text('Model'), sg.InputText(key="-POPUP_MODEL-")],
                        [sg.Text('OS'), sg.InputText(key="-POPUP_OS-")],
                        [sg.Text('Duration'), sg.InputText(key="-POPUP_DURATION-", enable_events=True), sg.Text('minutes')],
                        [sg.Button('Save', key="-SAVE-"), sg.Button('Cancel', key="-CANCEL-")]
                    ]

        # Create the popup window
        popup = sg.Window('Settings', playout)
        while True:
            event, values = popup.read()
            if event == sg.WINDOW_CLOSED or event == "-CANCEL-":
                break
            elif event == "-POPUP_DURATION-":
                # Check if the input is a number
                if not values["-POPUP_DURATION-"].isdigit():
                    # Clear the input if it's not a number
                    popup["-POPUP_DURATION-"].update('')
            elif event == "-SAVE-":
                new_device = {
                    "Brands": values["-POPUP_BRAND-"],
                    "Device": values["-POPUP_MODEL-"],
                    "Os": values["-POPUP_OS-"],
                    "Time": int(values["-POPUP_DURATION-"])
                }
                data_list.append(new_device)
                with open('data.json', 'w') as file:
                    json.dump(data_list, file)
                for brand in brands_list:
                    if brand.brand_name == values["-POPUP_BRAND-"]:
                        # Create a new Device object and add it to the Brand object
                        brand.add_device(values["-POPUP_MODEL-"], values["-POPUP_OS-"], values["-POPUP_DURATION-"])
                popup.close()
                brands, models, os, durations, brands_list, data_list = loadData()
                break
        popup.close()

window.close()
