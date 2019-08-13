#include <opencv2/opencv.hpp>
#define CVUI_IMPLEMENTATION
#include "cvui.h"
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string>
#include <stdio.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <math.h>
#include <random>
#include <GeographicLib/Geocentric.hpp>
#include <GeographicLib/LocalCartesian.hpp>
#include <GeographicLib/GeoCoords.hpp>

#define WINDOW1_NAME "CVUI1"
#define WINDOW2_NAME "CVUI2"
#define WINDOW3_NAME "CVUI3"

#define MAGNIFICATION 2.2
#define SIGMA 0
#define W1_HEIGHT 493
#define W1_WIDTH 500
#define W2_HEIGHT 500
#define W2_WIDTH 500
#define W3_HEIGHT 500
#define W3_WIDTH 500

#define W1_POS_X 0
#define W1_POS_Y 0
#define W2_POS_X 500
#define W2_POS_Y 0
#define W3_POS_X 0
#define W3_POS_Y 550

#define NICE_COLOR 49, 52, 49

#define MARGIN 10
#define OFFSETX 0
#define OFFSETY 0

using namespace std;

static void help() {
    std::cout
        << "\n------------------------------------------------------------------\n"
        //TODO description - colorizer ?
        << " UI colorizer for 3D points of traffic signs\n"
        << " \n"
        << " Usage:\n"
        << "        ./colorizer <path_to_input_CSV> <path_to_folder_of_images> <path_to_output_CSV> <path_to_csv_file_containing_sign_bounding_box\n"
        << " Example:\n"
        << "        ./colorizer data/signs/signs.csv data/images/ data/signs_colorized/signsColorized.csv data/sign_bbox/test.csv\n"
        << " \n"
        << "------------------------------------------------------------------\n\n"
        << std::endl;
}

struct PointCld
{
    int signId;
    int id;
    double x;
    double y;
    double z;
    double retro;
    double utc;
    double angle;
    double dist;
    bool fromLas;
    int color[3];
    double px;
    double py;
};

class FrameOfImage
{
    private:
        std::string pathToImage;
        cv::Mat frame;
        cv::Mat img;
        cv::Mat imgBlur;
        cv::Mat imgDraw;
        cv::Mat imgCropped;
        cv::Mat imgResized;
        cv::Rect zoomRect;
        cv::Rect tmpZoomRect;
        int height;
        int width;
        float magnification;
        cv::Point ptA;
        cv::Point ptB;
        cv::Point ptC;
        cv::Point ptD;
        char lastPt;
        int margin;
        float gSigma; // Gaussian kernel size

        // Correct the perspective
        cv::Mat homography, imgWarped;
        std::vector<cv::Point2f> pts_src;
        std::vector<cv::Point2f> pts_dst;


    public:
        FrameOfImage()
        {
            height = 400;
            width = 400;
            magnification = 1;
            gSigma = 0;
            // set the zoom to the whole image
            zoomRect.x = 0;
            zoomRect.y = 0;
            zoomRect.width = width;
            zoomRect.height = height;
            // reset the selection of points
            ptA = cv::Point(-1,-1);
            ptB = cv::Point(-1,-1);
            ptC = cv::Point(-1,-1);
            ptD = cv::Point(-1,-1);
            lastPt = '0';
            pts_dst.push_back(cv::Point2f(250, margin));
            pts_dst.push_back(cv::Point2f(500-margin, 250));
            pts_dst.push_back(cv::Point2f(250, 500-margin));
            pts_dst.push_back(cv::Point2f(margin, 250));
        }

        FrameOfImage(std::string inputFolder_,string signCSV, int signNumber_, float magnification_, int margin_)
        {

        	std::ifstream infile(signCSV.c_str());
			string cell, line;
 			stringstream line_ss;
            frame = cv::Mat(300, 300, CV_8UC3, cv::Scalar(49, 52, 49));

            // reset the selection of points
            ptA = cv::Point(-1,-1);
            ptB = cv::Point(-1,-1);
            ptC = cv::Point(-1,-1);
            ptD = cv::Point(-1,-1);

 			lastPt = '0';
 			int org_image_height;
           	int org_image_width;
           	int x1=-1;
           	int x2=-1;
           	int y1=-1;
           	int y2=-1;

        	//std::ifstream infile(sign_image_csv_.c_str());
			//string cell, line;
	 			//stringstream line_ss;

        	if (signCSV!=""){
		    	int k = 0 ;
		    	for(k=0; getline(infile, line); k++)
		    	{
					if(k==signNumber_) // ignore csv header
					{
						cout<<"In";
						line_ss.str(line);
						for (int i=0; getline(line_ss, cell, ','); i++){
		  					if (i==1) x1=stod(cell);
		  					if (i==2) y1=stod(cell);
		  					if (i==3) x2=stod(cell);
		  					if (i==4) y2=stod(cell);
		  					if (i==8) org_image_width=stod(cell);
		  					if (i==9) org_image_height=stod(cell);

	  					}
					ptA.x = int((x1+x2)/2);
					ptA.y = y1;
					ptB.x = x2;
					ptB.y = int((y1+y2)/2);
					ptC.x = int((x1+x2)/2);
					ptC.y = y2;
					ptD.x = x1;
					ptD.y = int((y1+y2)/2);
					warpPerspective();
					lastPt = 'D';
					break;
					}
				}
            }

            // read image containing the sign
            pathToImage = inputFolder_ + std::to_string(signNumber_)+".jpg";
            img = cv::imread(pathToImage.c_str());

            if(img.data)
            {
                height = img.rows;
                width = img.cols;
       	        cout<<"Height width \n";
                cout<<height;
            	cout<<width;
            }
            else
            {
                height = 400;
                width = 500;
            }

            ptA.x *= float(width)/org_image_width;
			ptA.y *= float(height)/org_image_height;
			ptB.x *= float(width)/org_image_width;
			ptB.y *= float(height)/org_image_height;
			ptC.x *= float(width)/org_image_width;
			ptC.y *= float(height)/org_image_height;
			ptD.x *= float(width)/org_image_width;
			ptD.y *= float(height)/org_image_height;

			cout<<ptA.x<<","<<ptA.y<<"\n";
			cout<<ptB.x<<","<<ptB.y<<"\n";
			cout<<ptC.x<<","<<ptC.y<<"\n";
			cout<<ptD.x<<","<<ptD.y<<"\n";

            // set the zoom to the whole image
            zoomRect.x = 0;
            zoomRect.y = 0;
            zoomRect.width = width;
            zoomRect.height = height;
            magnification = magnification_;
            margin = margin_;
            // set the points destination for homography
            pts_dst.push_back(cv::Point2f(250, margin));
            pts_dst.push_back(cv::Point2f(500-margin, 250));
            pts_dst.push_back(cv::Point2f(250, 500-margin));
            pts_dst.push_back(cv::Point2f(margin, 250));
            // update the frame
            update();
        }

