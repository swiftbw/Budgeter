'''
Might be good to make this inherit from dict at some point...
'''
import csv, sys, os

class BActivity:
      def __init__(self, filestr = "", ftype = "None"):
            self._filename = filestr
            self._ftype = ftype
            self._headers = ['Date', 'Counterparty', 'Category', 'Amount', 'Source', 'Orig_Cparty']
            self._max_header = 0
            self._indexes = []
            self._records = []
            self._crecords = []
            self._current_header = []
            self._headerMap = {'CHASE' : {'Date' : 'Transaction Date', 'Counterparty' : 'Description', 'Category' : 'Category', 'Amount' : 'Amount', 'Source' : 'None', 'Orig_Cparty' : 'Description' }, 'BOFA' : {'Date' : 'Date', 'Counterparty' : 'Original Description', 'Category' : 'Category', 'Amount' : 'Amount', 'Source' : 'Account Name', 'Orig_Cparty' : 'Original Description' }}

            with open(self._filename, mode='r') as csv_file:
                  csv_reader = csv.DictReader(csv_file)
                  line_count = 0
                  for row in csv_reader:
                        cdentry = {}
                        for key in self._headers:
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
                              print(f'Column names are {", ".join(row)}')
                              line_count += 1
                        else:
                              line_count += 1
                        print ( cdentry )
                  print(f'Processed {line_count} lines.')
                  print(len(self._records))
      def getRecords(self):
            return self._crecords
      def load(self, crecords):
            for record in crecords:
                  self._crecords.append(record)
                  
      def write ( self, filename ):
            try:
                  filehandle = open(filename, "w")

                  filehandle.write (', '.join(self._headers) + '\n')

                  for i in self._crecords:
                        filehandle.write (', '.join(i.values()) + '\n')
                        
                  filehandle.close()
            except:
                  print ( "ERROR in write except\n" )

def main():
      filename = os.environ['HOME']
      filename += '/dev/BudgeterData/'
      bfilename = filename + 'ExportData-35.csv'
      cfilename = filename + 'Chase9789_Activity20230204.CSV'
      ofilename = filename + 'MergedBudgetData.csv'
      a = BActivity(bfilename, 'BOFA')
      b = BActivity(cfilename, 'CHASE')
      a.load(b.getRecords())
      a.write(ofilename)

if __name__ == "__main__":
      main()
