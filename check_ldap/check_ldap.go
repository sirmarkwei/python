package main

import (
	"fmt"
	"log"
	"os"

	"github.com/bogdanovich/dns_resolver"
)

func main() {
	resolver := dns_resolver.New([]string{"10.124.0.2"})
	resolver.RetryTimes = 5
	ip, err := resolver.LookupHost("<YOUR DNS FQDN YOU WAN TO LOOKUP>")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Could not get IPs: %v\n", err)

	}
	log.Printf("\nValue: %v\nType: %T\n", ip[0], ip)
}
