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
                  self._budgetmap = getCsvFileAsList ( filename )
            else:
                  self._budgetmap = []
      def getMappedCounterparty ( self, cpty ):
            return "hahahha"
      def getMappedCategory ( self, ctgy ):
            return "hahahahhah"

def main ( ):
      files = getBudgetFiles ()
      print ( 'Budget Data Dir is:  ' + files['BudgetDataDir'] )

if __name__ == "__main__":
      main()
