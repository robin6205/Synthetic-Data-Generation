from __future__ import division, absolute_import, print_function
from unrealcv import Client
from PIL import Image
import io
import matplotlib.pyplot as plt
import sys
import os
import time
import numpy as np
from io import BytesIO, StringIO
from datetime import datetime


def imread8(im_file):
    ''' Read image as an 8-bit numpy array '''
    im = np.asarray(Image.open(im_file))
    return im

def read_png(res):
    print('reading png')
    img = Image.open(io.BytesIO(res))
    return np.asarray(img)

def read_npy(res):
    return np.load(io.BytesIO(res))

def normalize_normal_map(normal_map):
    # Normalize the normal map values to the range [0, 1]
    norm_map = (normal_map / 255.0) * 2 - 1  # Map to [-1, 1]
    return (norm_map + 1) / 2  # Map to [0, 1] for display

def save_image(image_data, folder='data'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f'rgb_{timestamp}.png')
    img = Image.open(io.BytesIO(image_data))
    img.save(filename)
    print(f'Saved {filename}')
    
def normalize_depth(depth, clip_min=0, clip_max=500):
    # Clip depth values to avoid extreme outliers
    depth = np.clip(depth, clip_min, clip_max)
    depth_min = np.min(depth)
    depth_max = np.max(depth)
    return (depth - depth_min) / (depth_max - depth_min)

# Initialize client
client = Client(('localhost', 9000))

try:
    client.connect()

    # Check if connected
    if not client.isconnected():
        print('UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.')
        sys.exit(-1)
    # Spawn a new camera
    client.request('vset /objects/spawn FusionCameraActor Cam1')
    # The actual id counts up from 1
    time.sleep(1)  # Give some time for the camera to be spawned
    # Set camera location and orientation
    location_command = 'vset /camera/1/location 0 0 100'
    rotation_command = 'vset /camera/1/rotation 0 250 0.000000'
    client.request(location_command)
    client.request(rotation_command)
    
    # Get status
    res = client.request('vget /unrealcv/status')
    print(res)
    
    # get uclass name vget /object/[obj_name]/uclass_name
    res = client.request('vget /object/1/uclass_name')
    print(res)
    
    # Get image
    res = client.request('vget /camera/1/lit png')
    im = read_png(res)
    print('RGB image shape:', im.shape)
    # Get image
    
    res = client.request('vget /camera/1/object_mask png')
    object_mask = read_png(res)
    # print(object_mask)
    # plt.imshow(object_mask)
    # plt.axis('off')  # Hide axes
    # plt.show()
    
    # Get normals
    # res = client.request('vget /camera/1/normal png')
    # normal_img = read_png(res)
    # print(normal_img)
    # normalized_normal_img = normalize_normal_map(normal_img)
    # plt.imshow(normalized_normal_img)
    # plt.axis('off')  # Hide axes
    # plt.show()
    
    # Get depth
    res = client.request('vget /camera/1/depth npy')
    depth = read_npy(res)
    print(depth)

    # Normalize depth values for visualization
    normalized_depth = normalize_depth(depth, clip_min=0, clip_max=2000)

    # Visualize the depth map
    plt.imshow(normalized_depth, cmap='viridis')
    plt.colorbar(label='Normalized Depth')
    plt.axis('off')
    plt.title('Depth Map')
    plt.show()
    
    
    # Capture images for 30 seconds at 30 FPS
    fps = 30
    duration = 30
    start_time = time.time()

    while time.time() - start_time < duration:
        res = client.request('vget /camera/1/lit png')
        
        if isinstance(res, str):
            print('Received string response instead of bytes:', res)
        else:
            save_image(res)
        
        time.sleep(1 / fps)

    # Get image
    # Get status
 

    # # Get normals
    # res = client.request('vget /camera/0/normal png')
    # normal_img = read_png(res)
    # print('Normal image shape:', normal_img.shape)
    # normalized_normal_img = normalize_normal_map(normal_img)
    
    # # Get object mask
    # res = client.request('vget /camera/0/object_mask png')
    # mask_img = read_png(res)
    # print('Object mask image shape:', mask_img.shape)


    # Visualize the image we just captured
    # plt.imshow(im)
    # plt.axis('off')  # Hide axes
    # plt.show()
    
    # res = client.request('vget /camera/0/object_mask png')
    # object_mask = read_png(res)
    # res = client.request('vget /camera/0/normal png')
    # normal = read_png(res)

    # # Visualize the captured ground truth
    # plt.imshow(object_mask)
    # plt.axis('off')  # Hide axes
    # plt.show()
    # plt.figure()
    # plt.imshow(normal)
    # plt.axis('off')  # Hide axes
    # plt.show()

except KeyboardInterrupt:
    print("Interrupted by user")

except Exception as e:
    print(e)

finally:
    # Ensure proper cleanup and termination
    client.disconnect()
    print("Client disconnected")
    sys.exit(0)
