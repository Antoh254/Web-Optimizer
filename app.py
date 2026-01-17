from flask import Flask, render_template, request, send_file, send_from_directory
import os
import utils

app = Flask(__name__)

# Ensure download folder exists
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    if 'images' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist('images')
    max_width = int(request.form.get('width', 1200))
    quality = int(request.form.get('quality', 85))

    memory_file = utils.process_images(files, max_width, quality)
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='optimized_images.zip'
    )

@app.route('/minify', methods=['POST'])
def minify():
    if 'files' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist('files')
    
    memory_file = utils.process_code(files)
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='minified_code.zip'
    )

@app.route('/download/linux')
def download_linux():
    try:
        return send_from_directory(DOWNLOAD_FOLDER, 'WebOptimizer_Linux', as_attachment=True)
    except FileNotFoundError:
        return "File not found. Please build the app first.", 404

@app.route('/download/windows')
def download_windows():
    try:
        return send_from_directory(DOWNLOAD_FOLDER, 'WebOptimizr.exe', as_attachment=True)
    except FileNotFoundError:
        return "File not found. Please build the app first.", 404

@app.route('/sitemap.xml')
def sitemap():
    return render_template('sitemap.xml')

@app.route('/robots.txt')
def robots():
    return render_template('robots.txt')

if __name__ == '__main__':
    app.run(debug=True, port=5000)