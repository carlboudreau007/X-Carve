# Quick Reference Card - Multi-Format Export

## Basic Commands

```bash
# G-Code (default)
python line_to_gcode.py drawing.jpg

# DXF for CAD
python line_to_gcode.py drawing.jpg --format dxf

# SVG for graphics
python line_to_gcode.py drawing.jpg --format svg

# All formats
python line_to_gcode.py drawing.jpg --format all
```

---

## Format Options

| Format | Extension | Best For |
|--------|-----------|----------|
| `nc` or `gcode` | .nc | CNC machining |
| `dxf` | .dxf | CAD software, laser cutting |
| `svg` | .svg | Graphics, web, scaling |
| `all` | All three | Maximum flexibility |

---

## Common Options

```bash
# Custom output name
-o mydesign

# Skip G-Code parameters (DXF/SVG only)
--skip-gcode-params

# Image processing
-t 127          # Threshold (0-255)
-s 2.0          # Simplification
--skeleton      # For thick/variable lines
--smooth 10     # Smoothing level
--spline        # Spline fitting
```

---

## Complete Examples

### Example 1: Quick CNC
```bash
python line_to_gcode.py sketch.jpg
# Output: sketch.nc
# Use immediately on CNC
```

### Example 2: CAD Import
```bash
python line_to_gcode.py sketch.jpg --format dxf -o part_template
# Output: part_template.dxf
# Import to Fusion 360, add features, generate G-Code
```

### Example 3: Logo Design
```bash
python line_to_gcode.py logo.jpg --format svg --skip-gcode-params
# Output: logo.svg
# Edit in Inkscape, add colors, export as PNG
```

### Example 4: Complete Workflow
```bash
python line_to_gcode.py drawing.jpg --format all -o project
# Output: project.nc, project.dxf, project.svg
# CNC machining, CAD work, and graphics - all covered!
```

---

## Workflow Decision Tree

```
What's your next step?

├─ Machine it now?
│  └─ Use: --format nc (default)
│
├─ Edit in CAD first?
│  └─ Use: --format dxf
│
├─ Graphic design work?
│  └─ Use: --format svg
│
└─ Not sure yet?
   └─ Use: --format all
```

---

## File Compatibility

### G-Code (.nc)
- ✅ Universal G-Code Sender (UGS)
- ✅ X-Carve, Shapeoko, etc.
- ✅ CAM simulators
- ✅ Mach3, LinuxCNC

### DXF (.dxf)
- ✅ AutoCAD
- ✅ Fusion 360
- ✅ SolidWorks
- ✅ FreeCAD
- ✅ Laser cutting software

### SVG (.svg)
- ✅ Inkscape
- ✅ Adobe Illustrator
- ✅ Web browsers
- ✅ Affinity Designer
- ✅ CorelDRAW

---

## Tips

💡 **Always generate all formats** if you're unsure of your workflow
💡 **DXF is great** for combining multiple designs in CAD
💡 **SVG scales perfectly** - no quality loss at any size
💡 **G-Code is immediate** - straight to machine

---

## Installation

```bash
pip install opencv-python opencv-contrib-python numpy scipy ezdxf
```

Or:
```bash
pip install -r requirements_multiformat.txt
```

---

## Your Grape Leaf Example

```bash
python line_to_gcode.py Handwritten_grapeleaf.jpg --format all -o grapeleaf
```

**Created files:**
- `grapeleaf.nc` - 147 lines, ready for X-Carve
- `grapeleaf.dxf` - Import to CAD for further work
- `grapeleaf.svg` - Edit in Inkscape or use on web

**All from one command!** 🎉

---

## Need Help?

See **MULTI_FORMAT_GUIDE.md** for complete documentation including:
- Detailed format specifications
- Workflow examples
- Troubleshooting
- Advanced usage
- Integration tips