        void update()
        {
            if(img.data)
            {
                // Apply gaussian blur to the img
                if(gSigma>0)
                {
                    GaussianBlur( img, imgBlur, cv::Size( 0 , 0 ), gSigma, gSigma );
                }
                else
                {
                    imgBlur = img.clone();
                }
                // Draw the defined points on imgDraw
                imgDraw = imgBlur.clone();
                if(ptA.x != -1) circle(imgDraw, ptA, 5, cv::Scalar(0,255,0), CV_FILLED, 3, 0);
                if(ptB.x != -1) circle(imgDraw, ptB, 5, cv::Scalar(0,255,0), CV_FILLED, 3, 0);
                if(ptC.x != -1) circle(imgDraw, ptC, 5, cv::Scalar(0,255,0), CV_FILLED, 3, 0);
                if(ptD.x != -1) circle(imgDraw, ptD, 5, cv::Scalar(0,255,0), CV_FILLED, 3, 0);
                // Get the selected part of the image (zoom)
                imgCropped = imgDraw(zoomRect);
                // render the zoom rectangle if there is any
                if(zoomSelection())
                {
                    cvui::rect(imgDraw, tmpZoomRect.x, tmpZoomRect.y, tmpZoomRect.width, tmpZoomRect.height, 0x00ff00);
                }
                // resize the image and render it
                resize(imgCropped, imgResized, cv::Size(width/magnification, height/magnification));
                resize(frame, frame, cv::Size(width/magnification, height/magnification));
                cvui::image(frame,0,0,imgResized);
            }
            else
            {
                frame = cv::Mat(height, width, CV_8UC3, cv::Scalar(49, 52, 49));
                cvui::printf(frame, 30, 30, 0.5, 0xffff, "No image to display!");
            }
        }

        void resetZoom()
        {
            zoomRect.x = 0;
            zoomRect.y = 0;
            zoomRect.width = width;
            zoomRect.height = height;
            update();
        }

        void resetPoints()
        {
            ptA = cv::Point(-1,-1);
            ptB = cv::Point(-1,-1);
            ptC = cv::Point(-1,-1);
            ptD = cv::Point(-1,-1);
            lastPt = '0';
            update();
        }

        void undoLastPoint()
        {
            switch(lastPt)
            {
                case 'A':
                    ptA = cv::Point(-1,-1);
                    lastPt = '0';
                    break;
                case 'B':
                    ptB = cv::Point(-1,-1);
                    lastPt = 'A';
                    break;
                case 'C':
                    ptC = cv::Point(-1,-1);
                    lastPt = 'B';
                    break;
                case 'D':
                    ptD = cv::Point(-1,-1);
                    lastPt = 'C';
                    break;
            }
            update();
        }

        int warpPerspective(int height_, int width_)
        {
            if((lastPt=='D')&&(img.data))
            {
                pts_src.clear();
                pts_src.push_back(ptA);
                pts_src.push_back(ptB);
                pts_src.push_back(ptC);
                pts_src.push_back(ptD);
                homography = cv::findHomography(pts_src, pts_dst);
                cv::warpPerspective(imgBlur, imgWarped, homography, cv::Size(height_, width_));
                return 1;
            }
            else
            {
                return 0;
            }
        }

        void mouseDown(cv::Point cursor_)
        {
            cv::Point pixel = cursor_*magnification;
            cv::Point point = cv::Point(zoomRect.x + pixel.x*zoomRect.width/width, zoomRect.y + pixel.y*zoomRect.height/height);
            tmpZoomRect.x = point.x;
            tmpZoomRect.y = point.y;
        }

        void mouseIsDown(cv::Point cursor_)
        {
            cv::Point pixel = cursor_*magnification;
            cv::Point point = cv::Point(zoomRect.x + pixel.x*zoomRect.width/width, zoomRect.y + pixel.y*zoomRect.height/height);
            tmpZoomRect.width = point.x - tmpZoomRect.x;
            tmpZoomRect.height = point.y - tmpZoomRect.y;
            update();
        }

