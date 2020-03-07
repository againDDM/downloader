package main

import (
	"encoding/json"
	"net/http"
	"time"
)

// Body is a data structure for marshaling convenience.
type Body struct {
	Result string `json:"result"`
	Task   string `json:"task"`
	Tasks  []Task `json:"tasks"`
}

// Task is a data structure for marshaling convenience.
type Task struct {
	Target string `json:"url"`
	Status string `json:"status"`
}

func getTasksHandle(w http.ResponseWriter, r *http.Request) {
	body := Body{
		Result: "success",
		Tasks: []Task{
			Task{
				Target: "test-wait",
				Status: "WAIT",
			},
			Task{
				Target: "test-processed",
				Status: "PROCESSED",
			},
			Task{
				Target: "test-success",
				Status: "SUCCESS",
			},
			Task{
				Target: "test-unknow",
				Status: "UNKNOW",
			},
			Task{
				Target: "test-failed",
				Status: "FAILED",
			},
		},
	}
	json.NewEncoder(w).Encode(body)
}

func addTaskHandle(w http.ResponseWriter, r *http.Request) {
	time.Sleep(time.Duration(5) * time.Second)
	body := Body{
		Result: "success",
		Task:   "placeholder",
	}
	json.NewEncoder(w).Encode(body)
}

func deleteTaskHandle(w http.ResponseWriter, r *http.Request) {
	time.Sleep(time.Duration(2) * time.Second)
	body := Body{
		Result: "deleted",
		Task:   "placeholder",
	}
	json.NewEncoder(w).Encode(body)
}

func tasksHandle(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "OPTIONS":
		func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Allow", "GET, POST, DELETE, HEAD, OPTIONS")
			w.WriteHeader(http.StatusOK)
		}(w, r)
	case "GET":
		getTasksHandle(w, r)
	case "POST":
		addTaskHandle(w, r)
	case "DELETE":
		deleteTaskHandle(w, r)
	case "HEAD":
		func(w http.ResponseWriter, r *http.Request) {
			w.WriteHeader(http.StatusOK)
		}(w, r)
	default:
		func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Allow", "GET, POST, DELETE, HEAD, OPTIONS")
			w.WriteHeader(http.StatusMethodNotAllowed)
		}(w, r)
	}
}
