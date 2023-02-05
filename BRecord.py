'''
'''

import sys, csv

class QBRecord:
      def __init__(self, headers = [], indexes = [], recordstr = ""):
            self._headers = headers
            self._indexes = indexes
            self._record = recordstr
            self._values = []
            try:
                  values = next ( csv.reader ( [ recordstr ] ) )

                  if values[0] != '':
                        print ( self._record )
                        print ( "ERROR:  First column for record not empty.  Exitting.\n" )
                        sys.exit ( )
                  else:
                        if indexes != [] and len ( indexes ) != len ( values ):
                              print ( self._indexes )
                              print ( self._record )
                              print ( self._values )
                              print ( "ERROR:  Headers and values counts do not match.  Exitting.\n" )
                              sys.exit ( )

                  self._values = values

            except:
                  print ( "QBRecord failed in except!\n" )


def main():
      sl = QBRecord ( )
      
if __name__ == "__main__":
      main()
