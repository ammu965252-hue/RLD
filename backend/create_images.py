import os

# SVG content for sample image
sample_svg = '''<svg width="200" height="200" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="200" height="200" fill="#E8F5E8"/>
<path d="M100 20 Q120 40 100 80 Q80 120 100 160 Q140 140 160 100 Q140 60 100 20" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
<text x="100" y="180" font-family="Arial, sans-serif" font-size="12" fill="#666" text-anchor="middle">Sample Rice Leaf {i}</text>
</svg>'''

# SVG content for result image (with detection marks)
result_svg = '''<svg width="200" height="200" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="200" height="200" fill="#E8F5E8"/>
<path d="M100 20 Q120 40 100 80 Q80 120 100 160 Q140 140 160 100 Q140 60 100 20" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
<circle cx="120" cy="100" r="8" fill="#FF5722" opacity="0.7"/>
<circle cx="80" cy="120" r="6" fill="#FF5722" opacity="0.7"/>
<text x="100" y="180" font-family="Arial, sans-serif" font-size="12" fill="#666" text-anchor="middle">Detected Rice Leaf {i}</text>
</svg>'''

uploads_dir = 'uploads'
results_dir = os.path.join(uploads_dir, 'results')
os.makedirs(results_dir, exist_ok=True)

for i in range(1, 21):
    # Sample image
    with open(os.path.join(uploads_dir, f'sample_{i}.svg'), 'w') as f:
        f.write(sample_svg.replace('{i}', str(i)))
    
    # Result image
    with open(os.path.join(results_dir, f'result_sample_{i}.svg'), 'w') as f:
        f.write(result_svg.replace('{i}', str(i)))

print("Created 20 sample SVG images")