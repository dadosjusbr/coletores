FROM golang:1.14.0-alpine AS builder

# Set necessary environmet variables needed for our image
ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# Move to working directory /build
WORKDIR /build/executor

# Copy and download dependency using go mod
COPY ./executor/go.mod .
COPY ./executor/go.sum .
RUN go mod download

# Copy the code into the container
COPY ./executor/. .

# Build the application
RUN go build -o main .

# Move to /dist directory as the place for resulting binary folder
WORKDIR /dist

# Copy code into /dist
COPY . .

# Copy binary main builded aplication to our dist/executor folder
RUN cp /build/executor/main /dist/executor
RUN cp /build/executor/.env /dist/

# Change our context to docker image that will be used to run collectors images
FROM docker:19-git

# Set a new workdir inside our new image
WORKDIR /

# Copy /dist folder from builder to our workdir
COPY --from=builder /dist /

#Execute our binary content inside executor/main
ENTRYPOINT ["/executor/main"]