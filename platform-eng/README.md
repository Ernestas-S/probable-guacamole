# Messaging System in Go

## Overview

This project demonstrates a messaging system that reads lines from an input file, sends them via RabbitMQ, and writes them back into another file, implemented in Go.

## Components

* **Producer**: Reads lines from `input.txt` and sends them to RabbitMQ.
* **Consumer**: Receives lines from RabbitMQ and writes them into `output.txt`.
* **RabbitMQ**: Message broker for communication.

## Features

* HTTP health checks.
* Prometheus metrics for observability.
* Docker containerization.
* Kubernetes deployment manifests.

## Technologies Used

* Go
* RabbitMQ
* Prometheus
* Gin Framework
* Docker
* Kubernetes

## How it Works

### Producer

* Reads from `input.txt`
* Sends each line to RabbitMQ.
* Exposes health check (`/health`) and metrics (`/metrics`) endpoints.

### Consumer

* Listens to messages from RabbitMQ.
* Writes received lines to `output.txt`.
* Exposes health check (`/health`) and metrics (`/metrics`) endpoints.

## Running with Docker Compose

```sh
docker-compose up --build
```

Access services:

* RabbitMQ: `localhost:15672`
* Producer health: `localhost:8081/health`
* Consumer health: `localhost:8082/health`

## Kubernetes Deployment

Use provided manifests in the `k8s/` folder:

```sh
kubectl apply -f k8s/producer-deployment.yaml
kubectl apply -f k8s/consumer-deployment.yaml
```

## Testing

Check that `input.txt` and `output.txt` match after the system runs to confirm successful messaging.

## Observability

Prometheus metrics are available at:

* Producer: `localhost:8081/metrics`
* Consumer: `localhost:8082/metrics`

## Design Choices

* **Golang**: Chosen for concurrency and efficient handling of I/O.
* **RabbitMQ**: Reliable and straightforward message queue.
* **Prometheus & Gin**: Simple yet powerful for observability and health checks.
* **Docker & Kubernetes**: Easy deployment and scalability.

## Future Enhancements

* Add horizontal scaling capabilities.
* Implement robust error handling and retries.
* Include automated end-to-end testing in CI/CD pipelines.
