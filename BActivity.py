'''
Might be good to make this inherit from dict at some point...
'''
import csv, sys

from QBRecord import QBRecord

class QBActivity:
      def __init__(self, filestr = ""):
            self._filename = filestr
            self._headers = []
            self._max_header = 0
            self._indexes = []
            self._records = []
            self._current_header = []

            in_dataset = 0
            
            try:
                  filehandle = open(self._filename, "r")
                  activity = filehandle.readlines()
                  filehandle.close()

                  for i in activity:
                        line = i.strip(' ')
                        if line[0] == ',':
                              if self._indexes == []:
                                    self._indexes = next ( csv.reader ( [ line ] ) )
                                    in_dataset = 1
                                    if self._indexes[1] == '':
                                          self._indexes = []

                              else:
                                    rcrd = QBRecord(self._current_header, self._indexes, line)
                                    self._records.append ( rcrd )
                        else:
                              if line.find ( 'sub-accounts' ) != -1:
                                    continue

                              header_elem = next ( csv.reader ( [ line ] ) )
                              header_elem = header_elem[0]
                              header_elem = header_elem.strip(' ')

                              if not in_dataset:
                                    continue
                              
                              if header_elem[:5] == "Total":
                                    self._headers.append(self._current_header)
                                    if self._max_header < len ( self._current_header ):
                                          self._max_header = len (self._current_header )
                                    self._current_header = self._current_header[:-1]
                              else:
                                    self._current_header.append(header_elem)
                                    
            except IOError as e:
                  print ( "I/O error({0}): {1}".format(e.errno, e.strerror) )
                  print ( "Unable to open %s for reading.", filestr )

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
      a = QBActivity("/users/swiftb/dev/QBProcessor/TMOSAD2019.csv")
      print ( a._indexes )
      print ( a._max_header )
      print ( len ( a._records ) )
      a.write ( "/users/swiftb/dev/QBProcessor/TMOSAD2019_exp.txt" )

if __name__ == "__main__":
      main()
