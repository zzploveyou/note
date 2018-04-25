# Function
find and open note file from note-Dirs given(support re search).

# Usage

you should edit ```config.json``` firstly.

example of config.json:
```
{
    "DIRS":["/home/zzp/note"],
    "MAPS":{
        "jdk": "/home/zzp/note/java/jdk-docs/index.html",
        "re": "/home/zzp/note/python/re.md"
    }
}
```

then ```python note.py --recache```

when add new notes into note-Dirs or rename notes,

you should recache in case of wrong results.

## help
```bash
python note.py -h
```

## search from cache

```bash
alias note = "python note.py -k"
note tag1 tag2 ... tagn
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
```bash
$ note python module thread
[✓] read cache from pkfile.
/home/zzp/note/python
  1: └─── Module-threadpool-线程池.md
  2: └─── Module-threading-多线程.md
input id: 
```
# Example3
```bash
# find all files that is not with the suffix "html".
$ note "[^h][^t][^m][^l]$"
```
