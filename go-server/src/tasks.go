package main

// Task is a data structure for marshaling convenience.
type Task struct {
	Target string `json:"target"`
	Status string `json:"status"`
}
