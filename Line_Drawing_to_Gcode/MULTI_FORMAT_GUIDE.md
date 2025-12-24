# Multi-Format Export Guide
## G-Code, DXF, and SVG Output

The line-to-gcode converter now supports exporting to multiple formats:
- **G-Code (.nc)** - For CNC machining
- **DXF (.dxf)** - For CAD software (AutoCAD, Fusion 360, etc.)
- **SVG (.svg)** - For vector graphics editors (Inkscape, Illustrator, etc.)

---

## Quick Start

### Generate G-Code Only (Default)
```bash
python line_to_gcode.py drawing.jpg
```
Output: `drawing.nc`

### Generate DXF Only
```bash
python line_to_gcode.py drawing.jpg --format dxf
```
Output: `drawing.dxf`

### Generate SVG Only
```bash
python line_to_gcode.py drawing.jpg --format svg
```
Output: `drawing.svg`

### Generate All Formats
```bash
python line_to_gcode.py drawing.jpg --format all
```
Output: `drawing.nc`, `drawing.dxf`, `drawing.svg`

---

## Command-Line Options

### Format Selection
```bash
--format {nc,gcode,dxf,svg,all}
```
- `nc` or `gcode` - G-Code output (default)
- `dxf` - DXF CAD format
- `svg` - SVG vector format
- `all` - Generate all three formats

### Output Filename
```bash
-o, --output FILENAME
```
Specifies base filename (extensions added automatically)

**Examples:**
```bash
# Single format with custom name
python line_to_gcode.py drawing.jpg --format dxf -o my_design
# Output: my_design.dxf

# All formats with custom name
python line_to_gcode.py drawing.jpg --format all -o my_design
# Output: my_design.nc, my_design.dxf, my_design.svg
```

### Skip G-Code Parameters
```bash
--skip-gcode-params
```
Skip machining parameter prompts when only generating DXF/SVG

**Example:**
```bash
# Generate DXF without G-Code prompts
python line_to_gcode.py drawing.jpg --format dxf --skip-gcode-params
```

---

## When to Use Each Format

### G-Code (.nc)
**Use for:**
- CNC machining (X-Carve, Shapeoko, etc.)
- Direct machine control
- Simulation in CAM software

**Includes:**
- Tool paths with Z-axis control
- Feed rates and spindle speeds
- Plunge and retract movements
- Complete machining instructions

**Best for:** Final production, testing toolpaths

### DXF (.dxf)
**Use for:**
- CAD software (AutoCAD, Fusion 360, SolidWorks)
- Further design work
- Dimensioning and measuring
- Combining with other designs
- Laser cutting preparation

**Includes:**
- 2D polylines
- Accurate geometry
- Layer organization
- Units (mm or inches)

**Best for:** Design iteration, CAD integration, laser cutting

### SVG (.svg)
**Use for:**
- Vector graphics editors (Inkscape, Illustrator)
- Web display
- Scaling without quality loss
- Graphic design work
- Further artistic editing

**Includes:**
- Scalable vector paths
- Viewbox for proper scaling
- Metadata and comments
- Web-compatible format

**Best for:** Graphic design, web use, artistic work

---

## Workflow Examples

### Example 1: Quick CNC Machining
```bash
# Draw sketch → Generate G-Code → Machine
python line_to_gcode.py sketch.jpg
# Output: sketch.nc (ready for CNC)
```

### Example 2: Design Refinement
```bash
# Draw sketch → Import to CAD → Refine → Export G-Code
python line_to_gcode.py sketch.jpg --format dxf
# Open sketch.dxf in Fusion 360
# Refine design, add features
# Generate G-Code from Fusion 360
```

### Example 3: Graphic Design
```bash
# Draw sketch → Edit in Inkscape → Final artwork
python line_to_gcode.py sketch.jpg --format svg
# Open sketch.svg in Inkscape
# Add colors, text, effects
# Export as PNG/PDF
```

### Example 4: Complete Workflow
```bash
# Generate all formats for maximum flexibility
python line_to_gcode.py drawing.jpg --format all -o my_project

# Now you have:
# - my_project.nc for CNC machining
# - my_project.dxf for CAD work
# - my_project.svg for graphics/web
```

---

## Format-Specific Details

### G-Code Format
**File Structure:**
```gcode
; Header (tool info, parameters)
G21                     ; Set units
G90                     ; Absolute positioning
M3 S18000               ; Start spindle

; Path commands
G0 X... Y...            ; Rapid move
G1 Z-... F...           ; Plunge
G1 X... Y... F...       ; Cut
G0 Z...                 ; Retract

; Footer
M5                      ; Stop spindle
M2                      ; End program
```

**Parameters Included:**
- Tool diameter
- Cut depth
- Feed rate
- Plunge rate
- Safe height
- Spindle speed

### DXF Format
**Features:**
- R2010 DXF version (widely compatible)
- LWPOLYLINEs for paths
- Layer: "PATHS"
- Units: MM or IN

**Import Settings:**
Most CAD software will auto-detect units. If needed:
- Units are set in DXF header
- Can be changed after import

**Software Compatibility:**
✅ AutoCAD (all versions)
✅ Fusion 360
✅ SolidWorks
✅ FreeCAD
✅ LibreCAD
✅ DraftSight

### SVG Format
**Features:**
- Standard SVG 1.1
- Paths with absolute coordinates
- Viewbox for proper scaling
- Black stroke, no fill
- 0.5 stroke width

