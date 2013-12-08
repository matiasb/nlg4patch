"""Takes a URL with a unidiff and returns generated text (possibly cached)."""

import SimpleHTTPServer
import SocketServer
import os
import urllib

from nlg4patch.microplanner import microplanning
from nlg4patch.planner import content_planning
from nlg4patch.unidiff import parse_unidiff


PORT = 7473
JOURNAL = dict()


class NLG4PatchServer(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """Minimalist nlg4patch server."""

    def do_GET(self):
        if self.path[0:6] != '/?url=':
            self.send_response(400, 'Missing URL')
            return

        url = self.path[6:]
        text = ""
        if url in JOURNAL:
            text = JOURNAL[url]
        else:
            url_file = urllib.urlopen(url)
            patch_info = parse_unidiff(url_file)
            plan = content_planning(patch_info)
            micro = microplanning(plan)
            for para in micro:
                text += para.realise() + "\n"
            url_file.close()

            with open('journal.log', 'a') as jf2:
                jf2.write(url + '\t' + text.replace("\n","\\n"))
            JOURNAL[url] = text
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(text)


if os.path.exists('journal.log'):
    with open('journal.log') as jf:
        for line in jf:
            (journal_url, journal_text) = line.split("\t")
            JOURNAL[journal_url] = journal_text.replace("\\n", "\n")


HTTPD = SocketServer.ForkingTCPServer(('', PORT), NLG4PatchServer)
print "Try me: http://localhost:%s/?url=http://hg.python.org/cpython/raw-rev/1b1818fee351" % (PORT)
HTTPD.serve_forever()