        void mouseUp()
        {
            if((tmpZoomRect.width!=0)&&(tmpZoomRect.height!=0))
            {
                if((tmpZoomRect.width>0)&&(tmpZoomRect.height>0))
                {
                    bool insideImage = ((tmpZoomRect.x + tmpZoomRect.width)<width)
                                        &&((tmpZoomRect.y + tmpZoomRect.height)<height);
                    if(insideImage)
                    {
                        zoomRect = tmpZoomRect;
                    }
                }
                else if((tmpZoomRect.width<0)&&(tmpZoomRect.height>0))
                {
                    zoomRect.y = tmpZoomRect.y;
                    zoomRect.width = -tmpZoomRect.width;
                    if((tmpZoomRect.y + tmpZoomRect.height)<height)
                    {
                        zoomRect.height = tmpZoomRect.height;
                    }
                    else
                    {
                        zoomRect.height = height - tmpZoomRect.y;
                    }

                    if(tmpZoomRect.x + tmpZoomRect.width>= 0)
                    {
                        zoomRect.x = tmpZoomRect.x + tmpZoomRect.width;
                    }
                    else
                    {
                        zoomRect.x = 0;
                    }
                }
                else if((tmpZoomRect.width>0)&&(tmpZoomRect.height<0))
                {
                    zoomRect.x = tmpZoomRect.x;
                    zoomRect.height = -tmpZoomRect.height;
                    if((tmpZoomRect.x + tmpZoomRect.width)<width)
                    {
                        zoomRect.width = tmpZoomRect.width;
                    }
                    else
                    {
                        zoomRect.width = width - tmpZoomRect.x;
                    }

                    if(tmpZoomRect.y + tmpZoomRect.height>= 0)
                    {
                        zoomRect.y = tmpZoomRect.y + tmpZoomRect.height;
                    }
                    else
                    {
                        zoomRect.y = 0;
                    }
                }
                else if((tmpZoomRect.width<0)&&(tmpZoomRect.height<0))
                {
                    if((tmpZoomRect.x + tmpZoomRect.width) >= 0)
                    {
                        zoomRect.x = tmpZoomRect.x + tmpZoomRect.width;
                    }
                    else
                    {
                        zoomRect.x = 0;
                    }

                    if((tmpZoomRect.y + tmpZoomRect.height) >= 0)
                    {
                        zoomRect.y = tmpZoomRect.y + tmpZoomRect.height;
                    }
                    else
                    {
                        zoomRect.y = 0;
                    }
                    zoomRect.width = -tmpZoomRect.width;
                    zoomRect.height = -tmpZoomRect.height;
                }
            }

            // reset tmpZoomRect and update
            tmpZoomRect.x = 0;
            tmpZoomRect.y = 0;
            tmpZoomRect.width = 0;
            tmpZoomRect.height = 0;
            update();
        }

        bool zoomSelection()
        {
            if((tmpZoomRect.width!=0)&&(tmpZoomRect.height!=0))
            {
                return true;
            }
            else
            {
                return false;}
        }

        // Getters
        cv::Mat getFrame()
        {
            return frame;
        }

        cv::Point getPtA()
        {
            return ptA;
        }

        cv::Point getPtB()
        {
            return ptB;
        }

        cv::Point getPtC()
        {
            return ptC;
        }

        cv::Point getPtD()
        {
            return ptD;
        }

        char getLastPt()
        {
            return lastPt;
        }

        float getMagnification()
        {
            return magnification;
        }

        float getGBlurSigma()
        {
            return gSigma;
        }

        cv::Mat getImgWarped()
        {
            return imgWarped;
        }

        // Setters

        void setPoint(cv::Point cursor_)
        {
            cv::Point pixel = cursor_*magnification;
            cv::Point point = cv::Point(zoomRect.x + pixel.x*zoomRect.width/width, zoomRect.y + pixel.y*zoomRect.height/height);
            if(lastPt == 'C')
            {
                ptD = point;
                lastPt = 'D';
            }
            if(lastPt == 'B')
            {
                ptC = point;
                lastPt = 'C';
            }
            if(lastPt == 'A')
            {
                ptB = point;
                lastPt = 'B';
            }
            if(lastPt == '0')
            {
                ptA = point;
                lastPt = 'A';
            }
            update();
        }

        void setZoom(cv::Rect rect_)
        {
            zoomRect = rect_;
        }

        void setPtA(cv::Point ptA_)
        {
            ptA = ptA_;
            lastPt = 'A';
            update();
        }

        void setPtB(cv::Point ptB_)
        {
            ptB = ptB_;
            lastPt = 'B';
            update();
        }

        void setPtC(cv::Point ptC_)
        {
            ptC = ptC_;
            lastPt = 'C';
            update();
        }

        void setPtD(cv::Point ptD_)
        {
            ptD = ptD_;
            lastPt = 'D';
            update();
        }

        void setMagnification(float magnification_)
        {
            magnification = magnification_;
            update();
        }

        void setGBlurSigma (float gSigma_)
        {
            gSigma = gSigma_;
            update();
        }

};

class FrameOfSign
{
    private:
        cv::Mat frame;
        cv::Mat imgWarped;
        cv::Mat imgPoints;
        cv::Mat imgColorPoints;
        int width;
        int height;
        int margin;
        int offsetX;
        int offsetY;
        std::vector<PointCld> points;
        bool areColorised;
        bool showColorisedPoints;
        bool isWarped;
    public:
        // FrameOfSign();
        // FrameOfSign(int height_, int width_, int margin_, int offsetX_, int offsetY_);
        // void update();
        // cv::Mat getFrame();
        // void setImgWarped(cv::Mat& imgWarped_);
        // void init(std::vector<PointCld>& points_);
        // void setPoints(std::vector<PointCld>& points_);
        // std::vector<PointCld> getPoints();
        // void setOffsetX(int offsetX_);
        // void setOffsetY(int offsetY_);
        // void setOffset(int offsetX_ , int offsetY_);
        // void setMargin(int margin_);
        // int getOffsetX();
        // int getOffsetY();
        // int getMargin();
        // void setShowColorisedPoints (bool showColorisedPoints_);
        // void colorisePoints();
        // void drawColorisedPoints();
        // void drawPoints();
        // bool areColorised();


