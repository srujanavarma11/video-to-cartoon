import os

from controller.image_processor.constants import EXTENSION, FPS_TARGET
import cv2



def splitor(input_path, output_path, only_filename):
    print(f"Processing video: {input_path}")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    video = cv2.VideoCapture(input_path)
    
    # Get video properties
    original_fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
     # Calculate frame extraction interval
    # Example: if original_fps=30 and target_fps=10, we take every 3rd frame
    frame_interval = max(1, round(original_fps / FPS_TARGET))
    
    
    current_frame = 0
    saved_count = 0
    
    while True:
        ret, frame = video.read()
        
        if not ret:
            break
        
        if current_frame % frame_interval == 0:
            output_filename = os.path.join(output_path, f"{only_filename}_{saved_count}{EXTENSION}")
            
            cv2.imwrite(output_filename, frame)
            print(f"Saved: {output_filename}")
            
            saved_count += 1
            
        current_frame += 1
    
    print(f"Completed: Extracted {saved_count} frame")
    video.release()
    return saved_count



