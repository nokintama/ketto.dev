FROM golang:1.26.5
WORKDIR /app
COPY . .
RUN go build -o judge ./cmd/judge
CMD ["./judge"]