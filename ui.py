import api_requests
# UI related methods/helper functions, put them here to reduce clutter mostly


# Get input from textbox 1, helper function for set_home()
def get_user_lat(t1):
    return t1.get()


# Get input from textbox 2, helper function for set_home()
def get_user_lon(t2):
    return t2.get()


# Reset home location to input values
def set_home(background, t1, t2):
    # Get input from boxes
    lat = get_user_lat(t1)
    lon = get_user_lon(t2)
    try:
        # Convert to float
        float_lat = float(lat)
        float_lon = float(lon)
        # Invalid latitude
        if float_lat < -90 or float_lat > 90:
            raise ValueError
        # Invalid longitude
        if float_lon < -180 or float_lon > 180:
            raise ValueError
    except ValueError:
        # Print 'Invalid Input'
        background.create_text((45, 460), anchor='w', text="Invalid input", font=('verdana', 10), fill='white',
                               tags='error')
    else:
        user_x, user_y = get_map_loc(float_lat, float_lon)
        # Remove previous error message
        background.delete('error')
        # Remove and replace original home location
        background.delete('home')
        background.create_oval(user_x - 3, user_y - 3, user_x + 3, user_y + 3, fill='GREEN', outline='YELLOW',
                               tags='home')
        # Remove and replace original coordinate text
        background.delete('coord_text')
        background.create_text((5, 370), anchor='w',
                               text="Current home location: " + format_coords(float_lat, float_lon),
                               font=('verdana', 10), fill='white', tags='coord_text')


def set_home2(background, t3):
    location = t3.get()
    lat, lon = api_requests.request_coords_from_location(location)
    if lat == 0 and lon == 0:
        background.create_text((458, 460), anchor='w', text="Invalid Location", font=('verdana', 10), fill='white',
                               tags='error2')
    else:
        user_x, user_y = get_map_loc(lat, lon)
        background.delete('error2')
        background.delete('home')
        background.create_oval(user_x - 3, user_y - 3, user_x + 3, user_y + 3, fill='GREEN', outline='YELLOW',
                               tags='home')
        background.delete('coord_text')
        background.create_text((5, 370), anchor='w',
                               text="Current home location: " + format_coords(lat, lon),
                               font=('verdana', 10), fill='white', tags='coord_text')


# Converts geographic coordinates to pixel dimensions: 180x90 to 720x360
def get_map_loc(lat, lon):
    # Get absolute value of coordinates
    lat_abs = abs(lat)
    lon_abs = abs(lon)
    # East of Prime Meridian
    if lon > 0:
        x = (180 + lon_abs) * 2
    # West of Prime Meridian
    if lon <= 0:
        x = (180 - lon_abs) * 2
    # North of Equator
    if lat > 0:
        y = (90 - lat_abs) * 2
    # South of Equator
    if lat <= 0:
        y = (90 + lat_abs) * 2
    return x, y


# Format coordinate directions for display
def format_coords(lat, lon):
    if lat > 0:
        lat_dir = '°E'
    if lat <= 0:
        lat_dir = '°W'
    if lon > 0:
        lon_dir = '°N'
    if lon <= 0:
        lon_dir = '°S'
    return str(lat) + lat_dir + ", " + str(lon) + lon_dir


# Makes sure window is always centered
def center_window(w, h, root):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