        FrameOfSign()
        {
            width = 500;
            height = 500;
            frame = cv::Mat(height, width, CV_8UC3, cv::Scalar(49, 52, 49));
            imgWarped = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            imgPoints = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            imgColorPoints = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            margin = 0;
            offsetX = 0;
            offsetY = 0;
            areColorised = false;
            showColorisedPoints = false;
            isWarped = false;
        }

        FrameOfSign(int height_, int width_, int margin_, int offsetX_, int offsetY_)
        {
            height = height_;
            width = width_;
            frame = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            imgWarped = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            imgPoints = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            imgColorPoints = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            margin = margin_;
            offsetX = offsetX_;
            offsetY = offsetY_;
            isWarped = false;
            areColorised = false;
            showColorisedPoints = false;
        }

        bool arePointsColorized()
        {
            return areColorised;
        }

        void update()
        {
            if(isWarped)
            {
                if(showColorisedPoints)
                {
                    colorisePoints();
                    drawColorisedPoints();
                    cvui::image(frame,0,0,imgColorPoints);
                }
                else
                {
                    drawPoints();
                    cvui::image(frame,0,0,imgPoints);
                }
            }
            else
            {
                drawPoints();
                cvui::image(frame,0,0,imgPoints);
            }
        }

        cv::Mat getFrame()
        {
            return frame;
        }

        void init(std::vector<PointCld>& points_, int margin_, int offsetX_, int offsetY_)
        {
            frame = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            imgWarped = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            imgPoints = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            imgColorPoints = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            margin = margin_;
            offsetX = offsetX_;
            offsetY = offsetY_;
            isWarped = false;
            areColorised = false;
            showColorisedPoints = false;
            points = points_;
            update();
        }

        void setPoints(std::vector<PointCld>& points_)
        {
            points = points_;
            update();
        }

        std::vector<PointCld> getPoints()
        {
            return points;
        }

        void setImgWarped(cv::Mat imgWarped_)
        {
            imgWarped = imgWarped_.clone();
            isWarped = true;
            update();
        }

        void setOffsetX(int offsetX_)
        {
            offsetX = offsetX_;
            update();
        }

        void setOffsetY(int offsetY_)
        {
            offsetY = offsetY_;
            update();
        }

        void setOffset(int offsetX_ , int offsetY_)
        {
            offsetX = offsetX_;
            offsetY = offsetY_;
            update();
        }

        void setMargin(int margin_)
        {
            margin = margin_;
            update();
        }

        int getOffsetX()
        {
            return offsetX;
        }

        int getOffsetY()
        {
            return offsetY;
        }

        int getMargin()
        {
            return margin;
        }

        void setShowColorisedPoints (bool showColorisedPoints_)
        {
            showColorisedPoints = showColorisedPoints_;
            update();
        }

        void colorisePoints()
        {
            // check if there is a warped image
            if(isWarped)
            {
                cv::Vec3b intensity;
                int X, Y;

                for(int i=0; i<points.size(); i++)
                {
                    // Compute the position of the projected points[i] on the warped image
                    X = (int) (offsetX + margin + points[i].px*(width-2*margin));
                    Y = (int) (offsetY + margin + points[i].py*(height-2*margin));

                    // Check if the point (X,Y) is inside the warped image
                    if((0<=X)&&(X<=width)&&(0<=Y)&&(Y<=height))
                    {
                        // Get the color (BGR) from the warped image at the position (X,Y)
                        intensity = imgWarped.at<cv::Vec3b>(cv::Point(X,Y));

                        // Set the color (BGR) to point[i].color (RGB)
                        points[i].color[0] = (int) intensity.val[2];
                        points[i].color[1] = (int) intensity.val[1];
                        points[i].color[2] = (int) intensity.val[0];
                    }
                }
                areColorised = true;
            }
        }


        void drawColorisedPoints()
        {
            if(areColorised)
            {
                imgColorPoints = cv::Scalar(0, 0, 0);
                int X, Y;
                for(int i=0; i<points.size(); i++)
                {
                    // Compute the position of the projected points[i] on the warped image
                    X = (int) (offsetX + margin + points[i].px*(width-2*margin));
                    Y = (int) (offsetY + margin + points[i].py*(height-2*margin));

                    // draw the colorised points on the image with colorised points (imgColorPoints)
                    cv::circle(imgColorPoints, cv::Point(X,Y), 5, cv::Scalar(points[i].color[2],points[i].color[1],points[i].color[0]), CV_FILLED, 3, 0);
                }
            }
        }

        void drawPoints()
        {
            if(isWarped)
            {
                imgPoints = imgWarped.clone();
            }
            else
            {
                imgPoints = cv::Mat(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
            }

            int X, Y;
            for(int i=0; i<points.size(); i++)
            {
                // Compute the position of the projected points[i] on the warped image
                X = (int) (offsetX + margin + points[i].px*(width-2*margin));
                Y = (int) (offsetY + margin + points[i].py*(height-2*margin));

                // draw the points on the image with points (imgPoints)
                cv::circle(imgPoints, cv::Point(X,Y), 5, cv::Scalar(255,255,255)*points[i].retro, CV_FILLED, 3, 0);
            }
        }
};

class Colorizer {
    private:
        std::string inputCSV;
        std::string outputCSV;
        std::string folderOfImages;
        std::string signCSV;
        std::map<int, bool> saveStatus;
        std::map<int, std::vector<PointCld> > signs;
        std::map<int, std::vector<PointCld> >::iterator it;
        std::map<int, FrameOfSign> framesOfSign;
        std::map<int, FrameOfImage> framesOfImage;
        int w3height;
        int w3width;
        int margin;
        int offsetX;
        int offsetY;
        float magnification;
        float gSigma;

