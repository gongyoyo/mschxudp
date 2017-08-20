# mschxudp
打印和构建微软拼音（或五笔）的用户自定义短语文件。

# mschxudp file format
**``_X``** 做后缀的字段表示 win10 1703 与 1607 有改动的部分
```
# win10 1703
#           proto8                   unknown_X   version
# 00000000  6d 73 63 68 78 75 64 70  02 00 60 00 01 00 00 00  |mschxudp..`.....|
#           phrase_offset_start
#                       phrase_start phrase_end  phrase_count
# 00000010  40 00 00 00 48 00 00 00  98 00 00 00 02 00 00 00  |@...H...........|
#           timestamp
# 00000020  49 4e 06 59 00 00 00 00  00 00 00 00 00 00 00 00  |IN.Y............|
# 00000030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
#                                                      candidate2
#           phrase_offsets[]         magic_X     phrase_offset2
# 00000040  00 00 00 00 24 00 00 00  10 00 10 00 18 00 06 06  |....$...........|
#           phrase_unknown8_X        pinyin
# 00000050  00 00 00 00 96 0a 99 20  61 00 61 00 61 00 00 00  |....... a.a.a...|
#           phrase                               magic_X
# 00000060  61 00 61 00 61 00 61 00  61 00 00 00 10 00 10 00  |a.a.a.a.a.......|
#                       phrase_unknown8_X
#                 candidate2
#           offset2                        pinyin
# 00000070  1a 00 07 06 00 00 00 00  a6 0a 99 20 62 00 62 00  |........... b.b.|
#                             phrase
# 00000080  62 00 62 00 00 00 62 00  62 00 62 00 62 00 62 00  |b.b...b.b.b.b.b.|
# 00000090  62 00 62 00 62 00 00 00                           |b.b.b...|
# 00000098

# win10 1607
#           proto8                   version     phrase_offset_start
# 00000000  6d 73 63 68 78 75 64 70  01 00 00 00 40 00 00 00  |mschxudp....@...|
#          phrase_start phrase_end   phrase_count unknown_X
# 00000010  48 00 00 00 7e 00 00 00  02 00 00 00 00 00 00 00  |H...~...........|
#           timestamp
# 00000020  29 b8 cc 58 00 00 00 00  00 00 00 00 00 00 00 00  |)..X............|
# 00000030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
#                                                      candidate2
#           phrase_offsets[]         magic       offset2
# 00000040  00 00 00 00 1c 00 00 00  08 00 08 00 10 00 01 06  |................|
#           pinyin                   phrase
# 00000050  61 00 61 00 61 00 00 00  61 00 61 00 61 00 61 00  |a.a.a...a.a.a.a.|
#                                                pinyin
#                                          candidate2
#                       magic        offset2
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
* `phrase_offsets[N] + offset + len(phrase) == phrase_offsets[N+1]`
* `candidate2` 第一个字节代表短语在候选框位置
# 用法
* 打印
```
./mschxudp.py -d ChsPinyinUDP.lex
```
* 构建

```
$ cat in.txt
,aaa,aaaaa,6,6
,bbbb,bbbbbbbb,7,6
,bb,bbbb,7
|www|WOOOOOOWWWWWWWWWW|8|7
,hhhhh,红红火火恍恍惚惚,4,8
,xd,XD😂😂😂.3,7
$ ./mschxudp.py < in.txt -o out_mschxudp.dat
./mschxudp.py < in.txt 
phrase format(',pinyin,phrase,candidate,candidate2')
((6, 6), 'aaa', 'aaaaa')
((7, 6), 'bbbb', 'bbbbbbbb')
((7, 6), 'bb', 'bbbb')
((8, 7), 'www', 'WOOOOOOWWWWWWWWWW')
((4, 8), 'hhhhh', '红红火火恍恍惚惚')
((7, 6), 'xd', 'XD😂😂😂.3')
outfile = ./out_mschxudp.dat
```

# 与深蓝词库转换工具搭配使用导入其他输入法的词库

1. 打开[深蓝词库转换工具](https://github.com/studyzy/imewlconverter/releases)后,词库输出格式选择**用户自定义短语**
2. 设置自定义短语格式：``,编码,短语,排序位置`` 输出文件名称 aa.txt
3.  $ ./mschxudp.py < aa.txt -o out_mschxudp.dat
