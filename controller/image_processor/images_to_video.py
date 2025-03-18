import os
import cv2

from controller.image_processor.constants import OUTPUT_EXTENSION


def generate_video(input_path, output_path, filename):
    output_video_file_path = os.path.join(output_path, f'{filename}{OUTPUT_EXTENSION}')
    

    images = [img for img in os.listdir(input_path)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")] 


    frame = cv2.imread(os.path.join(input_path, images[0]))

    height, width, layers = frame.shape
    
    # There are multiple video format are supported but why only h264 is, 
    # the following stackoverflow gives you the answer 
    # https://stackoverflow.com/questions/30103077/what-is-the-codec-for-mp4-videos-in-python-opencv
    fourcc = cv2.VideoWriter_fourcc(*'h264')

    #0.1 so one image is 10 seconds
    video = cv2.VideoWriter(output_video_file_path, fourcc, 3, (width, height)) 

    for image in images:
        video.write(cv2.imread(os.path.join(input_path, image)))

    cv2.destroyAllWindows()
    video.release()
    

