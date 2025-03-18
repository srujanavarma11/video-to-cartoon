import os

from controller.image_processor.cartoon_convertor import cartoon_effect
from controller.image_processor.constants import BASE_DIR, EXTENSION
from controller.image_processor.images_to_video import generate_video
from controller.image_processor.video_to_images import splitor


def input_file(filename='test1.mp4'):
    only_filename = ''.join(filename.split('.')[:-1])
    
    input_path = os.path.join(BASE_DIR, 'storage', 'input', only_filename, filename)
    
    frames = os.path.join(BASE_DIR, 'storage', 'frames', only_filename)
    
    cartoon_img_path = os.path.join(BASE_DIR, 'storage', 'cartoon', only_filename)
    
    cartoon_video_path = os.path.join(BASE_DIR, 'storage', 'video', only_filename)
    
    
    required_dirs = [
        input_path,
        frames,
        cartoon_img_path,
        cartoon_video_path
    ]
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)

    
    number_of_frames = splitor(input_path, frames, only_filename)
    
    for current_frame in range(number_of_frames):
        image_path = os.path.join(frames, f"{only_filename}_{current_frame}{EXTENSION}")
        
        cartoon_path = os.path.join(cartoon_img_path, f"{only_filename}_{current_frame}{EXTENSION}")
        
        cartoon_effect(image_path, cartoon_path)
    
    generate_video(cartoon_img_path, cartoon_video_path, only_filename)
    
    
def upload_video_file(filename, file):
    only_extension = ''.join(file.filename.split('.')[-1])
    file_with_extension = f'{filename}.{only_extension}'
    print(only_extension)
    input_path = os.path.join(BASE_DIR, 'storage', 'input', filename)
    os.makedirs(input_path, exist_ok=True)
    file_path = os.path.join(input_path, file_with_extension)
    file.save(file_path)
    return file_with_extension
    
    