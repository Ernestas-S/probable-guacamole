package main

import (
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/streadway/amqp"
)

var linesReceived = prometheus.NewCounter(
	prometheus.CounterOpts{
		Name: "consumer_lines_received_total",
		Help: "Total lines received from queue",
	},
)

func init() {
	prometheus.MustRegister(linesReceived)
}

func consumeLines(outputFile string, amqpURL string, queueName string) {
	conn, err := amqp.Dial(amqpURL)
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(queueName, false, false, false, false, nil)
	failOnError(err, "Failed to declare a queue")

	msgs, err := ch.Consume(q.Name, "", true, false, false, false, nil)
	failOnError(err, "Failed to register consumer")

	file, err := os.Create(outputFile)
	failOnError(err, "Failed to create file")
	defer file.Close()

	forever := make(chan bool)

	go func() {
		for d := range msgs {
			file.WriteString(string(d.Body) + "\n")
			linesReceived.Inc()
			log.Printf("Received: %s", d.Body)
		}
	}()

	log.Printf("Waiting for messages...")
	<-forever
}

func main() {
	go consumeLines("output.txt", "amqp://guest:guest@rabbitmq:5672/", "line_queue")

	router := gin.Default()
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "Consumer running"})
	})

	router.GET("/metrics", gin.WrapH(promhttp.Handler()))

	router.Run(":8080")
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}
