#!/usr/bin/env python3
"""
Example script showing how to use the line_to_gcode converter programmatically
"""

from line_to_gcode import ImageProcessor, SVGProcessor, GCodeGenerator, scale_paths

def example_with_defaults():
    """Example using default parameters"""
    
    # Load an image
    print("Loading image...")
    paths, width, height = ImageProcessor.load_and_process(
        'example.png',
        threshold=127,
        simplify_epsilon=1.0
    )
    
    print(f"Found {len(paths)} paths in {width}x{height} image")
    
    # Define machining parameters
    params = {
        'filename': 'example.png',
        'units': 'mm',
        'material_width': 100,
        'material_height': 100,
        'tool_diameter': 3.175,  # 1/8" in mm
        'cut_depth': 2,
        'feed_rate': 800,
        'plunge_rate': 200,
        'safe_height': 5,
        'spindle_speed': 18000
    }
    
    # Scale paths to material size
    print("Scaling paths...")
    scaled_paths = scale_paths(
        paths,
        width,
        height,
        params['material_width'],
        params['material_height'],
        flip_y=True
    )
    
    # Generate G-Code
    print("Generating G-Code...")
    generator = GCodeGenerator(params)
    generator.generate_from_paths(scaled_paths)
    
    # Save
    output_file = 'example_output.nc'
    generator.save(output_file)
    print(f"Done! G-Code saved to {output_file}")


def example_with_custom_processing():
    """Example with custom path processing"""
    
    # Load image
    paths, width, height = ImageProcessor.load_and_process('example.png')
    
    # Filter paths by size (remove small noise)
    filtered_paths = []
    for path in paths:
        if len(path) > 10:  # Only keep paths with more than 10 points
            filtered_paths.append(path)
    
    print(f"Kept {len(filtered_paths)}/{len(paths)} paths after filtering")
    
    # Custom parameters for delicate work
    params = {
        'filename': 'example.png',
        'units': 'mm',
        'material_width': 50,
        'material_height': 50,
        'tool_diameter': 1.0,  # 1mm bit for fine detail
        'cut_depth': 0.5,      # Shallow cut
        'feed_rate': 300,      # Slow and careful
        'plunge_rate': 100,
        'safe_height': 3,
        'spindle_speed': 20000  # High speed for clean cuts
    }
    
    # Scale and generate
    scaled_paths = scale_paths(filtered_paths, width, height, 
                               params['material_width'], 
                               params['material_height'])
    
    generator = GCodeGenerator(params)
    generator.generate_from_paths(scaled_paths)
    generator.save('delicate_output.nc')


def example_svg():
    """Example processing SVG file"""
    
    print("Loading SVG...")
    paths, width, height = SVGProcessor.load_and_process('example.svg')
    
    print(f"Found {len(paths)} paths in SVG")
    
    # Typical parameters for sign making
    params = {
        'filename': 'example.svg',
        'units': 'inch',
        'material_width': 12,
        'material_height': 12,
        'tool_diameter': 0.125,  # 1/8"
        'cut_depth': 0.0625,     # 1/16"
        'feed_rate': 40,
        'plunge_rate': 15,
        'safe_height': 0.25,
        'spindle_speed': 16000
    }
    
    scaled_paths = scale_paths(paths, width, height,
                               params['material_width'],
                               params['material_height'])
    
    generator = GCodeGenerator(params)
    generator.generate_from_paths(scaled_paths)
    generator.save('sign_output.nc')
    print("Sign G-Code generated!")


def example_pencil_drawing():
    """Example processing pencil drawing with skeletonization"""
    
    print("Loading pencil sketch...")
    
    # For pencil drawings, use skeletonization to find centerline
    paths, width, height = ImageProcessor.load_and_process(
        'pencil_sketch.jpg',
        threshold=127,
        simplify_epsilon=1.0,
        use_skeleton=True,     # Enable skeletonization
        smooth_level=10,       # Higher smoothing for hand-drawn lines
        use_spline=True        # Use spline fitting for smooth curves
    )
    
    print(f"Found {len(paths)} paths after skeletonization")
    
    # Parameters for engraving a sketch
    params = {
        'filename': 'pencil_sketch.jpg',
        'units': 'mm',
        'material_width': 200,
        'material_height': 150,
        'tool_diameter': 1.0,    # Small bit for detail
        'cut_depth': 0.5,        # Shallow engraving
        'feed_rate': 400,        # Moderate speed
        'plunge_rate': 150,
        'safe_height': 5,
        'spindle_speed': 20000   # High speed for clean lines
    }
    
    scaled_paths = scale_paths(paths, width, height,
                               params['material_width'],
                               params['material_height'])
    
    generator = GCodeGenerator(params)
    generator.generate_from_paths(scaled_paths)
    generator.save('sketch_engraving.nc')
    print("Sketch engraving G-Code generated!")


def example_varying_thickness():
    """Example processing artwork with varying line thickness"""
    
    print("Loading artwork with thick lines...")
    
    # Process with skeletonization but moderate smoothing
    paths, width, height = ImageProcessor.load_and_process(
        'marker_drawing.png',
        threshold=150,         # Higher threshold for darker lines
        simplify_epsilon=2.0,  # More simplification
        use_skeleton=True,
        smooth_level=8,        # Moderate smoothing
        use_spline=False       # Use moving average instead of splines
    )
    
    print(f"Extracted {len(paths)} centerline paths")
    
    # Parameters for wood carving
    params = {
        'filename': 'marker_drawing.png',
        'units': 'mm',
        'material_width': 300,
        'material_height': 300,
        'tool_diameter': 3.175,
        'cut_depth': 3,
        'feed_rate': 600,
        'plunge_rate': 200,
        'safe_height': 5,
        'spindle_speed': 18000
    }
    
    scaled_paths = scale_paths(paths, width, height,
                               params['material_width'],
                               params['material_height'])
    
    generator = GCodeGenerator(params)
    generator.generate_from_paths(scaled_paths)
    generator.save('carved_artwork.nc')
    print("Wood carving G-Code generated!")


if __name__ == '__main__':
    print("=== Line to G-Code Examples ===\n")
    print("Uncomment the example you want to run:\n")
    
    # Uncomment one of these:
    # example_with_defaults()
    # example_with_custom_processing()
    # example_svg()
    # example_pencil_drawing()
    # example_varying_thickness()
    
    print("\nEdit this file to uncomment an example function!")
    print("\nNew examples:")
    print("  - example_pencil_drawing(): Process pencil sketch with skeletonization")
    print("  - example_varying_thickness(): Process marker/thick line drawings")
