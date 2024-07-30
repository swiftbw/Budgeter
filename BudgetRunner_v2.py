'''
Might be good to make this inherit from dict at some point...
'''
import csv, sys, os, datetime

from BActivity import BActivity

def main():
      rootdir = os.environ['HOME'] # root directory for all input, output, and config files.
      budgetdir = rootdir + '/Library/Mobile Documents/com~apple~cloudDocs/Documents/Finances/BudgetTracking/'
      configdir = budgetdir + 'BudgeterConfig/'
      bmapfilename = configdir + 'BudgetMap.csv'
      vcfilename = configdir + 'BudgetCategories.csv'
      overridefilename = configdir + 'OverrideMaps.csv'

      datadir = 'BudgetData2024/'
      bofafilenames = [ 'BofAExportData-20240101-20240331.csv',
                        'BofAExportData-20240401-20240630.csv',
                        'BofAExportData-20240701-20240729.csv'
                        ]
      chasefilenames = ['Chase1964_Activity20240101_20240331.CSV',
                        'Chase1964_Activity20240401_20240630.CSV',
                        'Chase1964_Activity20240701_20240726.CSV',
                        'Chase5436_Activity20240101_20240331.CSV',
                        'Chase5436_Activity20240401_20240630.CSV',
                        'Chase5436_Activity20240701_20240729.CSV'
                        ]
                        
      budgetdatadir = budgetdir + datadir
      mbdfilename = budgetdatadir + 'MergedBudgetData.csv'
      print (mbdfilename + '\n' + overridefilename + '\n' )
      a = BActivity()

      for fn in bofafilenames:
            b = BActivity(budgetdatadir+fn, 'BOFA')
            a.load(b.getRecords())

      for fn in chasefilenames:
            c = BActivity(budgetdatadir+fn, 'CHASE')
            a.load(c.getRecords())
      
      a.pruneSources()

      a.getValidCategories ( vcfilename )

      print ( bmapfilename )
      a.uploadBudgetMaps ( bmapfilename )
      a.uploadOverrides ( overridefilename )
      a.updateCounterparties ( )
      a.updateCategories ( )
      a.applyOverrides ( )
      a.write ( mbdfilename )
      nbmdata = budgetdatadir + 'NewBudgetMap.csv'
      a.writeBudgetMaps ( nbmdata )

      u = BActivity()
      u.load(a.getRecords('Unassigned'))
      u.writeRecordsForCat(budgetdatadir+'UnassignedBudgetData.csv')

if __name__ == "__main__":
      main()
