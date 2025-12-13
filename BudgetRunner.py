'''
Might be good to make this inherit from dict at some point...
'''
from tkinter import *
from tkinter import ttk

import csv, sys, os, datetime
import BudgetUtils

from BActivity import BActivity

class BudgetRunner:
      def __init__ (self):
            self._files = BudgetUtils.getBudgetFiles ()
      
            self._activity = BActivity()

            for fn in self._files['BofAFiles']:
                  b = BActivity( fn, 'BOFA' )
                  self._activity.load(b.getRecords())

            for fn in self._files['ChaseFiles']:
                  c = BActivity( fn, 'CHASE' )
                  self._activity.load(c.getRecords())
      
            self._activity.pruneSources()

            self._activity.getValidCategories ( self._files['ValidCategories'] )

      def run (self):
            print ( self._files['BudgetMap'] )

            bmap = BudgetUtils.BudgetMap (self._files['BudgetMap'])

            self._activity.uploadOverrides ( self._files['OverrideMaps'] )
            self._activity.updateCounterparties ( bmap )      
            self._activity.updateCategories ( bmap )      
            self._activity.applyOverrides ( )
            self._activity.write ( self._files['MergedBudgetData'] )

            u = BActivity()
            u.load(self._activity.getRecords('Unassigned'))
            u.writeRecordsForCat(self._files['BudgetDataDir']+'UnassignedBudgetData.csv')

