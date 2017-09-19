# Function
find and open note file from note-Dirs given(support re search).

# Usage

**you should modify config.py firstly**

then ```python note.py recache```

when add new notes into note-Dirs or rename notes,

you should recache in case of wrong results.

## recache

```bash
python note.py recache
```

## search from cache

```bash
python note.py tag1 tag2 ... tagn
```
# Example1
```bash
$ note "java.math.*BigInteger.html"
[✓] read cache from pkfile.
/home/zzp/note/java/jdk-8u144-docs/api/java/math/class-use
  1: └─── BigInteger.html
/home/zzp/note/java/jdk-8u144-docs/api/java/math
  2: └─── BigInteger.html
input id: 
```
# Example2
```python
$ note python module thread
[✓] read cache from pkfile.
/home/zzp/note/python
  1: └─── Module-threadpool-线程池.md
  2: └─── Module-threading-多线程.md
input id: 
```
