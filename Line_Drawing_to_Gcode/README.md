# Line Drawing to G-Code Converter

A Python script that converts line drawings (PNG, JPG, SVG) into G-Code for CNC machines like the X-Carve.

## Features

- **Multiple file formats**: PNG, JPG, JPEG, SVG
- **Pencil drawing support**: Handles variable width lines with skeletonization
- **Path smoothing**: Centerline extraction and smooth curve generation
- **Interactive input**: Prompts for all machining parameters
- **Automatic scaling**: Scales your design to fit your material
- **Clean G-Code output**: Properly formatted with comments and headers
- **Customizable**: Adjust threshold, simplification, smoothing, and all cutting parameters

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install opencv-python opencv-contrib-python numpy scipy
```

Note: `opencv-contrib-python` is required for advanced skeletonization. If not available, the script uses an alternative method.

## Usage

### Basic Usage

```bash
python line_to_gcode.py your_drawing.png
```

The script will:
1. Load and process your drawing
2. Ask for machining parameters interactively
3. Generate G-Code file (default: `your_drawing.nc`)

### With Options

```bash
# Specify output file
python line_to_gcode.py drawing.png -o output.gcode

# Adjust threshold for image processing (0-255)
python line_to_gcode.py drawing.png -t 150

# Simplify paths more aggressively
python line_to_gcode.py drawing.png -s 2.0

# FOR PENCIL DRAWINGS: Use skeletonization to find centerline
python line_to_gcode.py pencil_sketch.jpg --skeleton

# Adjust smoothing level (higher = smoother)
python line_to_gcode.py pencil_sketch.jpg --skeleton --smooth 10

# Use spline fitting for very smooth curves
python line_to_gcode.py pencil_sketch.jpg --skeleton --spline
```

## Processing Pencil Drawings

If your drawing has **variable line widths** (like a pencil sketch), use the `--skeleton` flag to find the centerline:

### How it Works

1. **Skeletonization**: Finds the centerline/skeleton of thick lines
2. **Path ordering**: Traces along the skeleton to create continuous paths
3. **Smoothing**: Applies moving average or spline fitting to smooth the result

### Example Commands

```bash
# Basic skeletonization
python line_to_gcode.py my_sketch.jpg --skeleton

# More aggressive smoothing for hand-drawn lines
python line_to_gcode.py my_sketch.jpg --skeleton --smooth 15

# Ultra-smooth with spline fitting
python line_to_gcode.py my_sketch.jpg --skeleton --spline

# Combine with threshold adjustment
python line_to_gcode.py my_sketch.jpg --skeleton --smooth 10 -t 180
```

### When to Use Skeleton Mode

✅ **Use `--skeleton` for:**
- Pencil or pen drawings with varying line thickness
- Marker drawings
- Scanned hand-drawn artwork
- Any image where lines have width/thickness

❌ **Don't use `--skeleton` for:**
- Clean vector-like line art
- High-contrast single-pixel lines
- CAD drawings
- SVG files (already vectorized)

### Smoothing Options

**`--smooth N`** (default: 5)
- Controls moving average window size
- Higher = smoother but less detail
- Range: 3-20
- Good starting point: 5-10

**`--spline`**
- Uses B-spline fitting for very smooth curves
- Best for organic/freehand drawings
- Requires scipy
- Slightly slower but produces fluid curves

## Parameters

When you run the script, you'll be prompted for:

### Units
- **mm** or **inch**

### Material Dimensions
- **Width**: Size of your material/workpiece
- **Height**: Size of your material/workpiece

### Tool Parameters
- **Tool diameter**: Size of your cutting bit (e.g., 3.175mm or 1/8")
- **Cut depth**: How deep to cut into material

### Speeds and Feeds
- **Feed rate**: Speed while cutting (mm/min or inch/min)
- **Plunge rate**: Speed when moving down into material
- **Safe height**: Height for rapid moves above material

### Spindle
- **Spindle speed**: RPM (or 0 for manual control)

### Example Session

```
=== CNC Machining Parameters ===

Units (mm/inch) [mm]: mm

Material dimensions (mm):
  Width [100]: 150
  Height [100]: 200

Tool parameters (mm):
  Tool diameter [3.175]: 3.175
  Cut depth [1]: 2

Speeds and feeds (mm/min):
  Feed rate [500]: 800
  Plunge rate [200]: 200
  Safe height [5]: 5
  Spindle speed (RPM) [0 for manual]: 18000
