//// Remember to check : joints[i].pos.z = -joint.z;
//
//// STL Header
//#include <iterator>
//// #include <iostream>
//#include <fstream>
//#include <sstream>
//#include <vector>
//#include <string>
//#include <iostream>
//#include "kinectbvh.h"
//#define xRow 4
//#define yRow 5
//#define zRow 6
//#define spineBase 0
//#define spineMid 4
//#define neck 8
//#define head 12
//#define shoulderLeft 16
//#define elbowLeft 20
//#define wristLeft 24
//#define handLeft 28
//#define shoulderRight 32
//#define elbowRight 36
//#define wristRight 40
//#define handRight 44
//#define hipLeft 48
//#define kneeLeft 52
//#define ankleLeft 56
//#define footLeft 60
//#define hipRight 64
//#define kneeRight 68
//#define ankleRight 72
//#define footRight 76
//#define spineShoulder 80
//#define handTipLeft 84
//#define thumbLeft 88
//#define handTipRight 92
//#define thumbRight 96
//
//
//using namespace std ;
//bool m_bIsCalibrated = false;
//KinectBVH *m_pKinectBVH = NULL;
//
//
//class CSVRow
//{
//public:
//    std::string const& operator[](std::size_t index) const
//    {
//        return m_data[index];
//    }
//    std::size_t size() const
//    {
//        return m_data.size();
//    }
//    void readNextRow(std::istream& str)
//    {
//        std::string         line;
//        std::getline(str, line);
//
//        std::stringstream   lineStream(line);
//        std::string         cell;
//
//        m_data.clear();
//        while(std::getline(lineStream, cell, ','))
//        {
//            m_data.push_back(cell);
//        }
//        // This checks for a trailing comma with no data after it.
//        if (!lineStream && cell.empty())
//        {
//            // If there was a trailing comma then add an empty element.
//            m_data.push_back("");
//        }
//    }
//private:
//    std::vector<std::string>    m_data;
//};
//
//std::istream& operator>>(std::istream& str, CSVRow& data)
//{
//    data.readNextRow(str);
//    return str;
//}
//
//
//void CalibrateSkeleton()
//{
//    m_pKinectBVH->CalibrateSkeleton();
//    m_bIsCalibrated = true;
//}
//
//void ProcessBonesOrientation(vector<Joint> skeletonJoints)
//{
//    vector<Joint> joints(JOINT_SIZE);
//    // Fill joints
//    for (int i = 0; i < JOINT_SIZE; i++)
//    {
//        // nite::Point3f pos = skel.getJoint((nite::JointType)i).getPosition();
//        Joint joint = skeletonJoints.at(i) ;
//        joints[i].pos.x = joint.pos.x;
//        joints[i].pos.y = joint.pos.y;
//        // convert to right hand coordinate
//        joints[i].pos.z = -joint.pos.z; // NOT SURE ABOUT THIS, MUST CHECK THIS
//        // joints[i].tracked = skel.getJoint((nite::JointType)i).getPositionConfidence() > 0.5f;
//        joints[i].tracked = true ;
//    }
//
//    // Add the positions of all joints.
//    m_pKinectBVH->AddAllJointsPosition(&joints[0]);
//
//    // Increase the frame number.
//    m_pKinectBVH->IncrementNbFrames();
//}
//
//// function which read csv file and generates an (T cross 15) vector of vectors
//
///**
// *   Current Mapping
// *    NiTE                Kinect
// *    Head                head
// *    Neck                spineShoulder
// *    LeftShoulder        shoulderLeft
// *    RightShoulder       shoulderRight
// *    LeftElbow           elbowLeft
// *    RightELbow          elbowRight
// *    LeftHand            handLeft
// *    RightHand           handRight
// *    Torso               (spineMid + spineBash)/2
// *    LeftHip             hipLeft
// *    RightHip            hipRight
// *    LeftKnee            kneeLeft
// *    RightKnee           kneeRight
// *    LeftFoot            footLeft
// *    RightFoor           footRight
// **/
//
//
//
//vector<vector<Joint>> readJointsFromCSV( string filename) {
//    std::ifstream       file(filename);
//
//    CSVRow              row;
//    vector<vector<Joint>> jointLocations ;
//    while(file >> row)
//    {
//        vector<Joint> currFrameJoints ;
//        Joint currJoint ;
//        currJoint.pos.x = stof(row[head + 1]) ;
//        currJoint.pos.y = stof(row[head + 2]) ;
//        currJoint.pos.z = stof(row[head + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[spineShoulder + 1]) ;
//        currJoint.pos.y = stof(row[spineShoulder + 2]) ;
//        currJoint.pos.z = stof(row[spineShoulder + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[shoulderLeft + 1]) ;
//        currJoint.pos.y = stof(row[shoulderLeft + 2]) ;
//        currJoint.pos.z = stof(row[shoulderLeft + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[shoulderRight + 1]) ;
//        currJoint.pos.y = stof(row[shoulderRight + 2]) ;
//        currJoint.pos.z = stof(row[shoulderRight + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[elbowLeft + 1]) ;
//        currJoint.pos.y = stof(row[elbowLeft + 2]) ;
//        currJoint.pos.z = stof(row[elbowLeft + 3] ) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[elbowRight + 1]) ;
//        currJoint.pos.y = stof(row[elbowRight + 2]) ;
//        currJoint.pos.z = stof(row[elbowRight + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[handLeft + 1]) ;
//        currJoint.pos.y = stof(row[handLeft + 2]) ;
//        currJoint.pos.z = stof(row[handLeft + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[handRight + 1]) ;
//        currJoint.pos.y = stof(row[handRight + 2]) ;
//        currJoint.pos.z = stof(row[handRight + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = ( stof(row[spineMid + 1]) + stof(row[spineBase + 1]) ) / 2 ;
//        currJoint.pos.y = ( stof(row[spineMid + 2]) + stof(row[spineBase + 2]) ) / 2 ;
//        currJoint.pos.z = ( stof(row[spineMid + 3]) + stof(row[spineBase + 3]) ) / 2 ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[hipLeft + 1]) ;
//        currJoint.pos.y = stof(row[hipLeft + 2]) ;
//        currJoint.pos.z = stof(row[hipLeft + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[hipRight + 1]) ;
//        currJoint.pos.y = stof(row[hipRight + 2]) ;
//        currJoint.pos.z = stof(row[hipRight + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[kneeLeft + 1]) ;
//        currJoint.pos.y = stof(row[kneeLeft + 2]) ;
//        currJoint.pos.z = stof(row[kneeLeft + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[kneeRight + 1]) ;
//        currJoint.pos.y = stof(row[kneeRight + 2]) ;
//        currJoint.pos.z = stof(row[kneeRight + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[footLeft + 1]) ;
//        currJoint.pos.y = stof(row[footLeft + 2]) ;
//        currJoint.pos.z = stof(row[footLeft + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
////        Joint currJoint ;
//        currJoint.pos.x = stof(row[footRight + 1]) ;
//        currJoint.pos.y = stof(row[footRight + 2]) ;
//        currJoint.pos.z = stof(row[footRight + 3]) ;
//        currFrameJoints.push_back(currJoint) ;
//
//        jointLocations.push_back(currFrameJoints) ;
//    }
//
//
//    return jointLocations ;
//}
//
//void endConversion( ) {
//
//    time_t nowtime = time(NULL);
//    struct tm *local = localtime(&nowtime);
//    char buf[256];
//    sprintf(buf, "/Users/daddysHome/data/%d-%d-%d-%d-%d-%d.bvh", local->tm_year+1900, local->tm_mon+1, local->tm_mday, local->tm_hour, local->tm_min, local->tm_sec);
//    cout << buf << endl ;
//    m_pKinectBVH->SaveToBVHFile(buf);
//    delete m_pKinectBVH;
//    m_pKinectBVH = NULL;
//    m_bIsCalibrated = false;
//
//}
//
//int main( int argc, char *	*argv )
//{
//    string filename = "output.csv" ;
//    vector<vector<Joint>>  jointCoordinates = readJointsFromCSV(filename) ;
//
//    for(int frameNo = 0 ;  frameNo < jointCoordinates.size() ; frameNo += 1) {
//        if(!m_bIsCalibrated){
//            CalibrateSkeleton() ;
//        }
//        ProcessBonesOrientation(jointCoordinates.at(frameNo)) ;
//    }
//    endConversion() ;
//
//    if (m_pKinectBVH)
//    {
//        delete m_pKinectBVH;
//        m_pKinectBVH = NULL;
//    }
//    cout <<"finished" << endl ;
//}