    public:

        Colorizer(std::string inputCSV_, std::string folderOfImages_, std::string outputCSV_,std::string signCSV_, int w3height_, int w3width_, int margin_, int offsetX_, int offsetY_, float magnification_, float gSigma_)
        {
            inputCSV = inputCSV_;
            outputCSV = outputCSV_;
            folderOfImages = folderOfImages_;
            signCSV = signCSV_;
            getPointsFromCSV();
            it = signs.begin();
            proj3DpointsOn2Dplane();
            w3height = w3height_;
            w3width = w3width_;
            margin = margin_;
            offsetX = offsetX_;
            offsetY = offsetY_;
            magnification = magnification_;
            gSigma = gSigma_;

            for(std::map<int, std::vector<PointCld> >::iterator itr=signs.begin(); itr!=signs.end(); itr++)
            {
                framesOfSign[itr->first] = FrameOfSign(w3height, w3width, margin, offsetX, offsetY);
                framesOfSign[itr->first].init(itr->second, margin, offsetX, offsetY);
                framesOfImage[itr->first] = FrameOfImage(folderOfImages_, signCSV_, itr->first, magnification, margin);
                saveStatus[itr->first] = false;
            }
        }

        void writeOut()
        {
            float vHSV[3];
            // write out CSV file
            std::ofstream csv;
            csv.open(outputCSV.c_str());
            csv << "SignId,Id,X,Y,Z,Retro,Angle,Distance,UTC,R,G,B,H,S,V,pX,pY\n";
            for (std::map<int, std::vector<PointCld> >::iterator itr=signs.begin(); itr!=signs.end(); ++itr)
            {
                std::vector <PointCld> points = itr->second;
                for(int i=0; i<points.size(); i++)
                {
                    if(framesOfSign[itr->first].arePointsColorized())
                    {
                        // compute hsv value
                        cv::Mat3b rgb(cv::Vec3b(points[i].color[0],points[i].color[1],points[i].color[2]));
                        cv::Mat3b hsv;
                        cv::cvtColor(rgb, hsv, CV_RGB2HSV);
                        // scale hsv
                        // h [0,180] -> [0,360] degrees
                        // s [0,255] -> [0,100] percentage
                        // h [0,255] -> [0,100] percentage
                        vHSV[0] = hsv(0)[0]*2.0;
                        vHSV[1] = hsv(0)[1]/255.0;
                        vHSV[2] = hsv(0)[2]/255.0;
                    }
                    else
                    {
                        vHSV[0] = -1;
                        vHSV[1] = -1;
                        vHSV[2] = -1;
                    }
                    // write the point
                    csv << points[i].signId << "," << points[i].id << "," << std::fixed
                        << std::setprecision(7) << points[i].x << "," << points[i].y << ","
                        << std::setprecision(3) << points[i].z << "," << std::setprecision(2)
                        << points[i].retro << "," <<std::setprecision(3)
                        << points[i].angle << "," <<std::setprecision(3)<<points[i].dist<<","
                        << std::setprecision(5) << points[i].utc

                        << std::setprecision(1) << "," << points[i].color[0] << ","
                        << points[i].color[1] << "," << points[i].color[2] << "," << vHSV[0]
                        << "," << std::setprecision(3) << vHSV[1] << "," << vHSV[2] << ","
			<<  points[i].px << "," << points[i].py  << "\n";
                }
            }
            csv.close();
        }

        void save()
        {
            if(framesOfSign[it->first].arePointsColorized())
            {
                signs[it->first] = framesOfSign[it->first].getPoints();
                saveStatus[it->first] = true;
            }
        }

        bool isSaved()
        {
            return saveStatus[it->first];
        }

        FrameOfSign* frameOfSign()
        {
            return &framesOfSign[it->first];
        }

        FrameOfImage* frameOfImage()
        {
            return &framesOfImage[it->first];
        }

        void warpPerspective()
        {
            if(framesOfImage[it->first].warpPerspective(w3height,w3width))
            {
                framesOfSign[it->first].setImgWarped(framesOfImage[it->first].getImgWarped());
                framesOfSign[it->first].colorisePoints();
            }
        }

        int nextSign()
        {
            if(it->first != signs.end()->first)
            {
                it++;
                return 1;
            }
            else
            {
                return 0;
            }
        }

        int precedentSign()
        {
            if(it != signs.begin())
            {
                it--;
                return 1;
            }
            else
            {
                return 0;
            }
        }

        void setInputCSV(std::string inputCSV_)
        {
            inputCSV = inputCSV_;
        }

        void setFolderOfImages(std::string folderOfImages_)
        {
            folderOfImages = folderOfImages_;
        }

        void setSign(int signNumber_, std::vector<PointCld>& sign_)
        {
            signs[signNumber_] = sign_;
        }

        int getSignNumber()
        {
            return it->first;
        }

        void getPointsFromCSV()
        {
            std::ifstream infile(inputCSV.c_str());
            std::string cell, line;
            std::stringstream line_ss;
            for(int k=0; getline(infile, line); k++)
            {
                if(k>0) // ignore csv header
                {
                    line_ss.str(line);
                    PointCld point;
                    for (int i=0; getline(line_ss, cell, ','); i++)
                    {
                        if(i==0) point.signId = stoi(cell);
                        if(i==1) point.id = stoi(cell);
                        if(i==2) point.x = stod(cell);
                        if(i==3) point.y = stod(cell);
                        if(i==4) point.z = stod(cell);
                        if(i==5) point.retro = stod(cell);
                        if(i==6) point.angle = stod(cell);
                        if(i==7) point.dist = stod(cell);

                        if(i==8) point.utc = stod(cell);
                    }
                    line_ss.clear();
                    point.fromLas = false;
                    point.color[0] = -1;
                    point.color[1] = -1;
                    point.color[2] = -1;
                    signs[point.signId].push_back(point);
                }
            }
        }

