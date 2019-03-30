package main

import (
    "fmt"
    "net/http"
    "os"
)

func main() {
    port := "8000"

    if len(os.Args) == 2 {
        port = os.Args[1]
    } else if len(os.Args) > 2 {
        fmt.Printf("Usage: %s [PORT]\n", os.Args[1])
    }

    cwd, _ := os.Getwd()
    http.Handle("/", http.FileServer(http.Dir(".")))

    fmt.Printf("Serving files from %s on port %s\n", cwd, port)
    http.ListenAndServe(":" + port, nil)

}

