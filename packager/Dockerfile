FROM golang:1.14.0-alpine AS builder

ARG GIT_COMMIT=unspecified

# Set necessary environmet variables needed for our image
ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# Move to working directory /build
WORKDIR /build

# Copy and download dependency using go mod
COPY go.mod .
COPY go.sum .
RUN go mod download

# Copy the code into the container
COPY . .

# Build the application
RUN go build -o main

# Move to /dist directory as the place for resulting binary folder
WORKDIR /dist

# Copy binary and .env from build to main folder
RUN cp /build/main .
RUN cp /build/datapackage_descriptor.json .

# Build a small image
FROM alpine:3.7

COPY --from=builder /dist/ /


# Command to run
ENTRYPOINT ["/main"]