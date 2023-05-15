# gui.py

import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import api



ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.geometry("400x600")



# Action methods
def entry_callback():
	address = entry.get()

	try: 
		coor = api.get_coordinates(address)
		stops = api.nearby_stops(coor[0], coor[1])

		box.configure(values=stops)
		box.set("Choose Stop")	

	except IndexError:
		print('[Error]: Enter Real Address.')


def box_callback(choice):

	address = entry.get()
	coor = api.get_coordinates(address)
	stops = api.nearby_stops(coor[0], coor[1], 'dict')

	departure_info = api.stop_departures(stops[choice])

	for i in departure_info:

		color = i[5]
		frame = ctk.CTkFrame(master=bottom_frame, fg_color="#"+color, width=1000, height=500)
		frame.pack(padx=10, pady=5)

		text_box = ctk.CTkTextbox(master=frame, height=100, width=250)
		text_box.insert("0.0", i[3] + '\n')

		text_box.insert(float(len(i[3])), i[6])

		text_box.configure(state="disabled")
		text_box.pack(padx=20, pady=10)


# GUI Structure
#
# (root) Frame
top_frame = ctk.CTkFrame(master=root, width=1000, height=250)
# (top_frame) Input Box
entry = ctk.CTkEntry(master=top_frame, placeholder_text="Enter address...")
# (top_frame) Submit Button
button = ctk.CTkButton(master=top_frame, text='Submit', command=entry_callback)

# (top_frame) Option Menu
box = ctk.CTkOptionMenu(master=top_frame, values=[], command=box_callback)

# (root) Frame
bottom_frame = ctk.CTkFrame(master=root, fg_color="light gray", width=1000, height=500)


top_frame.pack(padx=20, pady=10)
entry.pack(padx=20, pady=10)
button.pack(padx=20, pady=10)

box.pack(padx=20, pady=10)
box.set("")

bottom_frame.pack()



root.mainloop()