# Some notes on Single Camera calibration

#### Renato Afonso - 2022 - Portugal

## Single camera calibration

1. First define real world coordinates of 3D points using known size of checkerboard pattern.

2. Different viewpoints of check-board image is captured.

3. findChessboardCorners() is a method in OpenCV and used to find pixel coordinates (u, v) for each 3D point in different images

4. Then calibrateCamera() method is used to find camera parameters.

## Camera distortions

**Radial distortion** makes straight lines curved. It is more visible the more we go away from the center of the image.

x_corrrected = x*(1 + k1*r^2 + k2*r^4 + k3*r^6)

y_corrrected = y*(1 + k1*r^2 + k2*r^4 + k3*r^6)

r = sqrt((xc-xd)^2 + (yc-yd)^2)

**Tangential distortion** occurs because image taking lense is not aligned perfectly parallel to the imaging plane. So some areas in image may look nearer than expected.

x_corrected = x + [2p1xy + p2(r^2 + 2c^2)]

y_corrected = y + ...




