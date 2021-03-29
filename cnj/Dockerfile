# set base image
FROM blang/busybox-bash

ARG COURT
ARG YEAR
ARG MONTH

# copy the file to the working directory
ADD https://github.com/diegooalmeida/backup/raw/master/${COURT}.zip /

RUN unzip ${COURT}.zip
RUN rm ${COURT}.zip

RUN cat ${COURT}-${MONTH}-${YEAR}.json



