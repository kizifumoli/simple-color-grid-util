# color-grid

Simple script to make a labeled grid of colors. To use

``` bash
python main.py \
  create-color-grid \
  --json-input color-grid.json \
  --output-directory ~/
```

This script takes in a JSON file describing the number of rows/columns in the
color grid, as well as a "data" field containing the colors to put in the image. 

Sample Json:

``` json
{
  "n_rows": 2,
  "n_cols": 3,
  "data": [
    "ffffff",
    "ffffff",
    "ffffff",
    "ffffff",
    "ffffff",
    "000000"
  ]
}
```



