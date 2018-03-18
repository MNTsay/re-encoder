class ReEncoder:
    """Re-encode files in a list of directories to a target encoding

    It recognizes the current encoding for each file, reading number of lines (recommended 500), and re-encode them.
    It can generate statistics, how many:
        files, lines and characters. Also a hash table of every encoding and its files
    """

    def __init__(self, dirs=['c:\\invalid'], exts=['cpp', 'h'], tencoding='utf_8', num_lines=500):
        self.__glob = __import__('glob')
        self.__os = __import__('os')
        self.__chardet = __import__('chardet')
        self.__tencoding = tencoding
        self.__dirs = dirs
        self.__exts = exts
        self.__num_lines = num_lines
        self.__reset_stats()

    def start_recoding(self, calc_stats=False):
        """re-encode all files in list of dirs to target encoding recursively
        """
        self.__reset_stats()
        for dir_name in self.__dirs:
            for ext in self.__exts:
                for file_name in self.__glob.iglob(dir_name + '\\**\\*.' + ext, recursive=True):
                    encode = self.__define_encoding(file_name)
                    if calc_stats:
                        self.__collect_stats(encode, file_name)
                    self.__correct_encoding(encode, file_name)

    def __collect_stats(self, encode, file_name):
        """collect statistics while processing files if mode is True
        """
        if encode not in self.__hash.keys():
            self.__hash[encode] = []
        self.__hash[encode].append(file_name)
        self.__files_count += 1
        with open(file_name, 'r', encoding=encode) as fr:
            for line in fr:
                self.__lines += 1
                self.__chars += len(line)

    def get_stats(self):
        """return collected statistics
        """
        return self.__files_count, self.__lines, self.__chars, self.__hash

    def print_stats(self):
        """print statistics
        """
        print("files: {}\tlines: {}\tchars: {}".format(self.__files_count, self.__lines, self.__chars))
        for key, value in self.__hash.items():
            print("{} : {}\n\t\t{}".format(key, len(value), '\n\t\t'.join(value)))

    def __reset_stats(self):
        """reset statistics
        """
        self.__lines = 0
        self.__chars = 0
        self.__files_count = 0
        self.__hash = {}

    def __define_encoding(self, file_name):
        """recognize the encoding of a file
        """
        with open(file_name, 'rb') as f:
            raw_data = b''.join([f.readline() for _ in range(self.__num_lines)])
        return self.__chardet.detect(raw_data)['encoding']

    def __correct_encoding(self, encode, filename):
        """change the encoding to target encoding
        """
        if encode == 'None' or encode == self.__tencoding:
            return
        buffname = '~old' + filename
        self.__os.rename(filename, buffname)
        with open(buffname, 'r', encoding=self.__tencoding) as fr:
            with open(filename, 'w', encoding=self.__tencoding) as fw:
                for line in fr:
                    fw.write(line[:-1] + '\r\n')
        self.__os.remove(buffname)
