# Processing Mode Quick Reference

## When to Use Each Mode

### Standard Mode (Default)
```bash
python line_to_gcode.py drawing.png
```

**Best for:**
- Clean, single-pixel line art
- Vector-like drawings
- High-contrast black lines on white
- CAD exports saved as images
- Technical drawings

**Characteristics:**
- Uses contour detection
- Fast processing
- Best accuracy with clean edges
- Minimal smoothing needed

---

### Skeleton Mode
```bash
python line_to_gcode.py sketch.jpg --skeleton
```

**Best for:**
- Pencil drawings with varying thickness
- Hand-drawn sketches
- Marker or pen drawings
- Scanned artwork
- Any lines with width/thickness

**Characteristics:**
- Finds centerline of thick lines
- Handles variable line widths
- Requires smoothing adjustment
- Slightly slower processing

**What it does:**
1. Converts thick lines to single-pixel skeleton
2. Traces along skeleton to create paths
3. Applies smoothing to clean up result

---

### Skeleton + Smoothing
```bash
python line_to_gcode.py sketch.jpg --skeleton --smooth 15
```

**Best for:**
- Rough or shaky hand-drawn lines
- Scans with noise or texture
- Quick sketches
- Lines that need significant cleanup

**Smoothing values:**
- `--smooth 3-5`: Minimal smoothing (preserves detail)
- `--smooth 5-10`: Normal smoothing (default: 5)
- `--smooth 10-15`: Aggressive smoothing (removes roughness)
- `--smooth 15-20`: Very aggressive (may lose some detail)

---

### Skeleton + Spline
```bash
python line_to_gcode.py sketch.jpg --skeleton --spline
```

**Best for:**
- Organic, flowing lines
- Artistic curves
- When you want very smooth results
- Calligraphy or brush strokes

**Characteristics:**
- Uses B-spline curve fitting
- Produces mathematically smooth curves
- Best for freehand artistic work
- Requires scipy library
- Slightly longer processing time

**Note:** Spline fitting works best with `--smooth 5-10`. Very high smoothing before spline fitting may over-simplify.

---

## Quick Decision Guide

```
Is your drawing...

┌─ Single-pixel clean lines? 
│  └─ Use: Default mode
│
├─ Thick or variable width lines?
│  ├─ Fairly neat drawing?
│  │  └─ Use: --skeleton
│  │
│  ├─ Rough/shaky lines?
│  │  └─ Use: --skeleton --smooth 15
│  │
│  └─ Want very smooth curves?
│     └─ Use: --skeleton --spline
│
└─ SVG file?
   └─ Use: Default mode (no skeleton needed)
```

---

## Examples with Real-World Scenarios

### Scenario 1: CAD Export
**Input:** Technical drawing exported as PNG
**Command:** `python line_to_gcode.py technical.png`
**Why:** Clean lines, no need for skeleton

### Scenario 2: Quick Pencil Sketch
**Input:** Photo of pencil sketch on paper
**Command:** `python line_to_gcode.py sketch.jpg --skeleton --smooth 10 -t 140`
**Why:** Variable pencil width, needs centerline + smoothing, darker threshold for pencil

### Scenario 3: Artistic Calligraphy
**Input:** Scan of brush lettering
**Command:** `python line_to_gcode.py calligraphy.jpg --skeleton --spline --smooth 8`
**Why:** Thick brush strokes need skeleton, flowing curves benefit from splines

### Scenario 4: Marker Drawing on Whiteboard
**Input:** Photo of whiteboard drawing
**Command:** `python line_to_gcode.py whiteboard.jpg --skeleton --smooth 12 -t 160`
**Why:** Thick marker lines, possible shadows/reflections need higher threshold

### Scenario 5: Detailed Illustration
**Input:** Pen drawing with consistent line weight
**Command:** `python line_to_gcode.py illustration.png --skeleton --smooth 5`
**Why:** Some line width but detailed, minimal smoothing to preserve detail

---

## Combining Options

You can combine multiple options for best results:

```bash
# Pencil sketch with lots of cleanup
python line_to_gcode.py rough_sketch.jpg \
    --skeleton \
    --smooth 15 \
    --spline \
    -t 150 \
    -s 2.0

# Professional engraving from photo
python line_to_gcode.py photo_trace.jpg \
    --skeleton \
    --smooth 8 \
    --spline \
    -t 130 \
    -o final_engraving.nc
```

**Option meanings:**
- `--skeleton`: Use skeletonization for thick lines
- `--smooth N`: Apply smoothing (3-20)
- `--spline`: Use spline curve fitting
- `-t N`: Threshold for binarization (0-255)
- `-s N`: Path simplification (higher = fewer points)
- `-o FILE`: Output filename

---

## Troubleshooting Decision Tree

**Lines look jagged:**
→ Increase `--smooth` value
→ Add `--spline` flag

**Too smooth, losing detail:**
→ Decrease `--smooth` value
→ Remove `--spline` flag
→ Decrease `-s` simplification

**Paths broken/disconnected:**
→ Lower `-t` threshold
→ Check original image quality
→ Ensure lines are connected in original

**Too many small fragments:**
→ Increase `-t` threshold
→ Clean original image
→ Increase `-s` simplification

**Lines too thick/wrong shape:**
→ Add `--skeleton` flag
→ Adjust `-t` threshold

**Skeleton creates branches:**
→ Lines are crossing in original
→ Separate or clean up original
→ Or edit in CAM software after generation

---

## Performance Notes

**Processing Speed (fastest to slowest):**
1. Default mode (contour detection)
2. Skeleton mode
3. Skeleton + smoothing
4. Skeleton + spline

**Typical Processing Times** (1000x1000 image):
- Default: < 1 second
- Skeleton: 1-3 seconds
- Skeleton + spline: 2-5 seconds

*Times vary based on image complexity and number of paths*

---

## Memory Usage

Higher resolution images and more complex drawings require more memory:

- **Low complexity**: 500KB - 2MB image, few paths
  → Any method works fine

- **Medium complexity**: 2-5MB image, moderate detail
  → All methods work, skeleton mode slightly more memory

- **High complexity**: 5MB+ image, very detailed
  → Consider reducing resolution first
  → May need to increase system memory for spline fitting

**Tip:** If processing fails due to memory, resize image to 2000x2000 max before processing.
