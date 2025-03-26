FROM docker.elastic.co/beats/filebeat:8.10.2

COPY filebeat.yml /usr/share/filebeat/filebeat.yml
