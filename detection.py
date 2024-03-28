import cv2
import torch

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Define the video file path
video_path = 'C:/Users/Josh/Videos/purdue_airport_sunny.mkv'

# Open the video
cap = cv2.VideoCapture(video_path)

# Prepare the video writer to save output
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_no_label.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to the format expected by the model
    results = model(frame)

    # Iterate over the detections and draw a red bounding box for each
    for *xyxy, conf, cls in results.xyxy[0]:
        # Convert tensor to int
        x1, y1, x2, y2 = map(int, xyxy)
        # Draw the red bounding box on the frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red color and thin box

    # Write the frame with the custom drawn bounding boxes to output video
    out.write(frame)

    # Display the frame (optional, remove if not needed)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
