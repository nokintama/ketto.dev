package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "ok")
	})
	log.Println("Judge service starting on port 8082...")
	if err := http.ListenAndServe(":8082", nil); err != nil {
		log.Fatal("Error starting server:", err)
	}
}
