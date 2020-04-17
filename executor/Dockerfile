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

COPY . .

RUN cp /build/executor/main /dist/executor

FROM docker:19-git

WORKDIR /coletores

COPY --from=builder /dist /coletores

WORKDIR /coletores/executor
ENTRYPOINT ["/coletores/executor/main"]