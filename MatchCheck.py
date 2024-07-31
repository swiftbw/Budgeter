'''
The purpose of MatchCheck is to identify overlapping Counterparty Match functions.'''
import csv, sys, os, datetime
import BudgetUtils
from BActivity import BActivity

def main():
      files = BudgetUtils.getBudgetFiles ( )

      mbd = BudgetUtils.getCsvFileAsList ( files [ 'MergedBudgetData' ] )
      
      with open(self._filename, mode='r', encoding = 'utf-8-sig') as csv_file:
          csv_reader = csv.DictReader(csv_file)
          line_count = 0
          for row in csv_reader:
              cdentry = {}
              for key in self._headers:
                  if key == 'Month':
                      dt = row[self._headerMap[self._ftype]['Date']]
                      dto = datetime.datetime.strptime(dt, '%m/%d/%Y')
                      month = dto.strftime('%b')
                      cdentry[key] = month
                  else:
                      if key != 'Source':
                          cdentry[key] = row[self._headerMap[self._ftype][key]]
                      else:
                          if self._ftype == 'CHASE':
                              cdentry[key] = "Chase"
                          else:
                              cdentry[key] = row[self._headerMap[self._ftype][key]]
              self._crecords.append(cdentry)
              self._records.append(row)
              if line_count == 0:
                  line_count += 1
              else:
                  line_count += 1
          print(f'Processed {line_count} lines.')

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
