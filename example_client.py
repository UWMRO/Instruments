import http.client


def print_response(res):
    # Read response, decode from bytestring to normal string
    text = res.read().decode()
    print(f"[{res.status} {res.reason}] {text}")


# Create connection
conn = http.client.HTTPConnection('localhost', 5000)

# Send GET request and display response
conn.request("GET", "/")
print_response(conn.getresponse())

# Request and display temperature
conn.request("GET", "/temperature")
print_response(conn.getresponse())
