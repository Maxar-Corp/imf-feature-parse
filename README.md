
# Image Factory Feature Parser

Given an processed image file from Image Factory, we may want to know what processing options were selected.  With this script, users can parse the filename directly from command line.

### Required Tools:

- Python 3.8

### Usage:

```
python3 parse.py <filename>
```


The filename should include an extension (e.g., 'tif', 'nitf')

### Sample Output:

    No filename specified.  Using example filename '104001004E9B7800_dcId1_y1u6j5s.tif'...
    DRA-auto
    8 bit
    ortho-ossim
    SRTM 3
    aps-maxar
    ACOMP
    assembled