        void proj3DpointsOn2Dplane()
        {
            for(std::map<int, std::vector<PointCld> >::iterator itr=signs.begin(); itr!=signs.end(); itr++)
            {
                std::vector <PointCld> pointsGeo = itr->second;

                double minLat, maxLat, minLon, maxLon, minH, maxH;
                PointCld pointMinLat, pointMaxLat, pointMinLon, pointMaxLon;

                for(int i=0; i<pointsGeo.size(); i++)
                {
                    if(i==0)
                    {
                        pointMinLat = pointsGeo[i];
                        pointMaxLat = pointsGeo[i];
                        pointMinLon = pointsGeo[i];
                        pointMaxLon = pointsGeo[i];
                        minLat = pointsGeo[i].x;
                        maxLat = pointsGeo[i].x;
                        minLon = pointsGeo[i].y;
                        maxLon = pointsGeo[i].y;
                        minH = pointsGeo[i].z;
                        maxH = pointsGeo[i].z;
                    }
                    else
                    {
                        if(pointsGeo[i].x < minLat)
                        {
                            minLat = pointsGeo[i].x;
                            pointMinLat = pointsGeo[i];
                        }
                        if(pointsGeo[i].x > maxLat)
                        {
                            maxLat = pointsGeo[i].x;
                            pointMaxLat = pointsGeo[i];
                        }
                        if(pointsGeo[i].y < minLon)
                        {
                            minLon = pointsGeo[i].y;
                            pointMinLon = pointsGeo[i];
                        }
                        if(pointsGeo[i].y > maxLon)
                        {
                            maxLon = pointsGeo[i].y;
                            pointMaxLon = pointsGeo[i];
                        }
                        minH = (pointsGeo[i].z < minH)? pointsGeo[i].z : minH;
                        maxH = (pointsGeo[i].z > maxH)? pointsGeo[i].z : maxH;
                    }
                }
                // get the left edge and right edge of the sign
                // we assume that the left edge has the lowest utc
                PointCld leftEdge, rightEdge;
                leftEdge = pointMinLat;
                if(leftEdge.utc<pointMaxLat.utc) leftEdge = pointMaxLat;
                if(leftEdge.utc<pointMinLon.utc) leftEdge = pointMinLon;
                if(leftEdge.utc<pointMaxLon.utc) leftEdge = pointMaxLon;
                rightEdge = pointMinLat;
                if(rightEdge.utc>pointMaxLat.utc) rightEdge = pointMaxLat;
                if(rightEdge.utc>pointMinLon.utc) rightEdge = pointMinLon;
                if(rightEdge.utc>pointMaxLon.utc) rightEdge = pointMaxLon;

                // define top left corner as reference
                GeographicLib::Geocentric earth(GeographicLib::Constants::WGS84_a(), GeographicLib::Constants::WGS84_f());
                GeographicLib::LocalCartesian projw(leftEdge.x, leftEdge.y, maxH, earth);

                // compute height and width of the sign
                double cloudHeight = maxH - minH;
                double cloudWidth, xw, yw, zw;
                projw.Forward(rightEdge.x, rightEdge.y, maxH, xw, yw, zw);
                cloudWidth = sqrt(xw*xw + yw*yw);


                //// Project 3D points on a relative plane
                // Set top left edge of the sign as a reference point for local coords
                GeographicLib::LocalCartesian proj1(leftEdge.x, leftEdge.y, maxH, earth);
                for(int i=0; i<pointsGeo.size(); i++)
                {
                    double xd=-1, yd=-1, zd=-1;
                    // project and compute relative position to top left edge
                    proj1.Forward(pointsGeo[i].x, pointsGeo[i].y, pointsGeo[i].z, xd, yd, zd);
                    pointsGeo[i].px = (sqrt(xd*xd + yd*yd))/cloudWidth;
                    pointsGeo[i].py = -1*zd/cloudHeight;
                }

                itr->second = pointsGeo;
            }
        }
};

void getGeoRepFromUTM(int zone, double easting, double northing, double& lat, double& lon)
{

    // UTM for northern hemisphere
    std::string coords = std::to_string(zone) + "n," + std::to_string(easting) + "," + std::to_string(northing);
    GeographicLib::GeoCoords gc(coords);
    int geoPrecision = 9; // max precision for conversion
    std::string latlong =  gc.GeoRepresentation(geoPrecision);
    std::stringstream latlong_ss(latlong);
    std::string item;
    for(int k=0; getline(latlong_ss, item, ' '); k++)
    {
        if(k==0) lat = stod(item);
        if(k==1) lon = stod(item);
    }
}

void getUTMRepFromGeo(double lat, double lon, int& zone, double& easting, double& northing)
{

    // UTM for northern hemisphere
    std::stringstream coords_ss;
    coords_ss << std::fixed << std::setprecision(10) << lat << " " << lon;
    std::string coords = coords_ss.str();
    GeographicLib::GeoCoords gc(coords);
    int convPrecision = 9; // max precision for conversion
    std::string utm =  gc.UTMUPSRepresentation(convPrecision);
    std::stringstream utm_ss(utm);
    std::string item;

    for(int k=0; getline(utm_ss, item, ' '); k++)
    {
        if(k==0) zone = stod(item.substr(0,item.size()-1));
        if(k==1) easting = stod(item);
        if(k==2) northing = stod(item);
    }
}

int main(int argc, char** argv)
{

    if(argc != 5)
    {
        help();
        return 1;
    }
    // get input args
    std::string inputFile = argv[1];
    std::string outputFile = argv[3];
    std::string inputFolder = argv[2];
    std::string signcsv = argv[4];


    // cvui
    cv::Mat frame1 = cv::Mat(W1_HEIGHT, W1_WIDTH, CV_8UC3);
    cv::Mat frame2;
    cv::Mat frame3;

    // UI
    float magnification = MAGNIFICATION;
    float gSigma = SIGMA;
    cv::Point ptA(-1,-1);
    cv::Point ptB(-1,-1);
    cv::Point ptC(-1,-1);
    cv::Point ptD(-1,-1);
    cv::Point cursor(-1,-1);
    int w3height = W3_HEIGHT;
    int w3width = W3_WIDTH;
    int margin = MARGIN;
    int offsetX = OFFSETX;
    int offsetY = OFFSETY;
    int mouseDownPosX = 0, mouseDownPosY = 0;
    int mouseUpPosX = 0, mouseUpPosY = 0;
    int offsetXInit = 0, offsetYInit = 0;

    // Coloriser object
    Colorizer colorizer(inputFile, inputFolder, outputFile, signcsv,w3height, w3width, margin, offsetX, offsetY, magnification, gSigma);

    // cvui init OpenCV windows
    const cv::String windows[] = {WINDOW1_NAME, WINDOW2_NAME, WINDOW3_NAME};
    cvui::init(windows, 3);
    cv::moveWindow(WINDOW1_NAME, W1_POS_X, W1_POS_Y);
    cv::moveWindow(WINDOW2_NAME, W2_POS_X, W2_POS_Y);
    cv::moveWindow(WINDOW3_NAME, W3_POS_X, W3_POS_Y);

    while (true) {

        /////////////////////////////////   WINDOW 1    ///////////////////////////////////
        cvui::context(WINDOW1_NAME);

        // Fill the frame with a nice color
        frame1 = cv::Scalar(NICE_COLOR);

        //// STEP 0 ////
        // trackbar for image magnification
		cvui::text(frame1, 20, 20, "Step0: Adjust the zoom and the size of the image", 0.45, 0xffffff);
		cvui::text(frame1, 20, 45, "Image magnification: resolution/X");
        if(cvui::trackbar(frame1, 20, 60, 165, &magnification, 0.1f, 5.0f))
        {
            colorizer.frameOfImage()->setMagnification(magnification);
        }

        // Magnification Reset button
        if (cvui::button(frame1, 200, 70, "Magnification Reset"))
        {
            magnification = MAGNIFICATION;
            colorizer.frameOfImage()->setMagnification(magnification);
        }
        // Zoom Reset button
        if (cvui::button(frame1, 380, 70, "Zoom Reset"))
        {
            colorizer.frameOfImage()->resetZoom();
        }


        //// STEP 1 ////
        // print the points A B C D
		cvui::text(frame1, 20, 120, "Step1: Select the 4 corners of the sign", 0.45, 0xffffff);
        cvui::printf(frame1, 20, 150, "Point A = (%d,%d)", ptA.x, ptA.y);
        cvui::printf(frame1, 20, 170, "Point B = (%d,%d)", ptB.x, ptB.y);
        cvui::printf(frame1, 20, 190, "Point C = (%d,%d)", ptC.x, ptC.y);
        cvui::printf(frame1, 20, 210, "Point D = (%d,%d)", ptD.x, ptD.y);

        // Undo button
        if (cvui::button(frame1, 200, 155, "Undo"))
        {
            colorizer.frameOfImage()->undoLastPoint();
            ptA = colorizer.frameOfImage()->getPtA();
            ptB = colorizer.frameOfImage()->getPtB();
            ptC = colorizer.frameOfImage()->getPtC();
            ptD = colorizer.frameOfImage()->getPtD();
        }

        // Reset button
        if (cvui::button(frame1, 200, 190, "Reset"))
        {
            colorizer.frameOfImage()->resetPoints();
            ptA = colorizer.frameOfImage()->getPtA();
            ptB = colorizer.frameOfImage()->getPtB();
            ptC = colorizer.frameOfImage()->getPtC();
            ptD = colorizer.frameOfImage()->getPtD();
        }

        //// STEP 2 ////
		cvui::text(frame1, 20, 240, "Step2: Warp the persepective and adjust the point cloud", 0.45, 0xffffff);
        // // trackbar for offset X
		// cvui::printf(frame1, 20, 265, "Offset X");
        // if(cvui::trackbar(frame1, 20, 280, 200, &offsetX, -30, 30))
        // {
        //     colorizer.frameOfSign()->setOffsetX(offsetX);
        // }

        // // trackbar for offset Y
		// cvui::printf(frame1, 250, 265, "Offset Y");
        // if(cvui::trackbar(frame1, 250, 280, 200, &offsetY, -30, 30))
        // {
        //     colorizer.frameOfSign()->setOffsetY(offsetY);
        // }

        // trackbar for gaussian blur
		cvui::text(frame1, 20, 265, "Gaussian Sigma");
        if(cvui::trackbar(frame1, 20, 280, 200, &gSigma, 0.0f, 12.0f))
        {
            colorizer.frameOfImage()->setGBlurSigma(gSigma);
        }

        // Gaussian Blur Reset button
        if (cvui::button(frame1, 280, 290, "Gaussian Blur Reset"))
        {
            gSigma = SIGMA;
            colorizer.frameOfImage()->setGBlurSigma(gSigma);
        }

        // trackbar for margin
		cvui::printf(frame1, 20, 335, "Size");
        if(cvui::trackbar(frame1, 20, 350, 200, &margin, 0, 100))
        {
            colorizer.frameOfSign()->setMargin(margin);
        }

        // warp the perspective and project the sign
        if ((cvui::button(frame1, 280, 355, "Warp Perspective")))
        {
            colorizer.warpPerspective();
        }

        // TODO show at the bottom left sign number and if it is colored or not
        cvui::printf(frame1, 20, 453, 0.5, 0xffffff, "Sign number: %d", colorizer.getSignNumber());
        if(colorizer.isSaved())
        {
            cvui::text(frame1, 190, 453, "Saved",0.5, 0x42f498);
        }
        else
        {
            cvui::text(frame1, 170, 453, "Not Saved",0.5, 0xf4415c);
        }


        // should be back to last state after one next and one precedent ?

        // Save button
        if (cvui::button(frame1, 420, 400, "Save"))
        {
            colorizer.save();
        }

        // Show Colorised Points Button
        if (cvui::button(frame1, 222, 400, "Show Colorised Points"))
        {
            colorizer.frameOfSign()->setShowColorisedPoints(true);
        }

        // Show Sign Button
        if (cvui::button(frame1, 100, 400, "Show Sign"))
        {
            colorizer.frameOfSign()->setShowColorisedPoints(false);
        }

        // Next button
        if (cvui::button(frame1, 420, 450, "Next"))
        {
            // check if the next sign is available
            if(colorizer.nextSign())
            {
                // get the selection of points
                ptA = colorizer.frameOfImage()->getPtA();
                ptB = colorizer.frameOfImage()->getPtB();
                ptC = colorizer.frameOfImage()->getPtC();
                ptD = colorizer.frameOfImage()->getPtD();
                // get the offset and zoom
                offsetX = colorizer.frameOfSign()->getOffsetX();
                offsetY = colorizer.frameOfSign()->getOffsetY();
                margin = colorizer.frameOfSign()->getMargin();
                magnification = colorizer.frameOfImage()->getMagnification();
                gSigma = colorizer.frameOfImage()->getGBlurSigma();
            }
        }

        // Precedent button
        if (cvui::button(frame1, 300, 450, "Precedent"))
        {
            if(colorizer.precedentSign())
            {
                // get the selection of points
                ptA = colorizer.frameOfImage()->getPtA();
                ptB = colorizer.frameOfImage()->getPtB();
                ptC = colorizer.frameOfImage()->getPtC();
                ptD = colorizer.frameOfImage()->getPtD();
                // get the offset and zoom
                offsetX = colorizer.frameOfSign()->getOffsetX();
                offsetY = colorizer.frameOfSign()->getOffsetY();
                margin = colorizer.frameOfSign()->getMargin();
                magnification = colorizer.frameOfImage()->getMagnification();
                gSigma = colorizer.frameOfImage()->getGBlurSigma();
            }
        }

        // Show everything on the screen
        cvui::imshow(WINDOW1_NAME, frame1);

        /////////////////////////////////   WINDOW 2    ///////////////////////////////////
        cvui::context(WINDOW2_NAME);
        // Fill the frame with a nice color
        //frame2 = cv::Scalar(49, 52, 49);

        // get the cursor and pixel position
        cursor = cvui::mouse();

        // Get the points A B C D
        if (cvui::mouse(cvui::UP)&&(!colorizer.frameOfImage()->zoomSelection()))
        {
            colorizer.frameOfImage()->setPoint(cursor);
            ptA = colorizer.frameOfImage()->getPtA();
            ptB = colorizer.frameOfImage()->getPtB();
            ptC = colorizer.frameOfImage()->getPtC();
            ptD = colorizer.frameOfImage()->getPtD();
        }

        // zoom rectangle
        if (cvui::mouse(cvui::DOWN))
        {
            // get the position of the pixel in the original image.
            colorizer.frameOfImage()->mouseDown(cursor);
        }

        if (cvui::mouse(cvui::IS_DOWN))
        {
            // Compute the width and height
            colorizer.frameOfImage()->mouseIsDown(cursor);
        }

        if (cvui::mouse(cvui::UP))
        {
            // set the zoom rectangle
            colorizer.frameOfImage()->mouseUp();
        }
        // Show everything on the screen
        frame2 = colorizer.frameOfImage()->getFrame();
        cvui::imshow(WINDOW2_NAME, frame2);

        /////////////////////////////////   WINDOW 3    ///////////////////////////////////
        cvui::context(WINDOW3_NAME);

        // Did any mouse button go down?
        if (cvui::mouse(cvui::DOWN)) {
            // get the position of the mouse pointer.
            mouseDownPosX = cvui::mouse().x;
            mouseDownPosY = cvui::mouse().y;
            offsetXInit = offsetX;
            offsetYInit = offsetY;
        }

        // Is any mouse button down (pressed)?
        if (cvui::mouse(cvui::IS_DOWN)) {
            // Adjust the offsetX and offsetY
            offsetX = offsetXInit + cvui::mouse().x - mouseDownPosX;
            offsetY = offsetYInit + cvui::mouse().y - mouseDownPosY;

            colorizer.frameOfSign()->setOffset(offsetX, offsetY);
        }

        // Did any mouse button go up?
        if (cvui::mouse(cvui::UP)) {
            // Reset the mouseDownPosX and mouseDownPosY
            mouseDownPosX = 0;
            mouseDownPosY = 0;
        }

        // Show everything on the screen
        frame3 = colorizer.frameOfSign()->getFrame();
        cvui::imshow(WINDOW3_NAME, frame3);

        // Check if ESC key was pressed
        if (cv::waitKey(20) == 27) {
            colorizer.writeOut();
            break;
        }
    }
    return 0;
}