```

## File Format Support

### PNG/JPG Images
- Converts image to black and white
- Extracts contours/edges as paths
- Use `-t` to adjust threshold (default: 127)
- Use `-s` to simplify paths (higher = fewer points)

**Best practices for images:**
- Use high contrast (black lines on white background)
- Remove noise and artifacts
- Higher resolution = better detail

### SVG Files
- Parses vector paths directly
- Supports M, L, H, V, Z commands
- More accurate than raster images

**Best practices for SVG:**
- Use simple paths (not text or complex shapes)
- Flatten any groups or transformations in your vector editor first
- Export as plain SVG (not Inkscape SVG)

## Tips for Good Results

### Image Preparation

**For clean line drawings:**
1. **Clean lines**: Use black lines on white background
2. **High contrast**: Avoid gray or anti-aliased edges
3. **Closed paths**: For pockets, ensure shapes are closed
4. **Remove text**: Convert text to paths in your design software

**For pencil drawings/sketches:**
1. **Scan at high resolution**: 300+ DPI recommended
2. **Good contrast**: Dark lines on light paper
3. **Consistent pressure**: Try to maintain even line darkness
4. **Clean background**: Erase stray marks and smudges
5. **Use `--skeleton` flag**: Essential for variable width lines
6. **Adjust smoothing**: Start with `--smooth 10` and adjust up/down
7. **Test with splines**: Add `--spline` for organic curves

### Parameter Selection
1. **Tool diameter**: Matches your actual bit
2. **Cut depth**: Start shallow (0.5-1mm) for first tests
3. **Feed rate**: Conservative speeds for your material
   - Wood: 800-1500 mm/min (30-60 in/min)
   - Plastic: 500-1000 mm/min (20-40 in/min)
   - Soft metals: 200-500 mm/min (8-20 in/min)
4. **Safe height**: High enough to clear clamps (typically 5-10mm)

### Testing
1. Run the G-Code in a simulator first (UGS Platform, CAMotics, etc.)
2. Do an "air cut" above the material to verify paths
3. Start with a small test piece

## Output

The script generates standard G-Code with:
- Header with metadata and initialization
- Movement commands (G0 for rapids, G1 for cuts)
- Proper Z-axis control (plunge and retract)
- Footer to return home and stop spindle

### Example G-Code Output

```gcode
; Generated by Line to G-Code Converter
; File: drawing.png
; Tool diameter: 3.175 mm
; Cut depth: 2.0 mm
G21                    ; Set units to mm
G90                    ; Absolute positioning
G17                    ; XY plane
G0 Z5.0000            ; Move to safe height
M3 S18000             ; Start spindle
G4 P2                 ; Dwell 2 seconds

; Path 1/5
G0 X10.5000 Y15.2500  ; Rapid to start
G1 Z-2.0000 F200      ; Plunge
G1 X20.5000 Y15.2500 F800
G1 X20.5000 Y25.2500 F800
...
```

## Troubleshooting

### "No paths found in file"
- Image might be inverted (white lines on black)
- Try adjusting threshold: `-t 200` or `-t 50`
- Increase simplification: `-s 0.5`

### "Paths too complex"
- Reduce image resolution
- Increase simplification: `-s 2.0` or higher
- Clean up drawing in image editor

### "Pencil lines look jaggy/rough"
- Use `--skeleton` flag for variable width lines
- Increase smoothing: `--smooth 15` or `--smooth 20`
- Try spline fitting: `--spline`
- Adjust threshold to capture full line width: `-t 180`

### "Lines are broken/disconnected"
- Lower threshold to capture fainter lines: `-t 100`
- Increase scanning resolution
- Trace over faint areas with darker pencil

### "Too many stray marks"
- Clean up original image in photo editor
- Increase threshold to ignore light marks: `-t 150`
- Use simplification to remove noise: `-s 2.0`

### "Skeleton creates weird branches"
- Indicates lines touching or crossing
- Separate lines in original drawing
- Or manually edit paths in CAM software after generation

### "OpenCV not installed"
- Install: `pip install opencv-python opencv-contrib-python`
- For skeleton mode, opencv-contrib-python is recommended
- Or use SVG files instead

## Advanced Usage

### Custom Defaults

Edit the script to change default values in the `get_user_inputs()` function.

### Batch Processing

Create a shell script to process multiple files:

```bash
#!/bin/bash
for file in *.png; do
    python line_to_gcode.py "$file" -t 127 -s 1.0
done
```

### Integration

The script can be imported as a module:

```python
from line_to_gcode import ImageProcessor, GCodeGenerator

# Load image
paths, width, height = ImageProcessor.load_and_process('drawing.png')

# Scale paths
scaled_paths = scale_paths(paths, width, height, 100, 100)

# Generate G-Code
params = {
    'units': 'mm',
    'tool_diameter': 3.175,
    'cut_depth': 2,
    # ... other params
}
generator = GCodeGenerator(params)
generator.generate_from_paths(scaled_paths)
generator.save('output.nc')
```

## Limitations

- Only supports contour/outline operations (not pockets or drilling)
- SVG parser supports basic path commands (M, L, H, V, Z)
- No support for Bezier curves (approximated as straight lines in SVG)
- No tool compensation (paths follow centerline of tool)

## Safety Reminders

⚠️ **ALWAYS:**
- Test G-Code in a simulator first
- Do an air cut before actual cutting
- Wear safety glasses
- Secure your workpiece properly
- Start with conservative feeds and speeds
- Keep hands clear of moving parts

## License

Free to use and modify for personal and commercial projects.

## Contributing

Suggestions and improvements welcome!
