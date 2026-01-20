'''
Might be good to make this inherit from dict at some point...
'''

import tkinter as tk
from tkinter import ttk

import csv, sys, os, datetime

class Launcher:
      def __init__ (self, root ):
            self.root = root
            root.title("Launcher")
            mainframe = ttk.Frame(root, padding="3 3 12 12")
            mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
            ttk.Button(mainframe, text="Launch Edit Panel PopUp", command=self.Launch).grid(column=1, row=1, sticky=tk.W)

            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)
            
      def Launch (self):
            entry = {}
            entry['CPartyMatch'] = '*Elden'
            entry['Counterparty'] = 'Elden Ring Superstore'
            entry['Category'] = 'Lala Land'
            print ('Launch MapEntryEditorPopUp')
            mee = MapEntryEditorPopUp (self.root, entry)

class MapEntryEditorPopUp:
      def __init__(self, parent, entry = None):
            if entry == None:
                  print ('ERROR:  No Entry!!!  Cancelling.')
                  return
            self.entry = entry

            self.cpm = tk.StringVar()
            self.cp = tk.StringVar()
            self.ct = tk.StringVar()
            self.cpm.set(self.entry['CPartyMatch'])
            self.cp.set(self.entry['Counterparty'])
            self.ct.set(self.entry['Category'])

            self.tl = tk.Toplevel (parent)
            self.meefr = ttk.Frame(self.tl, padding="3 3 12 12")
            self.wcmapentry = ttk.Entry(self.meefr, textvariable=self.cpm)
            self.wcmapentry.grid(column = 1, row = 1, sticky = (tk.N, tk.S, tk.E, tk.W))
            self.cptymapentry = ttk.Entry(self.meefr, textvariable=self.cp)
            self.cptymapentry.grid(column = 2, row = 1, sticky = (tk.N, tk.S, tk.E, tk.W))
            self.ctgymapentry = ttk.Entry(self.meefr, textvariable=self.ct)
            self.ctgymapentry.grid(column = 3, row = 1, sticky = (tk.N, tk.S, tk.E, tk.W))
            ttk.Button(self.meefr, text = 'Accept', command=self.accept).grid(column = 4, row = 1, sticky=tk.W)
            ttk.Button(self.meefr, text = 'Cancel', command=self.cancel).grid(column = 5, row = 1, sticky=tk.W)
            self.meefr.grid(column=5, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
      def accept (self):
            print ( 'Accepting' )
            self.entry['CPartyMatch'] = self.cpm.get()
            self.entry['Counterparty'] = self.cp.get()
            self.entry['Category'] = self.ct.get()
            self.tl.destroy()
            print ( 'Ha Ha I can still return values!')
            # destroy window and return edited values.
      def cancel ( self ):
            print ( 'Cancelling' )
            self.tl.destroy()
            # destroy window and return None.
            
def main ( ):
      root = tk.Tk()
      Launcher ( root )
      root.mainloop()

if __name__ == "__main__":
      main( )

