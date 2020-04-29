from tkinter import *
from PIL import Image, ImageTk
import api_requests
import ui


def fetch():
    coords = api_requests.request_iss_location()
    global current_latitude, current_longitude
    current_latitude, current_longitude, time_stamp = coords
    draw_iss(current_latitude, current_longitude)
    formatted_coords = ui.format_coords(current_latitude, current_longitude)
    root.title('ISS Sky Scanner LIVE || ' + formatted_coords)
    background.delete('time')
    background.create_text((5, 490), anchor='w', text=time_stamp, tags='time')
    root.after(1000, fetch)


def draw_iss(lat, lon):
    x, y = ui.get_map_loc(lat, lon)
    background.create_oval(x - 1, y - 1, x + 1, y + 1, fill='WHITE', outline='WHITE')
    background.delete('iss')
    background.create_oval(x - 3, y - 3, x + 3, y + 3, fill='RED', outline='YELLOW', tags='iss')


def fetch_geocoder(lat, lon):
    global current_location
    current_location = api_requests.request_location_from_coords(lat, lon)
    background.delete('status')
    background.create_text((160, 390), anchor='w',
                           text="The ISS is currently passing over:",
                           font=('verdana', 14), fill='white', tags='status')
    background.create_text((160, 412), anchor='w',
                           text=current_location,
                           font=('verdana', 12), fill='white', tags='status', width=260)
    root.after(60000, lambda: fetch_geocoder(current_latitude, current_longitude))


# Main window
root = Tk()

# Set borders
root.title('ISS Sky Scanner LIVE')
root.geometry('720x500')
root.resizable(False, False)

# Render background canvas
background = Canvas(root, highlightthickness=0)
background.pack(expand=YES, fill=BOTH)
load_background = Image.open('images/map.jpg')
render_background = ImageTk.PhotoImage(load_background)
background.create_image(0, 0, image=render_background, anchor='nw')

# NASA logo
load_nasa = Image.open('images/nasa.png')
render_nasa = ImageTk.PhotoImage(load_nasa)
background.create_image(640, 430, image=render_nasa)

# Set default home location/text
default_lat = 40.7127
default_lon = -74.0060
def_x, def_y = ui.get_map_loc(default_lat, default_lon)
background.create_oval(def_x - 3, def_y - 3, def_x + 3, def_y + 3, fill='GREEN', outline='YELLOW', tags='home')
background.create_text((5, 370), anchor='w',
                       text="Current home location: " + ui.format_coords(default_lat, default_lon),
                       font=('verdana', 10), fill='white', tags='coord_text')

# Input text-boxes
textbox_1 = Entry(root)
textbox_2 = Entry(root)
textbox_3 = Entry(root)
background.create_window(50, 410, window=textbox_1, width=50, height=22)
background.create_window(110, 410, window=textbox_2, width=50, height=22)
background.create_window(500, 410, window=textbox_3, width=110, height=22)
background.create_text((28, 390), anchor='w', text="Latitude", font=('verdana', 10), fill='white')
background.create_text((83, 390), anchor='w', text="Longitude", font=('verdana', 10), fill='white')
background.create_text((477, 390), anchor='w', text="Location", font=('verdana', 10), fill='white')

# Button to set new location
button_1 = Button(text='Set Home Location', command=lambda: ui.set_home(background, textbox_1, textbox_2))
button_2 = Button(text='Set Home Location', command=lambda: ui.set_home2(background, textbox_3))
background.create_window(80, 440, window=button_1, tags='button')
background.create_window(500, 440, window=button_2, tags='button')

current_latitude = 0
current_longitude = 0
current_location = ""
ui.center_window(720, 500, root)
root.after(0, fetch)
root.after(0, lambda: fetch_geocoder(current_latitude, current_longitude))
root.mainloop()
