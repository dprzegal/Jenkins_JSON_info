Program shows some info about the file: jenkins_data.json that is being put in the directory named json_file. In the same directory the file jenkins_data_output.json can be found if during the program running user will choose to save the sorted or changed data of the original file: jenkins_data.json.

commands that can be used to test working on this project (used by me)

--- with alpine (Dockerfile_alpine)---

#you can make image of alpine version with command:
sudo docker build -f Dockerfile_alpine . -t jenkins_json_alpine:v1

#you can create and run container for alpine image:
sudo docker run -d -it --rm -v $(pwd)/json_file/:/Jenkins_JSON_info/json_file/ --name=jenkinsjsonalpine1 jenkins_json_alpine:v1

#you can go to your container's command line:
sudo docker exec -it jenkinsjsonalpine1 sh

#and see how the script is working:
python3 jenkinsinfo_from_json.py



---- with ubuntu (Dockerfile)----

#you can make image with ubuntu version with command:
sudo docker build . -t jenkins_json_info:v1

#you can create and run container for alpine image:
sudo docker run -d -it --rm -v $(pwd)/json_file/:/Jenkins_JSON_info/json_file/ --name=jenkinsjsoninfo1 jenkins_json_info:v1

#you can go to your container's command line:
sudo docker exec -it jenkinsjsoninfo1 sh

#and see how the script is working:
python3 jenkinsinfo_from_json.py
