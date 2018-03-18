This script is created for re-encoding all text files to a target new encoding

It solves the problem of doing it manually. since it searches recursively all included directories, recognizes the old encoding and re-encode.
It can collect statistics while doing it too, such as counts of files, lines and chars.
It can create a dictionary of encodes that has been recognaized and thier associated files.
It can return or print the statistics too.

[USAGE]
the useage is simple: 
1. the initializing:
  - list of directories to search;
  - list of file extension to include in re-encoding;
  - target encoding;
  - number of lines to read from each file (it is uesd for recognizing the source encoding) [RECOMMENDED > 500].

2. calling start_recoding:
  it takes a boolean parameter, it points to collecting the statistics or not.
  
3. if needed, it is possible to print the collected statistics.
