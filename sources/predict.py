from ultralytics import YOLO
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
import os
import cv2



def addedPredict(imagePath, savePath, model, printMode=0, roi=None):
    image = cv2.imread(imagePath)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    if roi is not None:
        x1, y1, x2, y2 = roi
        region_of_interest = image_rgb[y1:y2, x1:x2]
        results = model.predict(source=region_of_interest, imgsz=640)
        cropped_save_path = savePath.replace(".jpg", "_cropped.jpg")
        cv2.imwrite(cropped_save_path, cv2.cvtColor(region_of_interest, cv2.COLOR_RGB2BGR))
    else: results = model.predict(source=image_rgb, imgsz=640)

    predicted_classes = results[0].boxes.cls.cpu().numpy() 
    class_counts = Counter(predicted_classes)
    class_counts = {int(key): int(value) for key, value in class_counts.items()}

    class_names = ['Bunker', 'Cargo', 'Cistern', 'ClassCarriage', 'Dumpcar',
                   'Fitting platorm', 'Halfcarriage', 'Laying crane', 'MTSO',
                   'PRSM Machine', 'Platform PPK', 'SMMachine', 'Sapsan', 'USOPlatform']
    if printMode: 
        for class_id, count in class_counts.items(): print(f"{class_names[int(class_id)]}:  {count}")

    test_image = results[0].plot(line_width=2)
    plt.imshow(test_image)
    results[0].save(savePath)
    
    if printMode == 1:
        plt.axis('off')
        plt.show()
    
    return cropped_save_path if roi else savePath, class_counts


def predict(imagePath, savePath, model, printMode=0):
    results = model.predict(source=imagePath, imgsz=640)
    results[0].plot(line_width=2)
    test_image = results[0].plot(line_width=2)
    results[0].save(savePath)
    if printMode==1:
        plt.imshow(test_image)
        plt.axis('off')
        plt.show()
    
    return savePath


def predictFolder(folderPath, saveFolderPath, model, printMode=0, logMode=0):
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    os.makedirs(saveFolderPath, exist_ok=True)
    cnt = 0

    for filename in os.listdir(folderPath):
        imagePath = os.path.join(folderPath, filename)
        
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            if logMode==1: print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            results = model.predict(source=imagePath, imgsz=640, verbose=bool(logMode))
            savePath = os.path.join(saveFolderPath, f"{os.path.splitext(filename)[0]}_predict.jpg")
            results[0].save(savePath)
            if printMode == 1:
                test_image = results[0].plot(line_width=2)
                plt.imshow(test_image)
                plt.axis('off')
                plt.show()
            cnt += 1

    print(f"{cnt} processing completed ", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    return savePath



def predictVideo(videoPath, savePath, model, printMode=0, logMode=0):
    if printMode: print("start    ", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    video_output = model.predict(source=videoPath, conf=0.6,save=True)
    if printMode: print("end     ", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    





# print("0    ", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
# model = YOLO("C:/Users/maxim/Desktop/pfo/resources/models/yolov8/best.pt")
# imagePath = 'C:/Users/maxim/Desktop/pfo/resources/yolov8/train/images/1_fixed_mp4-0005_jpg.rf.fbb81706e08ae705493e2737d9cc19e4.jpg'
# savePath = "C:/Users/maxim/Desktop/pfo/resources/results/img.jpg"
# folderPath = 'C:/Users/maxim/Desktop/pfo/resources/yolov8/train/images'
# saveFolderPath = "C:/Users/maxim/Desktop/pfo/resources/results/yolo_v8_predictions"
# videoPath = 'C:/Users/maxim/Desktop/pfo/resources/20241018115520848_72bb652cb6f742a99915c3e164fb76b5_AC1418956.mp4'
# 
# # print("1    ", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
# # predict(imagePath, savePath, model)
# # print("2    ", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
# # predictFolder(folderPath, saveFolderPath, model)
# # print("3    ", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
# predictVideo(videoPath, "C:/Users/maxim/Desktop/pfo/resources/results/yolo_v8_predictions/video", model)
# print("4    ", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))


