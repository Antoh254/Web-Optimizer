from flask import Flask, render_template, request, send_file
from PIL import Image
import io
import zipfile
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    if 'images' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist('images')
    max_width = int(request.form.get('width', 1200))
    quality = int(request.form.get('quality', 85))

    # Create a ZIP file in memory
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for file in files:
            if file.filename == '':
                continue
                
            try:
                # Open image from memory
                img = Image.open(file.stream)
                
                # 1. Resize logic
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                # 2. Save compressed image to memory buffer
                img_buffer = io.BytesIO()
                # Convert filename to .webp
                filename_base = os.path.splitext(file.filename)[0]
                new_filename = f"{filename_base}.webp"
                
                # Save as WebP
                img.save(img_buffer, "WEBP", quality=quality, optimize=True)
                
                # Add to ZIP
                zf.writestr(new_filename, img_buffer.getvalue())
            
            except Exception as e:
                print(f"Error processing {file.filename}: {e}")
                continue

    memory_file.seek(0)
    
    # Send the ZIP file to the user
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='optimized_images.zip'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)