from flask import Flask, send_file, request, jsonify, send_from_directory
from flask_cors import CORS  # Импортируйте CORS
import os
from sources.predict import predict, addedPredict
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

RESOURCES_FOLDER = 'resources'
MODEL_PATH = "resources/models/yolov8/best.pt"
PREDICTION_FOLDER = os.path.join(RESOURCES_FOLDER, 'results', 'yolo_v8_predictions')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = YOLO(MODEL_PATH)



@app.route('/show-image')
def show_image():
    print("Showing image...")
    file_path = os.path.join(RESOURCES_FOLDER, 'output.jpg')
    return send_file(file_path, mimetype='image/jpeg')

@app.route('/results/<filename>')
def get_result(filename):
    print(f"Fetching result for: {filename}")
    return send_from_directory(PREDICTION_FOLDER, filename)


@app.route('/upload', methods=['POST'])
def upload_image():
    print("Received upload request")
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    y1 = request.form.get('y1')
    y2 = request.form.get('y2')

    roi = [int(x1), int(y1), int(x2), int(y2)] if all([x1, x2, y1, y2]) else None

    result_path = os.path.join(PREDICTION_FOLDER, f'predicted_{file.filename}')

    save_path, class_counts = addedPredict(file_path, result_path, model, printMode=0, roi=roi)
    print(f"Prediction saved to {save_path}")

    return jsonify({'result_image': f'/results/predicted_{file.filename}', 'class_counts': class_counts}), 200




if __name__ == '__main__':
    app.run(debug=True)






"""
@app.route('/upload', methods=['POST'])
def upload_image():
    print("Received upload request")
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print(f"File saved to {file_path}")

    result_path = os.path.join(PREDICTION_FOLDER, f'predicted_{file.filename}')
    
    predict(file_path, result_path, model)
    print(f"Prediction saved to {result_path}")

    return jsonify({'result_image': f'/results/predicted_{file.filename}'}), 200 
"""




"""
@app.route('/process-folder', methods=['POST'])
def process_folder():
    print("Starting folder processing...")
    folder_path = request.json.get('folderPath')
    print(f"Received folder path: {folder_path}")  # Добавьте этот лог
    save_folder_path = os.path.join(RESOURCES_FOLDER, 'results/test')

    if not folder_path or not os.path.isdir(folder_path):
        print("Invalid folder path:", folder_path)
        return jsonify({"error": "Invalid folder path"}), 400

    model = YOLO(MODEL_PATH)
    processed_files = []

    for filename in os.listdir(folder_path):
        print(f"Processing file: {filename}") 
        image_path = os.path.join(folder_path, filename)

        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            save_path = os.path.join(save_folder_path, f"{os.path.splitext(filename)[0]}_predict.jpg")
            try:
                predict(image_path, save_path, model)  
                processed_files.append(save_path)
                print(f"Processed file saved at: {save_path}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    print("Folder processing completed.")
    return jsonify({"message": "Processing completed", "files": processed_files}), 200
"""