// Remember to check : joints[i].pos.z = -joint.z;
#include<algorithm>
#include<string.h>
#include<time.h>
// STL Header
#include <iterator>
// #include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <iostream>
#include "kinectbvh.h"
#define xRow 4
#define yRow 5
#define zRow 6
#define spineBase 0
#define spineMid 4
#define neck 8
#define head 12
#define shoulderLeft 16
#define elbowLeft 20
#define wristLeft 24
#define handLeft 28
#define shoulderRight 32
#define elbowRight 36
#define wristRight 40
#define handRight 44
#define hipLeft 48
#define kneeLeft 52
#define ankleLeft 56
#define footLeft 60
#define hipRight 64
#define kneeRight 68
#define ankleRight 72
#define footRight 76
#define spineShoulder 80
#define handTipLeft 84
#define thumbLeft 88
#define handTipRight 92
#define thumbRight 96


using namespace std ;
bool m_bIsCalibrated = false;
KinectBVH *m_pKinectBVH = NULL;


class CSVRow
{
public:
    std::string const& operator[](std::size_t index) const
    {
        return m_data[index];
    }
    std::size_t size() const
    {
        return m_data.size();
    }
    void readNextRow(std::istream& str)
    {
        std::string         line;
        std::getline(str, line);

        std::stringstream   lineStream(line);
        std::string         cell;

        m_data.clear();
        while(std::getline(lineStream, cell, ','))
        {
            m_data.push_back(cell);
        }
        // This checks for a trailing comma with no data after it.
        if (!lineStream && cell.empty())
        {
            // If there was a trailing comma then add an empty element.
            m_data.push_back("");
        }
    }
private:
    std::vector<std::string>    m_data;
};

