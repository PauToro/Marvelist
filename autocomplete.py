# -*- encoding: utf-8 -*-

#A tkinter widget that features autocompletion.

#Created by Mitja Martini on 2008-11-29.
#http://tkinter.unpythonic.net/wiki/AutocompleteEntry

# encoding: utf-8

import sys
import os
import Tkinter
import sqlite3

__version__ = "1.0"

tkinter_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']

class AutocompleteEntry(Tkinter.Entry):
	#Subclass of Tkinter.Entry that features autocompletion.
	
	#To enable autocompletion use set_completion_list(list) to define 
    #a list of possible strings to hit.
	#To cycle through hits use down and up arrow keys.

	def set_completion_list(self, completion_list):
		self._completion_list = completion_list
		self._hits = []
		self._hit_index = 0
		self.position = 0
		self.bind('<KeyRelease>', self.handle_keyrelease)		

	def autocomplete(self, delta=0):
		#autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits
		if delta: # need to delete selection otherwise we would fix the current position
			self.delete(self.position, Tkinter.END)
		else: # set position to end so selection starts where textentry ended
			self.position = len(self.get())
		# collect hits
		_hits = []
		for element in self._completion_list:
			if element.startswith(self.get().lower()):
				_hits.append(element)
		# if we have a new hit list, keep this in mind
		if _hits != self._hits:
			self._hit_index = 0
			self._hits=_hits
		# only allow cycling if we are in a known hit list
		if _hits == self._hits and self._hits:
			self._hit_index = (self._hit_index + delta) % len(self._hits)
		# now finally perform the auto completion
		if self._hits:
			self.delete(0,Tkinter.END)
			self.insert(0,self._hits[self._hit_index])
			self.select_range(self.position,Tkinter.END)
			
	def handle_keyrelease(self, event):
		#event handler for the keyrelease event on this widget
		if event.keysym == "BackSpace":
			self.delete(self.index(Tkinter.INSERT), Tkinter.END) 
			self.position = self.index(Tkinter.END)
		if event.keysym == "Left":
			if self.position < self.index(Tkinter.END): # delete the selection
				self.delete(self.position, Tkinter.END)
			else:
				self.position = self.position-1 # delete one character
				self.delete(self.position, Tkinter.END)
		if event.keysym == "Right":
			self.position = self.index(Tkinter.END) # go to end (no selection)
		if event.keysym == "Down":
			self.autocomplete(1) # cycle to next hit
		if event.keysym == "Up":
			self.autocomplete(-1) # cycle to previous hit
		# perform normal autocomplete if event is a single key or an umlaut
		if len(event.keysym) == 1 or event.keysym in tkinter_umlauts:
			self.autocomplete()
			
#Get character names for autocomplete entry
conn = sqlite3.connect('databases/MarvelNetworks')
cursor = conn.execute("SELECT APIname FROM nameMatch;")
charNamesList = []
for row in cursor:
	name = row[0]
	name = name.title()
	charNamesList.append(name)
conn.close()

#Run a mini application to test the AutocompleteEntry Widget.#
root = Tkinter.Tk(className=' AutocompleteEntry demo')
entry = AutocompleteEntry(root)
entry.set_completion_list(charNamesList)
entry.pack()
root.mainloop()