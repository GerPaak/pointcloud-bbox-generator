# Point Cloud Bounding Box Generator

A Python tool that processes LAS/LAZ point cloud files and generates a shapefile containing the bounding boxes of each file. 
This is useful for creating spatial indexes, visualizing point cloud coverage, or performing spatial queries on large collections of point cloud data.

## Features

- ✅ Processes both `.las` and `.laz` files
- ✅ Generates ESRI Shapefile with bounding box polygons
- ✅ Includes metadata (filename, coordinates, point count)
- ✅ Progress bar for batch processing
- ✅ Command-line interface with flexible options
- ✅ Error handling for corrupted files
- ✅ Customizable coordinate reference system

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

1. Clone or download this repository
2. Navigate to the project directory
3. Install required packages:

```bash
pip install -r requirements.txt
```

### Alternative Installation

You can also install dependencies individually:

```bash
pip install laspy fiona tqdm
```

## Usage

### Command Line Interface

Basic usage:
```bash
python main.py /path/to/your/pointcloud/folder
```

With custom output folder:
```bash
python main.py /path/to/input/folder -o /path/to/output/folder
```

With custom coordinate reference system:
```bash
python main.py /path/to/input/folder --crs EPSG:3857
```

### Command Line Options

- `input_folder`: Path to folder containing .las/.laz files (required)
- `-o, --output`: Custom output folder path (optional)
- `--crs`: Coordinate reference system for output shapefile (default: EPSG:4326)
- `-h, --help`: Show help message

### Example

```bash
# Process point clouds in the 'data' folder
python main.py ./data

# Process with custom output location
python main.py ./data -o ./results

# Process with UTM Zone 33N coordinate system
python main.py ./data --crs EPSG:32633
```

## Output

The script creates:

1. **Output folder**: `PointCloud_laz_BBOX` (or custom folder if specified)
2. **Shapefile**: `PointCloud_laz_BBOX_{folder_name}.shp` with associated files (.shx, .dbf, .prj)

### Shapefile Attributes

Each polygon feature contains the following attributes:

| Field | Type | Description |
|-------|------|-------------|
| `filename` | String | Original LAS/LAZ filename |
| `x_min` | Float | Minimum X coordinate |
| `x_max` | Float | Maximum X coordinate |
| `y_min` | Float | Minimum Y coordinate |
| `y_max` | Float | Maximum Y coordinate |
| `points` | Integer | Number of points in the file |

## File Structure

```
pointcloud-bbox-generator/
├── main.py              # Main script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Dependencies

- **laspy**: Reading LAS/LAZ point cloud files
- **fiona**: Writing ESRI Shapefiles
- **tqdm**: Progress bars for batch processing

## Supported File Formats

### Input
- `.las` - LAS point cloud files
- `.laz` - Compressed LAZ point cloud files

### Output
- `.shp` - ESRI Shapefile format (with .shx, .dbf, .prj files)

## Error Handling

- **Missing dependencies**: Clear error messages with installation instructions
- **Invalid folder paths**: FileNotFoundError with helpful message
- **No point cloud files**: ValueError if no .las/.laz files found
- **Corrupted files**: Individual file errors are logged as warnings, processing continues
- **Permission errors**: Handled gracefully with informative messages


## Performance Notes

- Processing time depends on the number of files and file sizes
- Large collections (1000+ files) may take several minutes
- Memory usage is minimal as only headers are read
- Progress bar shows real-time processing status

## Troubleshooting

### Common Issues

1. **Import Error**: Install missing dependencies with `pip install -r requirements.txt`
2. **Permission Denied**: Ensure write permissions for output folder
3. **No Files Found**: Check that folder contains .las or .laz files
4. **Coordinate System Issues**: Verify CRS code is valid (e.g., EPSG:4326)

### Getting Help

If you encounter issues:

1. Check that all dependencies are installed
2. Verify input folder contains point cloud files
3. Ensure you have write permissions for the output location
4. Check the console output for specific error messages

## License

This project is released under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Changelog

### Version 1.0.0
- Initial release
- Support for LAS/LAZ files
- ESRI Shapefile output
- Command-line interface
- Progress tracking
- Error handling