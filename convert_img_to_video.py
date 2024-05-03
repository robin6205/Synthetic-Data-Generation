import cv2
import os
import glob

def create_video_from_images(images, output_video_file, fps=24):
    # Ensure the images are in the correct order
    # images.sort(key=lambda x: int(x.split('\\')[-1].split('_')[1]))
    images.sort(key=lambda x: int(x.split('\\')[-1].split('_')[0]))
    
    # Use the first image to get the video dimensions
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can also use 'XVID' if you prefer
    out = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))
    
    # Loop through all images and write them to the video
    for image in images:
        frame = cv2.imread(image)
        out.write(frame)
    
    # Release everything when job is finished
    out.release()
    cv2.destroyAllWindows()

def filter_and_create_videos_for_cameras(image_folder, fps=10):
    # Gather all image filenames
    all_images = glob.glob(os.path.join(image_folder, '*.png'))
    
    # Filter images for each camera
    cam0_images = [img for img in all_images]
    cam1_images = [img for img in all_images if 'cam1_' in img]
    cam2_images = [img for img in all_images if 'cam2_' in img]
    cam3_images = [img for img in all_images if 'cam3_' in img]
    cam4_images = [img for img in all_images if 'cam4_' in img]
    
    # Output file names
    cam0_output_video_file = os.path.join(image_folder, 'cam0output.mp4')
    cam1_output_video_file = os.path.join(image_folder, 'cam1output.mp4')
    cam2_output_video_file = os.path.join(image_folder, 'cam2output.mp4')
    cam3_output_video_file = os.path.join(image_folder, 'cam3output.mp4')
    cam4_output_video_file = os.path.join(image_folder, 'cam4output.mp4')
    
    # Create video for cam1 images
    if cam1_images:
        print("Creating video for cam1 images...")
        create_video_from_images(cam1_images, cam1_output_video_file, fps)
    else:
        print("No images found for cam1.")
    
    # Create video for cam2 images
    if cam2_images:
        print("Creating video for cam2 images...")
        create_video_from_images(cam2_images, cam2_output_video_file, fps)
    else:
        print("No images found for cam2.")
        
    # Create video for cam3 images
    if cam3_images:
        print("Creating video for cam3 images...")
        create_video_from_images(cam3_images, cam3_output_video_file, fps)
    else:
        print("No images found for cam3.")
    
    # Create video for cam4 images
    if cam4_images:
        print("Creating video for cam4 images...")
        create_video_from_images(cam4_images, cam4_output_video_file, fps)
    else:
        print("No images found for cam4.")
        
    if cam0_images:
        print("Creating video for cam0 images...")
        create_video_from_images(cam0_images, cam0_output_video_file, fps)

# Specify the folder where your images are
image_folder = 'D:\\Unreal Projects\\camera_setup_env\\Saved\\UnrealGT\\UEDPIE_0_Purdue_airport4\\20240418T142658809Z\\GTFileStreamer'

# Call the function
filter_and_create_videos_for_cameras(image_folder)
