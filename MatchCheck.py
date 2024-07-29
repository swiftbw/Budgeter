'''
The purpose of MatchCheck is to identify overlapping Counterparty Match functions.'''
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
      '''
      Load Budget Records from Bank
      '''
      a = BActivity()
      for fn in bofafilenames:
            b = BActivity(budgetdatadir+fn, 'BOFA')
            a.load(b.getRecords())
      for fn in chasefilenames:
            c = BActivity(budgetdatadir+fn, 'CHASE')
            a.load(c.getRecords())

      '''
      Remove entries from non-monitored sources
      '''
      
      a.pruneSources()

      a.getValidCategories ( vcfilename )

      '''
      Load Combined Counterparty and Category mapping file
      '''
      a.uploadBudgetMaps ( bmapfilename )

      '''
      Get list of Counterparties and corresponding matches
      '''
      matchctpydict = a.counterpartyMatches ( )

      dupfilename = budgetdatadir + 'CounterpartyMatchDupes.csv'

      dfhandle = open ( dupfilename, 'w' )
      
      for i in matchctpydict:
            ct = len(matchctpydict[i])
            if ct != 1:
                  print ( i + '\t' + str(ct) + '\n')
                  if ct == 0:
                        dfhandle.write ( i + '\n' )
                  else:
                        for j in matchctpydict[i]:
                              dfhandle.write ( '"' + i + '","' + j + '","' + a._counterpartyMaps[j] + '"\n' )
      dfhandle.close ()
      
      a.updateCounterparties ( )

if __name__ == "__main__":
      main()
