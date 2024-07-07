import cv2
import numpy as np
import glob

# Define the chessboard size (number of inner corners per a chessboard row and column)
chessboard_size = (9, 9)

# Define arrays to store object points and image points from all the images
obj_points = []  # 3d points in real world space
img_points = []  # 2d points in image plane

# Prepare object points
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# Load calibration images
images = glob.glob('ImageStream/*.png')

# Make sure we have at least one valid image
if not images:
    print("No calibration images found. Please check the path.")
    exit()

# Print the number of images found
print("Number of images found: ", len(images))

valid_detections = 0
image_size = None

for fname in images:
    # Print name of the file being processed
    print("Processing ", fname)
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCornersSB(gray, chessboard_size, None)

    if ret:
        valid_detections += 1
        # Print completion of chessboard corner detection for the image name
        print("Chessboard corners detected for ", fname)
        obj_points.append(objp.copy())
        img_points.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('Checkerboard', img)
        cv2.waitKey(100)  # Display each image for 500 milliseconds

        # Set the image size based on the first valid image
        if image_size is None:
            image_size = gray.shape[::-1]
    else:
        print("Chessboard corners not detected for ", fname)

cv2.destroyAllWindows()

print(f"Valid detections: {valid_detections} out of {len(images)} images")

# Ensure obj_points and img_points are numpy arrays
obj_points = [np.array(pts, dtype=np.float32) for pts in obj_points]
img_points = [np.array(pts, dtype=np.float32) for pts in img_points]

# Print the shapes and types to ensure correctness
print("obj_points shape:", np.shape(obj_points))
print("img_points shape:", [np.shape(pts) for pts in img_points])
print("image_size:", image_size)

# Define the initial camera matrix using F and C values
f_x = 640.0
f_y = 640.0
c_x = 640.0
c_y = 360.0

camera_matrix = np.array([[f_x, 0, c_x],
                          [0, f_y, c_y],
                          [0, 0, 1]], dtype=np.float32)

# Set the distortion coefficients to zero initially
dist_coeffs = np.zeros((5, 1), dtype=np.float32)

# Use the initial camera matrix and fix it during calibration
flags = cv2.CALIB_USE_INTRINSIC_GUESS 

# Perform camera calibration
# Make sure to pass the correct image size (width, height)

# log calibrateCamera function


if valid_detections > 0 and image_size is not None:
    print("Performing camera calibration...")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (int(image_size[0]), int(image_size[1])), camera_matrix, dist_coeffs, None)

    # Print the calibration result
    print("Camera matrix:\n", mtx)
    print("Distortion coefficients:\n", dist)

    # Save the calibration result
    np.savez('calibration_data.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
else:
    print("No valid chessboard detections found. Calibration not performed.")
