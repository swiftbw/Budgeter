'''
Might be good to make this inherit from dict at some point...
'''
import csv, sys, os, datetime
import BudgetUtils

from BActivity import BActivity

def main():
      files = BudgetUtils.getBudgetFiles ()
      
      a = BActivity()

      for fn in files['BofAFiles']:
            b = BActivity( fn, 'BOFA' )
            a.load(b.getRecords())

      for fn in files['ChaseFiles']:
            c = BActivity( fn, 'CHASE' )
            a.load(c.getRecords())
      
      a.pruneSources()

      a.getValidCategories ( files['ValidCategories'] )

      print ( files['BudgetMap'] )

      bmap = BudgetUtils.BudgetMap (files['BudgetMap'])

      a.uploadOverrides ( files['OverrideMaps'] )
      a.updateCounterparties ( bmap )      
      a.updateCategories ( bmap )      
      a.applyOverrides ( )
      a.write ( files['MergedBudgetData'] )

      u = BActivity()
      u.load(a.getRecords('Unassigned'))
      u.writeRecordsForCat(files['BudgetDataDir']+'UnassignedBudgetData.csv')

if __name__ == "__main__":
      main()
