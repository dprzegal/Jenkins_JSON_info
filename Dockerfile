FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 \
    && apt-get install -y python3-pip

#define working directory
WORKDIR /Jenkins_JSON_info

COPY /json_file/jenkins_data.json $Home/Jenkins_JSON_info/json_file/
COPY jenkinsinfo_from_json.py $Home/Jenkins_JSON_info/

ENTRYPOINT ["python3"]

CMD ["./jenkinsinfo_from_json.py"]
