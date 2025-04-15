# photo-collage-generator
A quick utility function I made to combine image files into collages, for use in printing for a scrapbook

### How to Use
* install requirements via `pip install -r requirements.txt`

* Config the below variables to define your outputted collages: (any excluded will just use the default values)
```
NPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
DPI = 300
CARD_WIDTH_INCHES = 6
CARD_HEIGHT_INCHES = 4
GRID_COLUMNS = 2
GRID_ROWS = 1
```

* run the file via `python photo_collage_generator.py`

* outputted images will be saved in the specified output folder

### Future ideas for self to add:
- [ ] integrate directly via google photos so I don't have to download input folder
- [ ] support collage types: expanded (current) vs. cropped
- [ ] build some sort of optimisation to pick the collage pairs to minimise resultant whitespace / image cropping
