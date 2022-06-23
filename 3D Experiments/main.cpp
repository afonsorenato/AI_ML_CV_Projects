#include <iostream>
#include <opencv2/opencv.hpp>

using namespace cv;


int main()
{
    system("CLS");

    Mat image;
    image = imread("img1.png");

    if (!image.data){
        printf("No image data \n");
        return -1;
    }

    namedWindow("Display Image", WINDOW_AUTOSIZE);
    imshow("Display Iamge", image);
    waitKey(0);

    return 0;
}
