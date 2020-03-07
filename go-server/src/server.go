package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	_ "github.com/lib/pq"
)

// >>> DATABASE SECTION <<<

var db *sql.DB
var pgConfig = struct {
	driverName      string
	dbSchema        string
	PGuser          string
	PGpassword      string
	PGhost          string
	PGport          string
	PGdatabase      string
	PGmaxConnection int
}{
	driverName:      "postgres",
	dbSchema:        "postgres",
	PGuser:          os.Getenv("PGUSER"),
	PGpassword:      os.Getenv("PGPASSWORD"),
	PGhost:          os.Getenv("PGHOST"),
	PGport:          os.Getenv("PGPORT"),
	PGdatabase:      os.Getenv("PGDATABASE"),
	PGmaxConnection: 10,
}

func initDatabase() {
	dataSourceName := fmt.Sprintf(
		"%v://%v:%v@%v:%v/%v?sslmode=disable",
		pgConfig.dbSchema, pgConfig.PGuser, pgConfig.PGpassword,
		pgConfig.PGhost, pgConfig.PGport, pgConfig.PGdatabase,
	)
	var err error
	db, err = sql.Open(pgConfig.driverName, dataSourceName)
	if err != nil {
		log.Fatal("Database connection error :: ", err)
	}
	db.SetMaxOpenConns(pgConfig.PGmaxConnection)
	if err = db.Ping(); err != nil {
		log.Fatal("Database error :: ", err)
	} else {
		log.Println("Success initialization")
	}
}

// <<<------ end of section ------>>>

var httpConfig = struct {
	port string
	cors string
}{
	port: os.Getenv("HTTP_PORT"),
	cors: os.Getenv("CORS_STRING"),
}

func handleCors(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Add("Access-Control-Allow-Origin", httpConfig.cors)
		w.Header().Set(
			"Access-Control-Allow-Methods",
			"GET, POST, DELETE, HEAD, OPTIONS",
		)
		w.Header().Set("Access-Control-Allow-Headers", "content-type")
		next.ServeHTTP(w, r)
	})
}

func accessLogMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		log.Printf("[%s] %s, %s %s Origin: %s\n",
			r.Method, r.RemoteAddr, r.URL.Path,
			time.Since(start), r.Header["Origin"],
		)
	})
}

func panicMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				log.Println("RECOVERED", err)
				http.Error(w, "Internal server error", 500)
			}
		}()
		next.ServeHTTP(w, r)
	})
}

func main() {
	// initDatabase() #sometime later
	mux := http.NewServeMux()
	mux.HandleFunc("/api/tasks/", tasksHandle)

	apiHandler := handleCors(mux)
	apiHandler = accessLogMiddleware(apiHandler)
	apiHandler = panicMiddleware(apiHandler)

	log.Fatal(http.ListenAndServe(":"+os.Getenv("HTTP_PORT"), apiHandler))
}
