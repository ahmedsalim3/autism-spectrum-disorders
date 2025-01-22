// Clip SSBD dataset tool based on https://github.com/antran89/clipping_ssbd_videos with small fixes to update OpenCV constants

#include <opencv2/video.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <fstream>
#include <string>
#include <boost/filesystem.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>

using namespace std;
using namespace cv;
namespace fs = boost::filesystem;
using namespace boost::property_tree;

int main(int argc, char** argv)
{
    const char* keys = 
    {
        "{ d  datasetFolder      | /home/beahacker/Public/data/video/ssbd | }"
        "{ a  annotationFolder   | /home/beahacker/Desktop/workspace/BoW_frameworks/dense_trajectories_BoW/ssbd-release/Annotations | }"
        "{ o  outputFolder       | /home/beahacker/Public/data/video/ssbd_avi | }"
        "{ h  new_height         | 0 | new height of images and flows }"
        "{ w  new_width          | 0 | new width of images and flows }"
    };

    CommandLineParser cmd(argc, argv, keys);
    string datasetFolder = cmd.get<string>("datasetFolder");
    string annotationFolder = cmd.get<string>("annotationFolder");
    string outputFolder = cmd.get<string>("outputFolder");
    int new_height = cmd.get<int>("new_height");
    int new_width = cmd.get<int>("new_width");

    cout << "OpenCV version: " << CV_VERSION << endl;

    string str;
    vector<string> actions;
    fs::path filename(datasetFolder);
    filename.append("classes.txt");

    ifstream infile(filename.c_str());
    if (!infile.is_open()) exit(1);

    while (getline(infile, str))
    {
        actions.push_back(str);
    }
    infile.close();

    int cnt = 0, t1, t2, dur;
    char num[10];

    for (const auto& action : actions)
    {
        fs::path actionFolder(datasetFolder);
        actionFolder.append(action);

        int numFiles = 0;
        for (fs::directory_iterator itr(actionFolder); itr != fs::directory_iterator(); ++itr)
        {
            if (fs::is_regular_file(itr->status())) numFiles++;
        }

        cout << "Total number of files in folder: " << numFiles << endl;

        for (int i = 1; i <= 25; ++i)
        {
            sprintf(num, "_%02d.xml", i);
            string xml_file = "v_" + action + num;
            fs::path xml_path(annotationFolder);
            xml_path.append(xml_file);

            ptree pt;
            read_xml(xml_path.string(), pt);

            string time = pt.get<string>("video.behaviours.behaviour.time");
            sscanf(time.c_str(), "%d:%d", &t1, &t2);

            string duration = pt.get<string>("video.duration");
            sscanf(duration.c_str(), "%ds", &dur);

            cout << "Time of action " << t1 << ":" << t2 << " in video of " << dur << "s" << endl;

            cnt++;
            fs::path vid_path(datasetFolder);
            vid_path.append(action);
            sprintf(num, "_%02d.avi", i);
            string avi_file = "v_" + action + num;
            vid_path.append(avi_file);

            if (!fs::is_regular_file(vid_path)) continue;

            VideoCapture inputVideo(vid_path.c_str());
            double numFrames = inputVideo.get(CAP_PROP_FRAME_COUNT);
            float fps = numFrames / static_cast<float>(dur);
            int start = cvFloor(fps * (t1 / 100 * 60 + t1 % 100));
            int end = cvFloor(fps * (t2 / 100 * 60 + t2 % 100));

            fs::path outvid_path(outputFolder);
            outvid_path.append(action);
            if (!fs::is_directory(outvid_path)) fs::create_directory(outvid_path);

            string video_file = "v_" + action;
            sprintf(num, "_%02d.avi", i);
            video_file.append(num);
            outvid_path.append(video_file);

            if (fs::is_regular_file(outvid_path)) continue;

            int ex = static_cast<int>(inputVideo.get(CAP_PROP_FOURCC));
            new_height = (new_height > 0) ? new_height : inputVideo.get(CAP_PROP_FRAME_HEIGHT);
            new_width = (new_width > 0) ? new_width : inputVideo.get(CAP_PROP_FRAME_WIDTH);
            cv::Size new_size(new_width, new_height);
            VideoWriter outputVideo(outvid_path.c_str(), ex, fps, new_size);

            if (!outputVideo.isOpened())
            {
                cout << "Could not open the output video for write" << endl;
                return -1;
            }

            Mat img;
            int fr = 0;
            while (true)
            {
                inputVideo >> img;
                if (img.empty()) break;
                fr++;
                if (fr < start || fr > end) continue;
                resize(img, img, new_size);
                outputVideo << img;
            }
        }
    }
}
