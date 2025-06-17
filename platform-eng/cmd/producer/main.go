package main

import (
	"bufio"
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/streadway/amqp"
)

var linesSent = prometheus.NewCounter(
	prometheus.CounterOpts{
		Name: "producer_lines_sent_total",
		Help: "Total lines sent to queue",
	},
)

func init() {
	prometheus.MustRegister(linesSent)
}

func publishLines(filePath string, amqpURL string, queueName string) {
	conn, err := amqp.Dial(amqpURL)
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(queueName, false, false, false, false, nil)
	failOnError(err, "Failed to declare a queue")

	file, err := os.Open(filePath)
	failOnError(err, "Failed to open file")
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		body := scanner.Text()
		err = ch.Publish("", q.Name, false, false, amqp.Publishing{ContentType: "text/plain", Body: []byte(body)})
		failOnError(err, "Failed to publish message")
		linesSent.Inc()
		log.Printf("Sent: %s", body)
	}
	failOnError(scanner.Err(), "Error reading file")
}

func main() {
	go publishLines("input.txt", "amqp://guest:guest@rabbitmq:5672/", "line_queue")

	router := gin.Default()
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "Producer running"})
	})

	router.GET("/metrics", gin.WrapH(promhttp.Handler()))

	router.Run(":8080")
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}
