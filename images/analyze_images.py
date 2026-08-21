from PIL import Image
import numpy as np

def analyze_image(filepath, label):
    print(f"\n{'='*60}")
    print(f"ANALYZING: {label}")
    print(f"File: {filepath}")
    print(f"{'='*60}")
    
    img = Image.open(filepath)
    arr = np.array(img)
    print(f"  Image shape: {arr.shape}")
    print(f"  Image mode: {img.mode}")
    
    # Get unique colors
    pixels = arr.reshape(-1, arr.shape[2])
    unique_colors = np.unique(pixels, axis=0)
    print(f"  Total unique colors: {len(unique_colors)}")
    
    # Show colors that are not white/black/gray (potential important elements)
    print(f"  Non-white/black/gray colors:")
    for i, c in enumerate(unique_colors):
        r, g, b = c[0], c[1], c[2]
        # Skip near-white, near-black, and near-gray
        is_gray = abs(int(r) - int(g)) < 15 and abs(int(g) - int(b)) < 15 and abs(int(r) - int(b)) < 15
        if not is_gray:
            print(f"    Color {i}: RGB({r}, {g}, {b}) - {hex(r<<16|g<<8|b)}")
    
    # Check top portion for text/labels
    print(f"\n  Top-left corner (50x50) sampling:")
    for y in range(0, min(50, arr.shape[0]), 10):
        for x in range(0, min(50, arr.shape[1]), 10):
            r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
            if r < 200 or g < 200 or b < 200:  # Not near-white
                print(f"    Pixel at ({x},{y}): RGB({r},{g},{b})")
    
    return arr

# Analyze all 6 images
analyze_image(r"D:\ai_project_all\Terraform教程\images\phase3-vpc-architecture.png", "Phase 3 - VPC Architecture")
analyze_image(r"D:\ai_project_all\Terraform教程\images\phase5-ha-architecture.png", "Phase 5 - HA Architecture")
analyze_image(r"D:\ai_project_all\Terraform教程\images\phase7-production-architecture.png", "Phase 7 - Production Architecture")
analyze_image(r"D:\ai_project_all\Terraform教程\images\project1-single-web.png", "Project 1 - Single Web")
analyze_image(r"D:\ai_project_all\Terraform教程\images\project2-ha-web.png", "Project 2 - HA Web")
analyze_image(r"D:\ai_project_all\Terraform教程\images\project3-full-production.png", "Project 3 - Full Production")