std::istream& operator>>(std::istream& str, CSVRow& data)
{
    data.readNextRow(str);
    return str;
}


void CalibrateSkeleton()
{
    m_pKinectBVH->CalibrateSkeleton();
    m_bIsCalibrated = true;
}

void ProcessBonesOrientation(vector<Joint> skeletonJoints)
{
    vector<Joint> joints(JOINT_SIZE);
    // Fill joints
    for (int i = 0; i < JOINT_SIZE; i++)
    {
        // nite::Point3f pos = skel.getJoint((nite::JointType)i).getPosition();
        Joint joint = skeletonJoints.at(i) ;
        joints[i].pos.x = joint.pos.x;
        joints[i].pos.y = joint.pos.y;
        // convert to right hand coordinate
        joints[i].pos.z = -joint.pos.z; // NOT SURE ABOUT THIS, MUST CHECK THIS
        // joints[i].tracked = skel.getJoint((nite::JointType)i).getPositionConfidence() > 0.5f;
        joints[i].tracked = true ;
    }

    // Add the positions of all joints.
    m_pKinectBVH->AddAllJointsPosition(&joints[0]);

    // Increase the frame number.
    m_pKinectBVH->IncrementNbFrames();
}

// function which read csv file and generates an (T cross 15) vector of vectors

/**
 *   Current Mapping
 *    NiTE                Kinect
 *    Head                head
 *    Neck                spineShoulder
 *    LeftShoulder        shoulderLeft
 *    RightShoulder       shoulderRight
 *    LeftElbow           elbowLeft
 *    RightELbow          elbowRight
 *    LeftHand            handLeft
 *    RightHand           handRight
 *    Torso               (spineMid + spineBash)/2
 *    LeftHip             hipLeft
 *    RightHip            hipRight
 *    LeftKnee            kneeLeft
 *    RightKnee           kneeRight
 *    LeftFoot            footLeft
 *    RightFoor           footRight
 **/



