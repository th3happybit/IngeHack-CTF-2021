vcl 4.1;
backend apache { # Define one backend
    .host = "client.haxor"; # IP or Hostname of backend
    .port = "80"; # Port Apache or whatever is listening
    .max_connections = 500; # That's it 500
    .probe = {
        #.url = "/"; # short easy way (GET /)
        # We prefer to only do a HEAD /
        .request =
        "HEAD / HTTP/1.1"
        "Host: localhost"
        "Connection: close"
        "User-Agent: Varnish Health Probe";

        .interval  = 60s; # check the health of each backend every 60 seconds
        .timeout   = 10s; # timing out after 10 second.
        .window    = 5;   # If 3 out of the last 5 polls succeeded the backend is considered healthy, otherwise it will be marked as sick
        .threshold = 3;
    }
    .first_byte_timeout     = 300s;   # How long to wait before we receive a first byte from our backend?
    .connect_timeout        = 10s;     # How long to wait for a backend connection?
    .between_bytes_timeout  = 5s;     # How long to wait between bytes received from our backend?
}
backend api {
    .host = "api.haxor";
    .port = "5000";
    .max_connections = 300;
    .probe = {
    	.url = "/";
        .interval  = 60s;
        .timeout   = 10s;
        .window    = 5;
        .threshold = 3;
    }
    .first_byte_timeout     = 300s;
    .connect_timeout        = 10s;
    .between_bytes_timeout  = 5s;
}

sub vcl_pipe {
	# Called upon entering pipe mode.
	# In this mode, the request is passed on to the backend, and any further data from both the client
	# and backend is passed on unaltered until either end closes the connection. Basically, Varnish will
	# degrade into a simple TCP proxy, shuffling bytes back and forth. For a connection in pipe mode,
	# no other VCL subroutine will ever get called after vcl_pipe.
    if (req.http.upgrade) {
        set bereq.http.upgrade = req.http.upgrade;
	    set bereq.http.connection = req.http.connection;
    }
}
sub vcl_recv {
	unset req.http.proxy; # remove the proxy headers

	  # Only deal with "normal" types
	if (req.method != "GET" &&
	    req.method != "HEAD" &&
	    req.method != "PUT" &&
	    req.method != "POST" &&
	    req.method != "TRACE" &&
	    req.method != "OPTIONS" &&
	    req.method != "PATCH" &&
	    req.method != "DELETE") {
	    /* Non-RFC2616 or CONNECT which is weird. */
		return (pipe);
	}

    if (req.url ~ "^/socket.io/") {
        set req.backend_hint = api;
    } else {
        set req.backend_hint = apache;
    }

    # Implementing websocket support (https://varnish-cache.org/docs/trunk/users-guide/vcl-example-websockets.html)
    if (req.http.Upgrade ~ "(?i)websocket") {
        set req.backend_hint = api;
        return (pipe);
    }
    else {
        set req.backend_hint = apache;
    }
}

sub vcl_backend_response {
    # Don't cache 50x responses
    set beresp.http.server = "Try harder";
    if (beresp.status == 500 || beresp.status == 502 || beresp.status == 503 || beresp.status == 504) {
      return (abandon);
    }
    return (deliver);
}

# The routine when we deliver the HTTP request to the user
# Last chance to modify headers that are sent to the client
sub vcl_deliver {
  # Called before a cached object is delivered to the client.
  # Remove some headers: Apache version & OS
  unset resp.http.Server;
  unset resp.http.X-Drupal-Cache;
  unset resp.http.X-Varnish;
  unset resp.http.Via;
  unset resp.http.Link;
  unset resp.http.X-Generator;

  return (deliver);
}

sub vcl_fini {
  # Called when VCL is discarded only after all requests have exited the VCL.
  # Typically used to clean up VMODs.

  return (ok);
}