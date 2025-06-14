'''
Might be good to make this inherit from dict at some point...
'''
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

def main ():
      a = BudgetRunner()
      a.run()

if __name__ == "__main__":
      main()
