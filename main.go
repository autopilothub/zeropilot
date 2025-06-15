package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"github.com/gorilla/mux"
	"github.com/stianeikeland/go-rpio/v4"
)

// ESC and Servo configuration
const (
	escPin     = 18
	servoPin   = 17
	pwmFreq    = 50 // 50Hz
	escMinDuty = 5  // 5% duty cycle
	escMaxDuty = 10 // 10% duty cycle
	servoMinDuty = 2.5  // 2.5% duty cycle
	servoMaxDuty = 12.5 // 12.5% duty cycle
)

var (
	escPWM   rpio.Pin
	servoPWM rpio.Pin
)

// Response represents the API response structure
type Response struct {
	Message string `json:"message"`
}

func initGPIO() error {
	// Open and map memory to access GPIO
	if err := rpio.Open(); err != nil {
		return fmt.Errorf("failed to open GPIO: %v", err)
	}

	// Initialize ESC pin
	escPWM = rpio.Pin(escPin)
	escPWM.Mode(rpio.Pwm)
	escPWM.Freq(pwmFreq * 1000) // Convert to Hz
	escPWM.DutyCycle(0, 100)    // Start with 0% duty cycle

	// Initialize Servo pin
	servoPWM = rpio.Pin(servoPin)
	servoPWM.Mode(rpio.Pwm)
	servoPWM.Freq(pwmFreq * 1000) // Convert to Hz
	servoPWM.DutyCycle(0, 100)    // Start with 0% duty cycle

	// Initialize ESC (send minimum signal)
	escPWM.DutyCycle(uint32(escMinDuty), 100)
	return nil
}

func cleanup() {
	// Stop motors
	escPWM.DutyCycle(0, 100)
	servoPWM.DutyCycle(0, 100)
	
	// Close GPIO
	rpio.Close()
}

func setESCSpeed(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	speed := vars["speed"]

	// Convert speed to duty cycle
	var dutyCycle float64
	fmt.Sscanf(speed, "%f", &dutyCycle)
	if dutyCycle < 0 || dutyCycle > 100 {
		http.Error(w, "Speed must be between 0 and 100", http.StatusBadRequest)
		return
	}

	// Calculate duty cycle
	duty := escMinDuty + (escMaxDuty-escMinDuty)*(dutyCycle/100)
	escPWM.DutyCycle(uint32(duty), 100)

	// Send response
	response := Response{
		Message: fmt.Sprintf("ESC speed set to %.1f%%", dutyCycle),
	}
	json.NewEncoder(w).Encode(response)
}

func setServoAngle(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	angle := vars["angle"]

	// Convert angle to duty cycle
	var angleValue float64
	fmt.Sscanf(angle, "%f", &angleValue)
	if angleValue < 0 || angleValue > 180 {
		http.Error(w, "Angle must be between 0 and 180", http.StatusBadRequest)
		return
	}

	// Calculate duty cycle
	duty := servoMinDuty + (servoMaxDuty-servoMinDuty)*(angleValue/180)
	servoPWM.DutyCycle(uint32(duty), 100)

	// Send response
	response := Response{
		Message: fmt.Sprintf("Servo angle set to %.1f°", angleValue),
	}
	json.NewEncoder(w).Encode(response)
}

func main() {
	// Initialize GPIO
	if err := initGPIO(); err != nil {
		log.Fatalf("Failed to initialize GPIO: %v", err)
	}
	defer cleanup()

	// Create router
	r := mux.NewRouter()

	// Define routes
	r.HandleFunc("/esc/speed/{speed}", setESCSpeed).Methods("POST")
	r.HandleFunc("/servo/angle/{angle}", setServoAngle).Methods("POST")
	r.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(Response{Message: "Raspberry Pi Zero Motor Control API"})
	}).Methods("GET")

	// Handle graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		<-sigChan
		log.Println("Shutting down...")
		cleanup()
		os.Exit(0)
	}()

	// Start server
	log.Println("Server starting on :8000")
	log.Fatal(http.ListenAndServe(":8000", r))
} 