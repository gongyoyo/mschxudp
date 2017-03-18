# mschxudp
easy dump and build mschxudp(Win10 pinyin user define phrase) file.

打印和构建微软拼音的用户自定义短语文件。

# mschxudp file format
```
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
```
* `proto :  'mschxudp'`
* `phrase_offset_start + 4*phrase_count == phrase_start`
* `phrase_start + phrase_offsets[N] == magic(0x00080008)`
* `pinyin&phrase: utf16-le string`
* `hanzi_offset = 8 + len(pinyin)`
* `phrase_offsets[N] + hanzi_offset + len(phrase) == phrase_offsets[N+1]`

# usage
* dump
```
./mschxudp.py -d ChsPinyinUDP.lex
```
* build
```
$ ./mschxudp.py [-o out.txt]
Enter a phrase(',pinyin,phrase,candidate,candidate2'):,aaa,bbbb,2,3
Enter a phrase(',pinyin,phrase,candidate,candidate2'):#bbbbb#不不不不不不不不不,322#3#5   
outfile = out.txt
```


