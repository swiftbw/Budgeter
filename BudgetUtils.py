'''
Might be good to make this inherit from dict at some point...
'''
import csv, sys, os, datetime

def getBudgetFiles ( ):
      rootdir = os.environ['HOME'] # root directory for all input, output, and config files.
      budgetdir = rootdir + '/Library/Mobile Documents/com~apple~cloudDocs/Documents/Finances/BudgetTracking/'
      configdir = budgetdir + 'BudgeterConfig/'
      bmapfilename = configdir + 'BudgetMap.csv'
      vcfilename = configdir + 'ValidCategories.csv'
      overridefilename = configdir + 'OverrideMaps.csv'

      datadir = 'BudgetData2024/'
      budgetdatadir = budgetdir + datadir

      bofafilenames = [ 'BofAExportData20240101_20240331.csv',
                        'BofAExportData20240401_20240630.csv',
                        'BofAExportData20240701_20240930.csv',
                        'BofAExportData20241001_20241231.csv'
                        ]
      chasefilenames = ['Chase1964_Activity20240101_20240331.CSV',
                        'Chase1964_Activity20240401_20240630.CSV',
                        'Chase1964_Activity20240701_20240930.CSV',
                        'Chase1964_Activity20241001_20241231.CSV',
                        'Chase5436_Activity20240101_20240331.CSV',
                        'Chase5436_Activity20240401_20240630.CSV',
                        'Chase5436_Activity20240701_20240930.CSV',
                        'Chase5436_Activity20241001_20241231.CSV'
                        ]
                        
      mbdfilename = budgetdatadir + 'MergedBudgetData.csv'

      files = {}
      files['MergedBudgetData'] = mbdfilename
      files['BofAFiles'] = []
      files['ChaseFiles'] = []
      files['OverrideMaps'] = overridefilename
      files['BudgetMap'] = bmapfilename
      files['ValidCategories'] = vcfilename
      files['BudgetDataDir'] = budgetdatadir
      
      for fn in bofafilenames:
            files['BofAFiles'].append ( budgetdatadir + fn )
 
      for fn in chasefilenames:
            files['ChaseFiles'].append ( budgetdatadir + fn )

      return files

def getCsvFileAsList ( filename ):
      map = []
      with open(filename, mode='r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                  map.append(row)
      csv_file.close
      return map

def ExactMatch ( instr = "", pattern = "" ):
      response = True
      if instr != pattern:
            return False
      else:
            return True

def WildCardMatch ( instr = "", pattern = "" ):
      response = True
      if pattern[0] == '*':
            wildcard = True
            pattern = pattern[1:]

      if instr.find(pattern) == -1:
            return False
      else:
            return True

class BudgetMap:
      def __init__( self, filename = "" ):
            if filename != "":
                  self._budgetMap = getCsvFileAsList ( filename )
            else:
                  self._budgetMap = []
      def getMappedCounterparty ( self, cpty ):
            if self._budgetMap == None or self._budgetMap == []:
                  print ( "ERROR:  No BudgetMap Loaded when trying to map " + str ( cpty ) + ".  Exitting...\n" )
                  sys.exit ( 0 )
            for i in self._budgetMap:
                  if WildCardMatch ( cpty, i[ 'CPartyMatch' ] ):
                        return i[ 'Counterparty' ]
            print ( "WARNING:  Couldn't find match for Counterparty " + str ( cpty ) + " in BudgetMap.  Setting Counterparty to " + str ( cpty ) + ".\n" )
            return cpty
      def getMappedCategory ( self, ctgy ):
            if self._budgetMap == None or self._budgetMap == []:
                  print ( "ERROR:  No BudgetMap Loaded when trying to map " + str ( ctgy ) + ".  Exitting...\n" )
                  sys.exit ( 0 )
            for i in self._budgetMap:
                  if ExactMatch ( ctgy, i[ 'Counterparty' ] ):
                        return i[ 'Category' ]
            print ( "WARNING:  Couldn't find match for Counterparty " + str ( ctgy ) + " in BudgetMap.  Setting Category to 'Unassigned'.\n" )
            return 'Unassigned'

def main ( ):
      files = getBudgetFiles ()
      print ( 'Budget Data Dir is:  ' + files['BudgetDataDir'] )

if __name__ == "__main__":
      main()
