#!/bin/bash



monitor() {
  inotifywait -mrq --format '%e'  --event create,delete,modify $1 | while read event
  do
      case $event in 
           MODIFY|CREATE|DELETE)
              rsync -avr $1  jenkins-slave1:$1
              rsync -avr $1  jenkins-slave3:$1
              ;;
           *)
      esac
  done

}

monitor "/data/ops/" &
monitor "/data/scripts/" &
monitor "/data/tools/" &
