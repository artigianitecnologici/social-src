from flask import Flask, Response, render_template, send_from_directory ,request
import os
import io
import zipfile
import binascii
import argparse

app = Flask("Flask Image Gallery")
app.config['IMAGE_EXTS'] = [".png", ".jpg", ".jpeg", ".gif", ".tiff"]

def encode(x):
    return binascii.hexlify(x.encode('utf-8')).decode()

def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()


    
# Remove the staticmethod decorator
def download_gallery():
    Gallery_Folder = app.config['ROOT_DIR'] + '/images'
    gallery_name = os.path.basename(Gallery_Folder)

    if os.path.isdir(Gallery_Folder):
        fileobj = io.BytesIO()
        with zipfile.ZipFile(fileobj, 'w') as zip_file:
            for root, dirs, files in os.walk(Gallery_Folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Set arcname relative to the gallery_path
                    arcname = os.path.relpath(file_path, Gallery_Folder)
                    zip_file.write(file_path, arcname=arcname)

        fileobj.seek(0)

        return Response(fileobj.getvalue(),
                        mimetype='application/zip',
                        headers={'Content-Disposition': f'attachment;filename={gallery_name}.zip'})
    else:
        return "Gallery not found", 404

@app.route('/')
def home():
    root_dir = app.config['ROOT_DIR']
    image_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                image_paths.append(encode(os.path.join(root, file)))
    return render_template('index.html', paths=image_paths)

@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir, filename = os.path.split(decode(filepath))
    
    return send_from_directory(dir, filename, as_attachment=False)

@app.route('/download')
def download():
    return download_gallery()


@app.route('/delete-photo', methods=['DELETE'])
def delete_photo():
    try:
        path = decode(request.args.get('path'))
        full_path = path #os.path.join(app.config['UPLOAD_FOLDER'], path)
        print(full_path)
        # Check if the file exists before attempting to delete it
        if os.path.exists(full_path):
            os.remove(full_path)
            return "Photo deleted successfully", 200
        else:
            return "Photo not found", 404

    except Exception as e:
        print(f"Error deleting photo: {e}")
        return "Failed to delete photo", 500

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Usage: %prog [options]')
    parser.add_argument('root_dir', help='Gallery root directory path')
    parser.add_argument('-l', '--listen', dest='host', default='127.0.0.1',
                        help='address to listen on [127.0.0.1]')
    parser.add_argument('-p', '--port', metavar='PORT', dest='port', type=int,
                        default=8081, help='port to listen on [8081]')
    args = parser.parse_args()
    app.config['ROOT_DIR'] = args.root_dir
    app.run(host=args.host, port=args.port, debug=True)