class BudgetControlPanel:
      def __init__ (self, root):
            self._budget = BudgetRunner ()

            self._unassignedRecords = []
            self._unassignedRecordsStringVar = StringVar()
            self._unassignedRecordsStringVar.set( self._unassignedRecords)

            self._assignedRecords = []
            self._assignedRecordsStringVar = StringVar()
            self._assignedRecordsStringVar.set(self._assignedRecords)

            self._validCategories = []
            self._validCategoriesStringVar = StringVar()
            self.getValidCategories()
            
            self._validCounterparties = []
            self._validCounterpartiesStringVar = StringVar()

            self._cpartyMap = {}
            root.title("Budget Control Panel")
            mainframe = ttk.Frame(root, padding="3 3 12 12")
            mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

            self._cpartyselection = StringVar()
            self._cpartymapping = StringVar()
            self._budgetMapUpdates = {}

            ttk.Button(mainframe, text="Run Budget", command=self.Exec).grid(column=1, row=1, sticky=W)
            ttk.Button(mainframe, text="Load Unassigned", command=self.LoadUnassigned).grid(column=1, row=2, sticky=W)

            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)
            
            # Set up Counterparty List Frame
            cpartyframe = ttk.Frame(mainframe, borderwidth = 1, relief = 'ridge', padding="3 3 12 12")
            cpartyframe.grid(column=1,row=3,sticky=(N,W,E,S))

            ttk.Label(cpartyframe,text="Counterparty Select").grid(column = 1, row = 1,sticky = (N,W,S,E))
            
            ttk.Label(cpartyframe,text="Unassigned").grid(column = 1, row = 2,sticky = (N,W,S,E))
            self._unassignedListbox = Listbox(cpartyframe, listvariable = self._unassignedRecordsStringVar, height=5)
            self._unassignedListbox.grid(column = 1, row=3,sticky = (N,W,S,E))
            self._unassignedListbox.bind('<<ListboxSelect>>', self.ULBSelect)

            ttk.Label(cpartyframe,text="Assigned").grid(column = 1, row = 4,sticky = (N,W,S,E))
            self._assignedListbox = Listbox(cpartyframe, listvariable = self._assignedRecordsStringVar, height=5)
            self._assignedListbox.grid(column = 1, row=5,sticky = (N,W,S,E))

            # Set up Mapping Frame
            mapframe = ttk.Frame(mainframe, borderwidth = 1, relief = 'ridge', padding="3 3 12 12")

            self._wildcardsvar = StringVar()
            self._cpartysvar = StringVar()
            self._catmapsvar = StringVar()
            self._mapfromlist = IntVar()
            self._mapfromlist.set(1)

            ttk.Label(mapframe,text="Map Counterparty").grid(column = 1, row = 1,sticky = (N,W,S,E))
            ttk.Label(mapframe,text="Wildcard Match").grid(column = 1, row = 2,sticky = (N,W,S,E))
            ttk.Entry(mapframe,textvariable = self._wildcardsvar, width = 15).grid(column = 2, row = 2, sticky = (N,W,S,E))
            ttk.Label(mapframe,text="Select Counterparty From List?").grid(column = 1, row = 3,sticky = (N,W,S,E))

            self._newCpartyLbl = ttk.Label(mapframe, text="Create New Counterparty:")
            self._newCpartyLbl.grid(column = 1, row = 4, sticky = W)
            self._newCpartyLbl.grid_remove()
            
            self._newCpartyEntry = ttk.Entry(mapframe, width=16, textvariable = self._cpartysvar)
            self._newCpartyEntry.grid(column=2,row=4,sticky = E)
            self._newCpartyEntry.grid_remove()

            self._mfcheckbutton = ttk.Checkbutton(mapframe,text="yes / no", variable = self._mapfromlist, command = self.ToggleCpartyList)
            self._mfcheckbutton.grid(column = 2, row = 3,sticky = (N,W,S,E))
            mapframe.grid(column=2,row=3,sticky=(N,W,E,S))

            # Set up Selection Frame
            selectframe = ttk.Frame(mainframe, borderwidth = 1, relief = 'ridge', padding="3 3 12 12")
            ttk.Label(selectframe,text="Selection Lists").grid(column = 1, row = 1,sticky = (N,W,S,E))
            selectframe.grid(column=3,row=3,sticky=(N,W,E,S))
            self._validCatsLbl = ttk.Label(selectframe,text="Valid Categories")
            self._validCatsLbl.grid(column = 1, row = 2,sticky = (N,W,S,E))
            self._validCatsLbl.grid_remove()
            self._validCatsListbox = Listbox(selectframe, listvariable = self._validCategoriesStringVar, height=5)
            self._validCatsListbox.grid(column = 1, row=3,sticky = (N,W,S,E))
            self._validCatsListbox.bind('<<ListboxSelect>>', self.VCSelect)
            self._validCatsListbox.grid_remove()

            self._validCPartyLbl = ttk.Label(selectframe,text="Valid Counterparties")
            self._validCPartyLbl.grid(column = 1, row = 2,sticky = (N,W,S,E))
            self.getCPartyMap()
                  
            self._validCPartyListbox = Listbox(selectframe, listvariable = self._validCounterpartiesStringVar, height=5)
            self._validCPartyListbox.grid(column = 1, row=3,sticky = (N,W,S,E))
            self._validCPartyListbox.bind('<<ListboxSelect>>', self.VCPSelect)

            ttk.Label(mainframe, textvariable = self._cpartyselection, width = 15, borderwidth = 1, relief = 'ridge').grid(column = 1, row = 4, sticky = (N, W, S, E))            
            mappingentry = ttk.Frame(mainframe, borderwidth = 1, relief = 'ridge')
            mappingentry.grid(column = 2, row = 4, sticky = (N, W, S, E))
            ttk.Label(mappingentry, textvariable = self._wildcardsvar, width = 20).grid(column = 1, row = 1, sticky = (N, W, S, E))
            ttk.Label(mappingentry, textvariable = self._cpartysvar, width = 10).grid(column = 2, row = 1, sticky = (N, W, S, E))
            ttk.Label(mappingentry, textvariable = self._catmapsvar, width = 10).grid(column = 3, row = 1, sticky = (N, W, S, E))
            ttk.Button(mainframe, text="Save Entry", command=self.SaveEntry).grid(column=3, row=4, sticky=W)
            ttk.Button(mainframe, text="Update Budget Map", command=self.UpdateMap).grid(column=3, row=5, sticky=W)

      def Exec (self):
            print ('Run Budget')
            self._budget.run()
      def LoadUnassigned  (self):
            '''
            self._unassignedRecords = []
            self._unassignedRecordsStringVar = StringVar()
            '''
            print ('Load Unassigned')
            unassigneddictlist = self._budget._activity.getRecords('Unassigned')
            for entry in unassigneddictlist:
                  if self.UnassignedExists( entry["Counterparty"] ):
                        continue
                  self._unassignedRecords.append(entry["Counterparty"])
            self._unassignedRecordsStringVar.set( self._unassignedRecords)
            print(self._unassignedRecords)
      def UnassignedExists(self, cpty):
            for entry in self._unassignedRecords:
                  if cpty == entry:
                        return True
            return False
      def SaveEntry (self):
            print ('Save Entry')
            idx = self._unassignedListbox.curselection()
            value = self._unassignedListbox.get(idx)
            print (value)
            # TODO implement checks to see if map values are set.
            if value == None or value == '':
                  print ( "Nothing Selected" )
                  return
            self._unassignedListbox.delete(idx)
            print (value)
            self._assignedListbox.insert(END, value)
            self._budgetMapUpdates[value] = (self._wildcardsvar.get(), self._cpartysvar.get(), self._catmapsvar.get())
            # TODO clear settings
      def UpdateMap (self):
            print ('Update Map')
            print ( self._budgetMapUpdates )
            keys = [ "CPartyMatch", "Counterparty", "Category" ]
            dl = []
            for i in list(self._budgetMapUpdates.values()):
                  dict={}
                  dict[keys[0]] = i[0]
                  dict[keys[1]] = i[1]
                  dict[keys[2]] = i[2]
                  print ( dict )
                  dl.append(dict)
            BudgetUtils.writeCSVFromDictList ( '/Users/swiftbr/newmap.csv', dl, keys )
                  
      def ToggleCpartyList (self):
            print ('Toggle Counterparty Selection List')
            tclstatus = self._mapfromlist.get()
            print (tclstatus)
            if tclstatus == 0:
                  self._newCpartyLbl.grid()
                  self._newCpartyEntry.grid()
                  self._validCatsLbl.grid()
                  self._validCatsListbox.grid()
                  self._validCPartyLbl.grid_remove()
                  self._validCPartyListbox.grid_remove()
            else:
                  self._newCpartyLbl.grid_remove()
                  self._newCpartyEntry.grid_remove()
                  self._validCatsLbl.grid_remove()
                  self._validCatsListbox.grid_remove()
                  self._validCPartyLbl.grid()
                  self._validCPartyListbox.grid()
      def ULBSelect(self, evt):
            if not evt.widget.curselection():
                  return
            print ( 'Selection made.')
            idx = self._unassignedListbox.curselection()
            value = self._unassignedListbox.get(idx)
            print ( idx, value )
            self._cpartyselection.set(value)
      def getValidCategories ( self ):
            map = BudgetUtils.getCsvFileAsList ( self._budget._files['ValidCategories'] )
            for i in map:
                  self._validCategories.append ( i['Category'] )
            self._validCategoriesStringVar.set(self._validCategories)
      def getCPartyMap ( self ):
            map = BudgetUtils.getCsvFileAsList ( self._budget._files['BudgetMap'] )
            for i in map:
                  key = i['Counterparty']
                  val = i['Category']
                  self._cpartyMap[key] = val
            self._validCounterparties = list(self._cpartyMap.keys())
            self._validCounterpartiesStringVar.set(self._validCounterparties)
      def VCPSelect (self, evt):
            return
      def VCSelect (self, evt):
            if not evt.widget.curselection():
                  return
            idx = evt.widget.curselection()
            value = evt.widget.get(idx)
            self._catmapsvar.set(value) 
            # Set Valid Category into Mapping if in the new counterparty configuration
            print ( 'choosing a valid category.' )
            return
def main ():
      '''
      a = BudgetRunner()
      a.run()
      '''
      root = Tk()
      BudgetControlPanel(root)
      root.mainloop()

if __name__ == "__main__":
      main()
