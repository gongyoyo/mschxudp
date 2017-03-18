import struct
from io import SEEK_SET
from io import SEEK_CUR

def read_int(file):
    return struct.unpack("i", file.read(4))[0];

def read_byte(file):
    return struct.unpack("b", file.read(1))[0];

def read_short(file):
    return struct.unpack("h", file.read(2))[0];

#           proto8                   version     phrase_offset_start
# 00000000  6d 73 63 68 78 75 64 70  01 00 00 00 40 00 00 00  |mschxudp....@...|
#          phrase_start phrase_end   phrase_count
# 00000010  48 00 00 00 7e 00 00 00  02 00 00 00 00 00 00 00  |H...~...........|
#           timestamp
# 00000020  29 b8 cc 58 00 00 00 00  00 00 00 00 00 00 00 00  |)..X............|
# 00000030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
#                                                      candidate2
#           phrase_offsets[]         magic       hanzi_offset2
# 00000040  00 00 00 00 1c 00 00 00  08 00 08 00 10 00 01 06  |................|
#           pinyin                   phrase
# 00000050  61 00 61 00 61 00 00 00  61 00 61 00 61 00 61 00  |a.a.a...a.a.a.a.|
#                                                pinyin
#                                          candidate2
#                       magic        hanzi_offset2
# 00000060  61 00 00 00 08 00 08 00  10 00 05 06 62 00 62 00  |a...........b.b.|
#                       phrase
# 00000070  62 00 00 00 62 00 62 00  62 00 62 00 00 00        |b...b.b.b.b...|
# 0000007e

class MschxudpFile(object):
    '''
    classdocs
    '''


    def __init__(self, file_name):
        '''
        Constructor
        '''
        self.open(file_name);
        
    def open(self, file_name):
        self.file_name =  file_name;
        with open(self.file_name, "rb") as file:
            self.proto = str(file.read(8));
            self.version = read_int(file);
            self.phrase_offset_start = read_int(file);
            self.phrase_start = read_int(file);
            self.phrase_end = read_int(file);
            self.phrase_count = read_int(file);
            self.timestamp_p = read_int(file);
            self.timestamp = read_int(file);
            self.timestamp_e = file.read(self.phrase_offset_start-file.tell());
            
            self.phrase_offsets = [];
            for i in range(self.phrase_count):
                offset = read_int(file);
                self.phrase_offsets.append(offset);
            self.phrase_offsets.append(self.phrase_end-self.phrase_start);
            
            self.phrases = [];
            for i in range(self.phrase_count):
                phrase_magic =  read_int(file);
                if phrase_magic != 0x80008:
                    print("---", self.file_name, "0x%X"%file.tell());
                    print("0x%X"%phrase_magic, "!=", 0x80008);
                    raise;
                offset =  read_short(file);
                candidate =  read_byte(file);
                candidate2 =  read_byte(file);
                pinyin = file.read(offset-8).decode('utf-16')[:-1];
                phrase_len = self.phrase_offsets[i+1]-self.phrase_offsets[i]-offset;
                phrase = file.read(phrase_len).decode('utf-16')[:-1];
                self.phrases.append((offset, candidate, 
                                     candidate2, pinyin, phrase));
    
    def dump(self):
        print('proto:', self.proto);
        print('version:', "0x%X"%self.version);
        print('phrase_offset_start:', "0x%X"%self.phrase_offset_start);
        print('phrase_start:', "0x%X"%self.phrase_start);
        print('phrase_end:', "0x%X"%self.phrase_end);
        print('phrase_count:', self.phrase_count);
        #print('timestamp_p:', self.timestamp_p);
        
        from datetime import datetime;
        print('timestamp:', datetime.fromtimestamp(self.timestamp));
        #print('timestamp_e:', self.timestamp_e);
      
        for i in range(self.phrase_count):
            (offset, candidate, 
             candidate2, pinyin, phrase) = self.phrases[i];
            print(i, pinyin, "===", phrase, "@@@", 
                  (candidate, candidate2));
            if offset != len(pinyin)*2+10:
                print(len(pinyin));    
                raise
 

def write_int(file, n):
    return file.write(struct.pack("i", n));
def write_short(file, n):
    return file.write(struct.pack("h", n));


class MschxudpFileBuilder(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.phrases = [];
        self.proto = b'mschxudp'
        self.version = 1;
        self.phrase_offset_start = 0x40;
        
    def add_phrase(self, candidate, pinyin, phrase):
        self.phrases.append((candidate, pinyin, phrase));
    
    def save(self, file_name):
        with open(file_name, 'wb') as file:
            file.write(self.proto);
            assert file.tell() == 8
            write_int(file, self.version);
            write_int(file, self.phrase_offset_start);
            phrase_count = len(self.phrases);
            phrase_start = self.phrase_offset_start + phrase_count*4;
            write_int(file, phrase_start);
            file.seek(4, SEEK_CUR); #phrase_end
            write_int(file, phrase_count);
            file.seek(4, SEEK_CUR); #timestamp_p
            
            from datetime import datetime;
            write_int(file, int(datetime.now().timestamp()));
            
            assert file.tell()+0x1c == self.phrase_offset_start
            
            file.seek(phrase_start, SEEK_SET);
            
            phrase_offsets = [];
            phrase_offset = 0;
            for i in self.phrases:
                #i : (candidate[2], pinyin, phrase)
                phrase_offsets.append(phrase_offset);
                
                pinyin_utf16 = (i[1]+'\0').encode('utf-16-le');
                phrase_utf16 = (i[2]+'\0').encode('utf-16-le');
                offset = 8+len(pinyin_utf16);
                            
                file.write(struct.pack('ihbb', 0x80008, offset, i[0][0], i[0][1]));
                file.write(pinyin_utf16)
                file.write(phrase_utf16);
                
                phrase_offset += offset + len(phrase_utf16);
            
            phrase_end = phrase_start + phrase_offset
            file.seek(0x14, SEEK_SET);
            write_int(file, phrase_end);
            
            file.seek(self.phrase_offset_start, SEEK_SET);
            for i in phrase_offsets:
                write_int(file, i);