**Display:**
- Opens in web browsers
- Scales perfectly to any size
- Preserves all detail

**Software Compatibility:**
✅ Inkscape
✅ Adobe Illustrator
✅ CorelDRAW
✅ Affinity Designer
✅ Web browsers
✅ Vector graphics editors

---

## Scaling and Units

### G-Code Output
Always prompts for:
- Units (mm or inch)
- Material dimensions
- Tool parameters

Paths are scaled to fit material size.

### DXF/SVG Output

**Option 1: Prompt for dimensions**
```bash
python line_to_gcode.py drawing.jpg --format dxf
# Will prompt for output width/height and units
```

**Option 2: Use original dimensions**
```bash
python line_to_gcode.py drawing.jpg --format dxf --skip-gcode-params
# Uses original pixel dimensions
```

**Option 3: Scale in target software**
- Import DXF/SVG
- Scale using software's scale tool
- Most flexible approach

---

## Tips and Best Practices

### For CNC Machining
1. Generate all formats: `--format all`
2. Review DXF in CAD software first
3. Verify dimensions before machining
4. Test G-Code in simulator
5. Keep original files

### For CAD Work
1. Use DXF format
2. Import with correct units
3. Paths are closed polylines
4. Easy to extrude, offset, or modify
5. Can add dimensions and notes

### For Graphics
1. Use SVG format
2. Opens in any vector editor
3. Scale without quality loss
4. Add colors, gradients, effects
5. Export to raster if needed

### For Laser Cutting
1. Generate DXF format
2. Import to laser software
3. Set cut/engrave parameters
4. DXF is standard for laser cutters

---

## Advanced Usage

### Custom Output Names
```bash
# Different names for different formats
python line_to_gcode.py sketch.jpg --format all -o final_design
# Creates: final_design.nc, final_design.dxf, final_design.svg
```

### Batch Processing
```bash
# Process multiple files
for file in *.jpg; do
    python line_to_gcode.py "$file" --format all
done
```

### Integration with Other Tools
```bash
# Generate DXF, then convert to other formats using external tools
python line_to_gcode.py drawing.jpg --format dxf
# Import to Fusion 360 for further work
# Export as STEP, IGES, or other formats
```

---

## File Size Comparison

Typical file sizes for a grape leaf design (123 points):

| Format | File Size | Compression |
|--------|-----------|-------------|
| G-Code (.nc) | 4-6 KB | Plain text |
| DXF (.dxf) | 8-12 KB | Plain text |
| SVG (.svg) | 2-4 KB | Plain text |

All formats are human-readable text files.

---

## Troubleshooting

### DXF Import Issues
**Problem:** Units wrong in CAD software
**Solution:** Set units manually after import, or specify when generating

**Problem:** Paths appear as separate lines
**Solution:** Normal - they're polylines, can be joined if needed

### SVG Display Issues
**Problem:** SVG too small/large in editor
**Solution:** Use viewBox attribute, or scale in editor

**Problem:** Paths not visible
**Solution:** Check stroke color (black by default)

### All Formats
**Problem:** Paths doubled/parallel
**Solution:** Already fixed in current version - uses RETR_EXTERNAL

---

## Format Recommendations

| Use Case | Recommended Format |
|----------|-------------------|
| CNC Machining | G-Code (.nc) |
| Laser Cutting | DXF (.dxf) |
| CAD Design | DXF (.dxf) |
| Graphic Design | SVG (.svg) |
| Web Display | SVG (.svg) |
| 3D Modeling (sketch) | DXF (.dxf) |
| Documentation | SVG (.svg) or DXF (.dxf) |
| Maximum Flexibility | All formats |

---

## Quick Reference

```bash
# G-Code only (default)
python line_to_gcode.py file.jpg

# DXF only
python line_to_gcode.py file.jpg --format dxf

# SVG only
python line_to_gcode.py file.jpg --format svg

# All formats
python line_to_gcode.py file.jpg --format all

# Custom output name
python line_to_gcode.py file.jpg --format all -o mydesign

# Skip G-Code prompts (DXF/SVG only)
python line_to_gcode.py file.jpg --format dxf --skip-gcode-params
```

---

## Installation

Make sure you have all required libraries:

```bash
pip install opencv-python opencv-contrib-python numpy scipy ezdxf
```

Or using requirements.txt:
```bash
pip install -r requirements.txt
```

**Note:** ezdxf is required for DXF export. SVG export uses built-in Python libraries.

---

## Examples

### Grape Leaf - All Formats
```bash
python line_to_gcode.py Handwritten_grapeleaf.jpg --format all -o grapeleaf

# Creates:
# - grapeleaf.nc (G-Code for CNC)
# - grapeleaf.dxf (CAD format)
# - grapeleaf.svg (Vector graphics)
```

### Logo Design - SVG for Web
```bash
python line_to_gcode.py logo_sketch.jpg --format svg --skip-gcode-params -o company_logo

# Creates:
# - company_logo.svg (ready for web or further design work)
```

### Part Template - DXF for CAD
```bash
python line_to_gcode.py template.jpg --format dxf -o part_template

# Creates:
# - part_template.dxf (import to Fusion 360 for 3D modeling)
```

---

## Summary

The multi-format export feature provides maximum flexibility:

✅ **G-Code** for immediate CNC machining
✅ **DXF** for CAD software and laser cutting
✅ **SVG** for graphics and web use
✅ **All formats** for complete workflow coverage

Choose the format(s) that best fit your workflow, or generate all three for maximum flexibility!
