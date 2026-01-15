import io
import zipfile
import os
from PIL import Image
import jsmin
import cssmin

def process_images(files, max_width=1200, quality=85):
    """
    Processes a list of image files: resizes, converts to WebP, adds to Zip.
    Returns: io.BytesIO (the zip file in memory)
    """
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for file in files:
            # Handle both FileStorage objects (Flask) and open file objects (Desktop)
            filename = getattr(file, 'filename', None)
            if not filename:
                # Fallback for desktop app where file might be a path string or file-like
                if isinstance(file, str):
                    filename = os.path.basename(file)
                    file_content = open(file, 'rb')
                else:
                    filename = os.path.basename(file.name)
                    file_content = file
            else:
                file_content = file.stream

            if not filename:
                continue
                
            try:
                # Open image
                if isinstance(file_content, io.BytesIO) or hasattr(file_content, 'read'):
                    img = Image.open(file_content)
                else:
                     # Re-open if it was a file path that we opened above
                     # (Logic simplified: if it's a path, we opened it. If it's FileStorage, we use .stream)
                     pass 

                # 1. Resize logic
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                # 2. Save compressed image to memory buffer
                img_buffer = io.BytesIO()
                filename_base = os.path.splitext(filename)[0]
                new_filename = f"{filename_base}.webp"
                
                img.save(img_buffer, "WEBP", quality=quality, optimize=True)
                
                zf.writestr(new_filename, img_buffer.getvalue())
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

    memory_file.seek(0)
    return memory_file

def process_code(files):
    """
    Processes a list of code files: minifies CSS/JS, adds to Zip.
    Returns: io.BytesIO (the zip file in memory)
    """
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for file in files:
            filename = getattr(file, 'filename', None)
            if not filename:
                 if isinstance(file, str):
                    filename = os.path.basename(file)
                    # Read content directly from path
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except:
                        continue
                 else:
                    filename = os.path.basename(file.name)
                    content = file.read().decode('utf-8')
            else:
                # Flask FileStorage
                content = file.read().decode('utf-8')
                # Reset stream for safety if needed elsewhere (not needed here but good practice)
                file.stream.seek(0) 

            if not filename:
                continue
                
            try:
                ext = os.path.splitext(filename)[1].lower()
                minified_content = ""
                
                if ext == '.css':
                    minified_content = cssmin.cssmin(content)
                elif ext == '.js':
                    minified_content = jsmin.jsmin(content)
                else:
                    continue
                
                zf.writestr(filename, minified_content)
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

    memory_file.seek(0)
    return memory_file
