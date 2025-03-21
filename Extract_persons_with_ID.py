#!/usr/bin/env python3
"""
interactive_process_video.py

This script loads a YOLO model and processes a video by tracking objects every
N-th frame, cropping the detected objects, and saving them to an output directory.
It interactively asks for parameters via the command line.
 
Requirements:
    pip install ultralytics opencv-python
"""

import os
# Workaround for OpenMP duplicate runtime error
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
from ultralytics import YOLO

def main():
    print("=== YOLO Video Tracker and Cropper ===")
    
    # Get model path interactively.
    model_path = input("Enter the path to the YOLO model file (default: yolov8n-pose.pt): ").strip()
    if not model_path:
        model_path = "yolov8n-pose.pt"
    
    # Get video file path.
    video_path = input("Enter the video file path (default: example_data/example_video.mp4): ").strip()
    if not video_path:
        video_path = "example_data/example_video.mp4"
    
    # Get frame interval (e.g., process every N-th frame).
    frame_interval_input = input("Enter the frame interval (default: 30): ").strip()
    try:
        frame_interval = int(frame_interval_input) if frame_interval_input else 30
    except ValueError:
        print("Invalid input. Using default frame interval of 30.")
        frame_interval = 30

    # Get output directory.
    output_dir = input("Enter the output directory (default: output): ").strip()
    if not output_dir:
        output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the YOLO model.
    print(f"Loading model from '{model_path}'...")
    try:
        model = YOLO(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Open the video file.
    print(f"Opening video file '{video_path}'...")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return

    frame_count = 0
    print("Processing video... (press CTRL+C to abort)")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # End of video

            if frame_count % frame_interval == 0:
                print(f"Processing frame {frame_count}...")
                try:
                    # Use the model to track objects on the current frame.
                    results = model.track(frame, persist=True)
                    # Loop through detections in the first result.
                    for i, det in enumerate(results[0].boxes.xyxy):
                        # Extract bounding box coordinates.
                        x1, y1, x2, y2 = map(int, det[:4])
                        crop = frame[y1:y2, x1:x2]
                        # Save the cropped image with a unique name.
                        crop_name = f"frame_{frame_count}_id_{results[0].boxes.id[i]}.jpg"
                        crop_path = os.path.join(output_dir, crop_name)
                        cv2.imwrite(crop_path, crop)
                except Exception as e:
                    print(f"Error processing frame {frame_count}: {e}")

            frame_count += 1

    except KeyboardInterrupt:
        print("Processing interrupted by user.")

    except Exception as main_e:
        print("An error occurred during video processing:", main_e)

    finally:
        cap.release()
        print("Video processing complete. Output saved in:", output_dir)

if __name__ == '__main__':
    main()
