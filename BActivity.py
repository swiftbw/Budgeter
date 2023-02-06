'''
Might be good to make this inherit from dict at some point...
'''
import csv, sys, os

class BActivity:
      def __init__(self, filestr = ""):
            self._filename = filestr
            self._headers = []
            self._max_header = 0
            self._indexes = []
            self._records = []
            self._current_header = []

            with open(self._filename, mode='r') as csv_file:
                  csv_reader = csv.DictReader(csv_file)
                  line_count = 0
                  for row in csv_reader:
                        self._records.append(row)
                        if line_count == 0:
                              print(f'Column names are {", ".join(row)}')
                              line_count += 1
#                        print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
                        else:
                              line_count += 1
                        print ( row )
                  print(f'Processed {line_count} lines.')
                  print(len(self._records))
      def write ( self, filename ):
            try:
                  filehandle = open(filename, "w")
                  
                  for i in range ( 0, self._max_header ):
                        filehandle.write ( 'Group ' )
                        filehandle.write ( str ( i ) )
                        filehandle.write ( '\t' )

                  for i in self._indexes[1:]:
                        filehandle.write ( i )
                        filehandle.write ( '\t' )

                  filehandle.write ( '\n' )
              
                  for record in self._records:
                        for i in record._headers:
                              filehandle.write ( i )
                              filehandle.write ( '\t' )
                        for i in range ( self._max_header - len ( record._headers ) ):
                              filehandle.write('\t')
                        for j in record._values[1:]:
                              filehandle.write ( j )
                              filehandle.write ( '\t' )

                        filehandle.write ( '\n' )
                        
                  filehandle.close()
            except:
                  print ( "ERROR in write except\n" )

def main():
      filename = os.environ['HOME']
      filename += '/dev/BudgeterData/'
      filename += 'ExportData-35.csv'
#      filename += 'Chase9789_Activity20230204.CSV'
      a = BActivity(filename)
#      print ( a._indexes )
#      print ( a._max_header )
#      print ( len ( a._records ) )
#      a.write ( "/users/swiftb/dev/QBProcessor/TMOSAD2019_exp.txt" )

if __name__ == "__main__":
      main()
