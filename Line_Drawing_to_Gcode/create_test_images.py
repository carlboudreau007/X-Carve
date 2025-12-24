#!/usr/bin/env python3
"""
Test and demonstration script for skeleton mode
Creates sample images to show the difference between standard and skeleton processing
"""

import numpy as np
import cv2
from pathlib import Path

def create_test_image_clean_lines():
    """Create a test image with clean single-pixel lines"""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Draw some clean single-pixel lines
    cv2.line(img, (50, 50), (550, 50), (0, 0, 0), 1)
    cv2.line(img, (50, 50), (50, 350), (0, 0, 0), 1)
    cv2.line(img, (50, 350), (550, 350), (0, 0, 0), 1)
    cv2.line(img, (550, 50), (550, 350), (0, 0, 0), 1)
    
    # Circle
    cv2.circle(img, (300, 200), 80, (0, 0, 0), 1)
    
    return img

def create_test_image_thick_lines():
    """Create a test image with thick, variable width lines (like pencil)"""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Draw some thick lines with variable width
    # Rectangle with thick lines
    cv2.line(img, (50, 50), (550, 50), (0, 0, 0), 8)
    cv2.line(img, (50, 50), (50, 350), (0, 0, 0), 8)
    cv2.line(img, (50, 350), (550, 350), (0, 0, 0), 8)
    cv2.line(img, (550, 50), (550, 350), (0, 0, 0), 8)
    
    # Circle with varying thickness
    for i in range(0, 360, 15):
        thickness = 5 + int(3 * np.sin(i * np.pi / 180))
        angle1 = i * np.pi / 180
        angle2 = (i + 15) * np.pi / 180
        pt1 = (int(300 + 80 * np.cos(angle1)), int(200 + 80 * np.sin(angle1)))
        pt2 = (int(300 + 80 * np.cos(angle2)), int(200 + 80 * np.sin(angle2)))
        cv2.line(img, pt1, pt2, (0, 0, 0), thickness)
    
    # Add a freehand-looking curve
    points = []
    for x in range(100, 500, 10):
        y = 250 + int(30 * np.sin((x - 100) * 0.02))
        points.append([x, y])
    
    points = np.array(points, dtype=np.int32)
    # Draw with varying thickness
    for i in range(len(points) - 1):
        thickness = 4 + int(2 * np.sin(i * 0.3))
        cv2.line(img, tuple(points[i]), tuple(points[i+1]), (0, 0, 0), thickness)
    
    return img

def create_test_image_sketch():
    """Create a test image simulating a rough pencil sketch"""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Add some texture/noise to simulate paper
    noise = np.random.randint(240, 256, (400, 600, 3), dtype=np.uint8)
    img = cv2.addWeighted(img, 0.7, noise, 0.3, 0)
    
    # Draw irregular lines with varying pressure (thickness and intensity)
    def draw_sketchy_line(img, pt1, pt2, base_thickness=6):
        """Draw a line with irregular thickness and intensity"""
        x1, y1 = pt1
        x2, y2 = pt2
        steps = int(np.sqrt((x2-x1)**2 + (y2-y1)**2) / 5)
        
        for i in range(steps):
            t = i / steps
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            
            # Add randomness
            x += np.random.randint(-2, 3)
            y += np.random.randint(-2, 3)
            
            # Vary thickness and intensity
            thickness = base_thickness + np.random.randint(-2, 3)
            intensity = np.random.randint(0, 50)
            
            cv2.circle(img, (x, y), thickness // 2, (intensity, intensity, intensity), -1)
    
    # Draw a rough rectangle
    draw_sketchy_line(img, (50, 50), (550, 50))
    draw_sketchy_line(img, (50, 50), (50, 350))
    draw_sketchy_line(img, (50, 350), (550, 350))
    draw_sketchy_line(img, (550, 50), (550, 350))
    
    # Draw a rough circle
    for angle in range(0, 360, 5):
        angle_rad = angle * np.pi / 180
        next_rad = (angle + 5) * np.pi / 180
        pt1 = (int(300 + 80 * np.cos(angle_rad)), int(200 + 80 * np.sin(angle_rad)))
        pt2 = (int(300 + 80 * np.cos(next_rad)), int(200 + 80 * np.sin(next_rad)))
        draw_sketchy_line(img, pt1, pt2, base_thickness=5)
    
    # Draw a wavy line
    for x in range(100, 500, 8):
        y = 250 + int(30 * np.sin((x - 100) * 0.02))
        next_x = x + 8
        next_y = 250 + int(30 * np.sin((next_x - 100) * 0.02))
        draw_sketchy_line(img, (x, y), (next_x, next_y), base_thickness=4)
    
    return img

def main():
    """Generate test images"""
    output_dir = Path("/mnt/user-data/outputs")
    output_dir.mkdir(exist_ok=True)
    
    print("Generating test images...")
    
    # Create test images
    img_clean = create_test_image_clean_lines()
    img_thick = create_test_image_thick_lines()
    img_sketch = create_test_image_sketch()
    
    # Save images
    cv2.imwrite(str(output_dir / "test_clean_lines.png"), img_clean)
    cv2.imwrite(str(output_dir / "test_thick_lines.png"), img_thick)
    cv2.imwrite(str(output_dir / "test_pencil_sketch.png"), img_sketch)
    
    print("\nTest images created:")
    print("  - test_clean_lines.png (use standard mode)")
    print("  - test_thick_lines.png (use --skeleton)")
    print("  - test_pencil_sketch.png (use --skeleton --smooth 10)")
    
    print("\nTest commands:")
    print("\n# Standard mode for clean lines:")
    print("python line_to_gcode.py test_clean_lines.png")
    
    print("\n# Skeleton mode for thick lines:")
    print("python line_to_gcode.py test_thick_lines.png --skeleton")
    
    print("\n# Skeleton + smoothing for sketches:")
    print("python line_to_gcode.py test_pencil_sketch.png --skeleton --smooth 10")
    
    print("\n# Skeleton + spline for very smooth curves:")
    print("python line_to_gcode.py test_pencil_sketch.png --skeleton --smooth 8 --spline")

if __name__ == '__main__':
    main()
