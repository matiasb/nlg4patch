
minimal_server.py
-----------------

Simple HTTP server that takes a url param, expecting to be a unified diff file,
and returns the verbalized description of the patch.

Run it with (assuming nlg4patch in your PYTHONPATH):
    $ python minimal_server.py

Example:
    http://localhost:7473/?url=http://hg.python.org/cpython/raw-rev/1b1818fee351

Thanks DrDub (Pablo Duboue).
