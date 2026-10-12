<!-- Source: https://docs.app.barge-master.com/autoapi/PyBM/marine/tools/api/oauth_session/index.html -->

# PyBM.marine.tools.api.oauth_session

Created by CVE, 05-11-2025, together with Copilot \<3

Handles API authentication for Barge Master API with Authentik OAuth2/OIDC.

Uses browser-based OAuth2 flow with PKCE. No hardcoded credentials. Tokens are cached locally. See OAUTH2_SETUP_GUIDE.md for setup instructions.

## Attributes

|                                                                                                                           |     |
|---------------------------------------------------------------------------------------------------------------------------|-----|
| [`CLIENT_ID`](#PyBM.marine.tools.api.oauth_session.CLIENT_ID "PyBM.marine.tools.api.oauth_session.CLIENT_ID")             |     |
| [`AUTHENTIK_URL`](#PyBM.marine.tools.api.oauth_session.AUTHENTIK_URL "PyBM.marine.tools.api.oauth_session.AUTHENTIK_URL") |     |
| [`API_BASE_URL`](#PyBM.marine.tools.api.oauth_session.API_BASE_URL "PyBM.marine.tools.api.oauth_session.API_BASE_URL")    |     |

## Classes

|                                                                                                                                                   |                                  |
|---------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| [`TokenCache`](#PyBM.marine.tools.api.oauth_session.TokenCache "PyBM.marine.tools.api.oauth_session.TokenCache")                                  |                                  |
| [`OAuth2CallbackHandler`](#PyBM.marine.tools.api.oauth_session.OAuth2CallbackHandler "PyBM.marine.tools.api.oauth_session.OAuth2CallbackHandler") | HTTP request handler base class. |

## Functions

|                                                                                                                                                                                      |                                                                                      |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| [`_get_oauth_config`](#PyBM.marine.tools.api.oauth_session._get_oauth_config "PyBM.marine.tools.api.oauth_session._get_oauth_config")()                                              | Fetch OAuth2 config from API server (allows updating Client ID without code changes) |
| [`_find_available_port`](#PyBM.marine.tools.api.oauth_session._find_available_port "PyBM.marine.tools.api.oauth_session._find_available_port")(\[start_port, max_attempts\])         | Find an available port starting from start_port                                      |
| [`_do_oauth2_flow`](#PyBM.marine.tools.api.oauth_session._do_oauth2_flow "PyBM.marine.tools.api.oauth_session._do_oauth2_flow")()                                                    | Execute OAuth2 authorization code flow with PKCE                                     |
| [`_exchange_code_for_token`](#PyBM.marine.tools.api.oauth_session._exchange_code_for_token "PyBM.marine.tools.api.oauth_session._exchange_code_for_token")(code, code_verifier, ...) | Exchange authorization code for access token                                         |
| [`get_authenticated_session`](#PyBM.marine.tools.api.oauth_session.get_authenticated_session "PyBM.marine.tools.api.oauth_session.get_authenticated_session")()                      | Get authenticated session using OAuth2 (browser-based, tokens cached locally)        |

## Module Contents

PyBM.marine.tools.api.oauth_session.CLIENT_ID[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  

&nbsp;

PyBM.marine.tools.api.oauth_session.AUTHENTIK_URL[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  

&nbsp;

PyBM.marine.tools.api.oauth_session.API_BASE_URL* = 'https://api.app.barge-master.com'*[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  

&nbsp;

PyBM.marine.tools.api.oauth_session.\_get_oauth_config()[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  
Fetch OAuth2 config from API server (allows updating Client ID without code changes)

&nbsp;

*class *PyBM.marine.tools.api.oauth_session.TokenCache[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  
cache_file[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  

save(*token_data*)[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  

load()[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  

&nbsp;

*class *PyBM.marine.tools.api.oauth_session.OAuth2CallbackHandler(*request*, *client_address*, *server*)[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  
Bases: `http.server.BaseHTTPRequestHandler`

HTTP request handler base class.

The following explanation of HTTP serves to guide you through the code as well as to expose any misunderstandings I may have about HTTP (so you don’t need to read the code to figure out I’m wrong :-).

HTTP (HyperText Transfer Protocol) is an extensible protocol on top of a reliable stream transport (e.g. TCP/IP). The protocol recognizes three parts to a request:

1.  One line identifying the request type and path

2.  An optional set of RFC-822-style headers

3.  An optional data part

The headers and data are separated by a blank line.

The first line of the request has the form

\<command\> \<path\> \<version\>

where \<command\> is a (case-sensitive) keyword such as GET or POST, \<path\> is a string containing path information for the request, and \<version\> should be the string “HTTP/1.0” or “HTTP/1.1”. \<path\> is encoded using the URL encoding scheme (using %xx to signify the ASCII character with hex code xx).

The specification specifies that lines are separated by CRLF but for compatibility with the widest range of clients recommends servers also handle LF. Similarly, whitespace in the request line is treated sensibly (allowing multiple spaces between components and allowing trailing whitespace).

Similarly, for output, lines ought to be separated by CRLF pairs but most clients grok LF characters just fine.

If the first line of the request has the form

\<command\> \<path\>

(i.e. \<version\> is left out) then this is assumed to be an HTTP 0.9 request; this form has no optional headers and data part and the reply consists of just the data.

The reply form of the HTTP 1.x protocol again has three parts:

1.  One line giving the response code

2.  An optional set of RFC-822-style headers

3.  The data

Again, the headers and data are separated by a blank line.

The response code line has the form

\<version\> \<responsecode\> \<responsestring\>

where \<version\> is the protocol version (“HTTP/1.0” or “HTTP/1.1”), \<responsecode\> is a 3-digit response code indicating success or failure of the request, and \<responsestring\> is an optional human-readable string explaining what the response code means.

This server parses the request and the headers, and then calls a function specific to the request type (\<command\>). Specifically, a request SPAM will be handled by a method do_SPAM(). If no such method exists the server sends an error response to the client. If it exists, it is called with no arguments:

do_SPAM()

Note that the request name is case sensitive (i.e. SPAM and spam are different requests).

The various request details are stored in instance variables:

- client_address is the client IP address in the form (host,

port);

- command, path and version are the broken-down request line;

- headers is an instance of email.message.Message (or a derived

class) containing the header information;

- rfile is a file object open for reading positioned at the

start of the optional input data part;

- wfile is a file object open for writing.

IT IS IMPORTANT TO ADHERE TO THE PROTOCOL FOR WRITING!

The first thing to be written must be the response line. Then follow 0 or more header lines, then a blank line, and then the actual data (if any). The meaning of the header lines depends on the command executed by the server; in most cases, when data is returned, there should be at least one header line of the form

Content-type: \<type\>/\<subtype\>

where \<type\> and \<subtype\> should be registered MIME types, e.g. “text/html” or “text/plain”.

result* = None*[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  

do_GET()[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  

log_message(*\*args*)[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  
Log an arbitrary message.

This is used by all other logging functions. Override it if you have specific logging wishes.

The first argument, FORMAT, is a format string for the message to be logged. If the format string contains any % escapes requiring parameters, they should be specified as subsequent arguments (it’s just like printf!).

The client ip and current date/time are prefixed to every message.

Unicode control characters are replaced with escaped hex before writing the output to stderr.

&nbsp;

PyBM.marine.tools.api.oauth_session.\_find_available_port(*start_port=8080*, *max_attempts=10*)[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  
Find an available port starting from start_port

&nbsp;

PyBM.marine.tools.api.oauth_session.\_do_oauth2_flow()[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  
Execute OAuth2 authorization code flow with PKCE

&nbsp;

PyBM.marine.tools.api.oauth_session.\_exchange_code_for_token(*code*, *code_verifier*, *redirect_uri*, *token_endpoint*, *client_id*)[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  
Exchange authorization code for access token

&nbsp;

PyBM.marine.tools.api.oauth_session.get_authenticated_session()[](../../../../../../../source-code/PyBM/marine/tools/api/oauth_session.py)  
Get authenticated session using OAuth2 (browser-based, tokens cached locally)
