# transitapp.py

import customtkinter as ctk
import customtkinter
from ttkbootstrap.tableview import Tableview

import api

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


def entry_callback():
	address = entry.get()
	coor = api.get_coordinates(address)

	nearby_stops = api.nearby_stops(coor[0], coor[1], 'list')
	box.configure(values=nearby_stops)
	print("Updated")

def create_rows(frame, data):
	""" Create a table for trains and stop times. """
	scrollable_frame_labels = []
	for i in range(len(data)):
		# print(i)
		label = ctk.CTkLabel(master=frame, text=data[0])
		label.grid(row=i, column=0, pady=(0, 20))
		scrollable_frame_labels.append(label)

	# coldata = [
	# 	{"text": "Name"}, # tss_short_name
	# 	{"text": "Times"}, # list_of_times
	# ]

	# table = Tableview(
	# 	master=frame,
	# 	coldata=coldata,
	# 	rowdata=data,
	# 	paginated=True,
	# 	searchable=True,		
	# )
		
	# table.grid(column=2, row=0, rowspan=4, padx=10, pady=10)
	# return table

def box_callback(choice):
	address = entry.get()
	coor = api.get_coordinates(address)
	nearby_stops = api.nearby_stops(coor[0], coor[1], 'dict')
	departure_info = api.stop_departures(nearby_stops[choice])
	# print(departure_info)

	data = []
	for i in departure_info:
		data.append((i[4], i[6]))

	create_rows(scrollable_frame, data)



app = ctk.CTk()
app.geometry("600x300")

# Define grid
app.columnconfigure((0,1), weight=1)
app.columnconfigure(2, weight=15)

app.rowconfigure(0, weight=1)
app.rowconfigure(1, weight=1)
app.rowconfigure(2, weight=1)
app.rowconfigure(3, weight=1)

# Define widgets
main = ctk.CTkFrame(app)

super_frame_2 = ctk.CTkFrame(main)
scrollable_frame = ctk.CTkScrollableFrame(super_frame_2, label_text="Trains and Times", height=20)


# Left to right definitions
super_frame_1 = ctk.CTkFrame(master=main)
entry = ctk.CTkEntry(master=super_frame_1, placeholder_text="Enter...")
button = ctk.CTkButton(master=super_frame_1, text="Submit", width=15, command=entry_callback)
optionbox_var = customtkinter.StringVar(value="Stops")
box = ctk.CTkOptionMenu(master=super_frame_1, variable=optionbox_var, values=[], command=box_callback)


# Pack
main.grid(column=0, row=0, rowspan=4, columnspan=3)

super_frame_1.grid(column=0, row=0, rowspan=4, columnspan=2, padx=10)
entry.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
button.grid(column=1, row=1, padx=10, pady=10, sticky="nsew")
box.grid(column=0, row=3, columnspan=2, pady=30)

super_frame_2.grid(column=2, row=0, rowspan=3, padx=10, pady=10)
scrollable_frame.grid(column=2, row=1, rowspan=2, sticky="nsew")

app.mainloop()




