#!/usr/bin/env python3
"""
Point Cloud Bounding Box Generator

This script processes .las/.laz files in a specified folder and generates
a shapefile containing the bounding boxes of each point cloud file.

Author: Gerasimos Papakostopoulos
License: MIT
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple

try:
    import laspy
    import fiona
    from tqdm import tqdm
except ImportError as e:
    print(f"Error: Required package not found: {e}")
    print("Please install required packages using: pip install -r requirements.txt")
    sys.exit(1)


def get_las_files(folder_path: str) -> List[Path]:
    """
    Get all .las and .laz files from the specified folder.
    
    Args:
        folder_path (str): Path to the folder containing point cloud files
        
    Returns:
        List[Path]: List of Path objects for .las/.laz files
    """
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    files = []
    for ext in ["*.las", "*.laz"]:
        files.extend(folder.glob(ext))
    
    return files


def create_bounding_box_points(header) -> List[Tuple[float, float]]:
    """
    Create bounding box corner points from LAS header information.
    
    Args:
        header: LAS file header containing min/max coordinates
        
    Returns:
        List[Tuple[float, float]]: List of (x, y) coordinate tuples forming a rectangle
    """
    return [
        (header.x_min, header.y_min),  # Bottom-left
        (header.x_min, header.y_max),  # Top-left
        (header.x_max, header.y_max),  # Top-right
        (header.x_max, header.y_min),  # Bottom-right
        (header.x_min, header.y_min)   # Close the polygon
    ]


def process_point_clouds(input_folder: str, output_folder: str = None, crs: str = "EPSG:4326") -> str:
    """
    Process all point cloud files in the input folder and create a shapefile
    with their bounding boxes.
    
    Args:
        input_folder (str): Path to folder containing .las/.laz files
        output_folder (str, optional): Path for output folder. If None, creates
                                     subfolder in input_folder
        crs (str, optional): Coordinate reference system for output shapefile
                           (default: EPSG:4326)    
    Returns:
        str: Path to the created shapefile
    """
    input_path = Path(input_folder)
    folder_name = input_path.name
    
    # Create output folder
    if output_folder is None:
        output_path = input_path / "PointCloud_laz_BBOX"
    else:
        output_path = Path(output_folder)
    
    output_path.mkdir(exist_ok=True)
    
    # Define output shapefile path
    shapefile_path = output_path / f'PointCloud_laz_BBOX_{folder_name}.shp'
    
    # Get all LAS/LAZ files
    las_files = get_las_files(input_folder)
    
    if not las_files:
        raise ValueError(f"No .las or .laz files found in {input_folder}")
    
    print(f"Found {len(las_files)} point cloud files")
    print(f"Output shapefile: {shapefile_path}")
    
    # Define shapefile schema
    schema = {
        'geometry': 'Polygon',
        'properties': {
            'filename': 'str:254',
            'x_min': 'float',
            'x_max': 'float',
            'y_min': 'float',
            'y_max': 'float',
            'points': 'int'
        }
    }
    
    # Process files and create shapefile
    with fiona.open(
        str(shapefile_path), 
        'w', 
        driver='ESRI Shapefile', 
        schema=schema,
        crs=crs  # Use user-specified CRS
    ) as dst:
        
        for las_file in tqdm(las_files, desc="Processing point cloud files"):
            try:
                with laspy.open(str(las_file)) as fh:
                    header = fh.header
                    
                    # Create bounding box polygon
                    bbox_points = create_bounding_box_points(header)
                    
                    # Create feature
                    feature = {
                        'geometry': {
                            'type': 'Polygon',
                            'coordinates': [bbox_points]
                        },
                        'properties': {
                            'filename': las_file.name,
                            'x_min': float(header.x_min),
                            'x_max': float(header.x_max),
                            'y_min': float(header.y_min),
                            'y_max': float(header.y_max),
                            'points': int(header.point_count)
                        }
                    }
                    
                    dst.write(feature)
                    
            except Exception as e:
                print(f"Warning: Could not process {las_file.name}: {e}")
                continue
    
    return str(shapefile_path)


def main():
    """Main function to handle command line arguments and execute processing."""
    parser = argparse.ArgumentParser(
        description="Generate bounding box shapefile from point cloud files (.las/.laz)"
    )
    parser.add_argument(
        "input_folder",
        help="Path to folder containing .las/.laz files"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output folder path (optional, defaults to subfolder in input folder)"
    )
    parser.add_argument(
        "--crs",
        default="EPSG:4326",
        help="Coordinate reference system for output shapefile (default: EPSG:4326)"
    )
    
    args = parser.parse_args()
    
    try:
        # Process point cloud files
        shapefile_path = process_point_clouds(args.input_folder, args.output, args.crs)
        print(f"\nSuccess! Bounding box shapefile created: {shapefile_path}")
        print(f"Coordinate Reference System: {args.crs}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