vector<vector<Joint> > readJointsFromCSV( string filename) {
    // cout<<"check filename here  "<< filename << endl ;
    std::ifstream       file(filename);

    CSVRow              row;
    vector<vector<Joint> > jointLocations ;
    while(file >> row)
    {
        vector<Joint> currFrameJoints ;
        Joint currJoint ;
        currJoint.pos.x = stof(row[head + 1]) ;
        currJoint.pos.y = stof(row[head + 2]) ;
        currJoint.pos.z = stof(row[head + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[spineShoulder + 1]) ;
        currJoint.pos.y = stof(row[spineShoulder + 2]) ;
        currJoint.pos.z = stof(row[spineShoulder + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[shoulderLeft + 1]) ;
        currJoint.pos.y = stof(row[shoulderLeft + 2]) ;
        currJoint.pos.z = stof(row[shoulderLeft + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[shoulderRight + 1]) ;
        currJoint.pos.y = stof(row[shoulderRight + 2]) ;
        currJoint.pos.z = stof(row[shoulderRight + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[elbowLeft + 1]) ;
        currJoint.pos.y = stof(row[elbowLeft + 2]) ;
        currJoint.pos.z = stof(row[elbowLeft + 3] ) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[elbowRight + 1]) ;
        currJoint.pos.y = stof(row[elbowRight + 2]) ;
        currJoint.pos.z = stof(row[elbowRight + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[handLeft + 1]) ;
        currJoint.pos.y = stof(row[handLeft + 2]) ;
        currJoint.pos.z = stof(row[handLeft + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[handRight + 1]) ;
        currJoint.pos.y = stof(row[handRight + 2]) ;
        currJoint.pos.z = stof(row[handRight + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = ( stof(row[spineMid + 1]) + stof(row[spineBase + 1]) ) / 2 ;
        currJoint.pos.y = ( stof(row[spineMid + 2]) + stof(row[spineBase + 2]) ) / 2 ;
        currJoint.pos.z = ( stof(row[spineMid + 3]) + stof(row[spineBase + 3]) ) / 2 ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[hipLeft + 1]) ;
        currJoint.pos.y = stof(row[hipLeft + 2]) ;
        currJoint.pos.z = stof(row[hipLeft + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[hipRight + 1]) ;
        currJoint.pos.y = stof(row[hipRight + 2]) ;
        currJoint.pos.z = stof(row[hipRight + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[kneeLeft + 1]) ;
        currJoint.pos.y = stof(row[kneeLeft + 2]) ;
        currJoint.pos.z = stof(row[kneeLeft + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[kneeRight + 1]) ;
        currJoint.pos.y = stof(row[kneeRight + 2]) ;
        currJoint.pos.z = stof(row[kneeRight + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[footLeft + 1]) ;
        currJoint.pos.y = stof(row[footLeft + 2]) ;
        currJoint.pos.z = stof(row[footLeft + 3]) ;
        currFrameJoints.push_back(currJoint) ;
//        Joint currJoint ;
        currJoint.pos.x = stof(row[footRight + 1]) ;
        currJoint.pos.y = stof(row[footRight + 2]) ;
        currJoint.pos.z = stof(row[footRight + 3]) ;
        currFrameJoints.push_back(currJoint) ;

        jointLocations.push_back(currFrameJoints) ;
    }

    // cout << "reading csv complete" << endl ;
    return jointLocations ;
}

// void endConversion( ) {

//     time_t nowtime = time(NULL);
//     struct tm *local = localtime(&nowtime);
//     char buf[256];
//     sprintf(buf, "../data/%d-%d-%d-%d-%d-%d.bvh", local->tm_year+1900, local->tm_mon+1, local->tm_mday, local->tm_hour, local->tm_min, local->tm_sec);
//     m_pKinectBVH->SaveToBVHFile(buf);
//     delete m_pKinectBVH;
//     m_pKinectBVH = NULL;
//     m_bIsCalibrated = false;

// }

void endConversion(string targetDir ,string ofilename ) {

    time_t nowtime = time(NULL);
    struct tm *local = localtime(&nowtime);
    char buf[256];
    sprintf(buf, "%s/%s.bvh",targetDir.c_str() ,  ofilename.c_str());
    // cout<<"see buf here:" << buf->sc_str() << endl ; 
    m_pKinectBVH->SaveToBVHFile(buf);
    delete m_pKinectBVH;
    m_pKinectBVH = NULL;
    m_bIsCalibrated = false;

}



int main( int argc, char *argv[] )
{   
    std::string current_exec_name = argv[0]; // Name of the current exec program
    std::string first_arge;
    std::vector<std::string> all_args;
    if (argc > 1) {

        first_arge = argv[1];
        all_args.assign(argv + 1, argv + argc);
    }

    std::ifstream infile(argv[1]);

    if (infile.is_open() && infile.good()) {
        cout << "File is now open!\nContains:\n";
        string line;
        while (getline(infile, line)){
              cout <<line<<"\n";
            string filename = line;
            string noExtFN = filename.substr(0, filename.size() - 4) ;
            std::string onlyFileName = noExtFN;
           std::string delimiter = "/";

    size_t pos = 0;
    std::string token;
    while ((pos = onlyFileName.find(delimiter)) != std::string::npos) {
        token = onlyFileName.substr(0, pos);
        // std::cout << token << std::endl;
        onlyFileName.erase(0, pos + delimiter.length());
    }
    // std::cout << s << std::endl;    
    string targetDir = all_args.at( 1 ) ; 
    vector<vector<Joint> >  jointCoordinates = readJointsFromCSV(filename) ;
    m_pKinectBVH = new KinectBVH();
    for(int frameNo = 0 ;  frameNo < jointCoordinates.size() ; frameNo += 1) {
        if(!m_bIsCalibrated){
            CalibrateSkeleton() ;
        }
        ProcessBonesOrientation(jointCoordinates.at(frameNo)) ;
    }
    endConversion(targetDir, onlyFileName) ;

    if (m_pKinectBVH)
    {
        delete m_pKinectBVH;
        m_pKinectBVH = NULL;
        }
    }
        }
        
  else {
        cout << "Failed to open file..";
    }

    
}

