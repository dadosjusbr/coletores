# set base image
FROM alpine:latest

ARG COURT
ARG YEAR
ARG MONTH
ENV FILE=${COURT}-${MONTH}-${YEAR}.json

# copy the file to the working directory
ADD https://github.com/diegooalmeida/backup/raw/master/${COURT}.zip .

RUN unzip ${COURT}.zip
RUN rm ${COURT}.zip

CMD ["sh", "-c", "cat ${FILE}"]