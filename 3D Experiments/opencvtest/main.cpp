#include <iostream>
#include <stdio.h>
#include <opencv2\opencv.hpp>

using namespace cv;

int main(int, char**) {
    std::cout << "Hello, world!\n";

    Mat image;
    image = imread("Hello.jpg");

    namedWindow("Display Image", WINDOW_AUTOSIZE);
    imshow("Display Image", image);
    waitKey(0);

    return 0;

}
