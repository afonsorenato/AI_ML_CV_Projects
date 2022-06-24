# Some notes on Single Camera calibration

#### Renato Afonso - 2022 - Portugal

## Single camera calibration

#### Step 1: 
First define real world coordinates of 3D points using known size of checkerboard pattern.

#### Step 2: 
Different viewpoints of check-board image is captured.

#### Step 3: 
findChessboardCorners() is a method in OpenCV and used to find pixel coordinates (u, v) for each 3D point in different images

#### Step 4: 
Then calibrateCamera() method is used to find camera parameters.