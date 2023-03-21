make sure to delete www.neverssl.com before, to test functionality

to run the proxy server:  python3 ProxyServer.py

to request a webpage through our proxy server, use the link http://localhost:8888/www.neverssl.com

The proxy server runs on port 8888. The proxy server creates a saved copy of a webpage the first time it's visited, then on all subsequent requests the proxy server sends back the saved copy of the webpage. This increases performance.