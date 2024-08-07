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
      categfilename = configdir + 'CategoryMaps.csv'
      counterfilename = configdir + 'CounterpartyMaps.csv'
      vcfilename = configdir + 'BudgetCategories.csv'
      overridefilename = configdir + 'OverrideMaps.csv'

      datadir = 'BudgetData2024/'
      bofafilenames = [ 'BofAExportData-20240101-20240331.csv',
                        'BofAExportData-20240401-20240608.csv', ]
      chasefilenames = ['Chase1964_Activity20240101_20240331.CSV',
                        'Chase1964_Activity20240401_20240608.CSV',
                        'Chase5436_Activity20240101_20240331.CSV',
                        'Chase5436_Activity20240401_20240608.CSV'
                        ]
                        
      budgetdatadir = budgetdir + datadir
      mbdfilename = budgetdatadir + 'MergedBudgetData.csv'
      print (categfilename + '\n' + counterfilename + '\n' + overridefilename + '\n' )
      a = BActivity()
      a.pruneSources()
      a.uploadCounterpartyMaps ( counterfilename )
      a.getValidCategories ( vcfilename )
      a.uploadCategoryMaps ( categfilename )
      a.uploadBudgetMaps ( bmapfilename )
      a.uploadOverrides ( overridefilename )
      a.applyOverrides ( )
      a.write ( mbdfilename )

if __name__ == "__main__":
      main()
