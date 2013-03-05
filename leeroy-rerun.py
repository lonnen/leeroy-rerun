import json
import optparse
import os
import re

import requests

"""
trigger leeroy to build and run a pull request as if it had just been updated.
"""

def _main():
    parser = optparse.OptionParser()
    parser.add_option("-L", "--leeroy-url", dest="leeroy_url",
                      default=os.environ.get("LEEROY_URL"), type="string",
                      help="if unprovided, uses env['LEEROY_URL']")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("what pull request needs rerunning?")
    if not options.leeroy_url:
        parser.error("where is leeroy?")
    pr_url_re = re.compile(r'https?://github.com/([\w-]+)/([\w-]+)/pull/(\d+)')
    for pr in args:
        groups = pr_url_re.match(pr).groups()
        if len(groups) != 3:
            print "invalid url: %s" % pr
            continue
        org, repo, pull_request_number = groups
        base_full_name = "%s/%s" % (org, repo)
        r = requests.get("https://api.github.com/repos/%s/pulls/%s" %
                         (base_full_name, pull_request_number))
        response_json = r.json()
        if 'message' in response_json:
            print 'Message from github: ' + response_json['message']
        if r.headers['X-RateLimit-Remaining'] == '0':
            print 'Rate limiting exceeded. Try again later.'
            return
        head_full_name = response_json['head']['repo']['full_name']
        sha = response_json['head']['sha']
        blob = {
            "type": "SimulatedPullRequestEvent",
            "action": "synchronize",
            "pull_request": {
                "number": pull_request_number,
                "html_url": "https://github.com/%s/pulls/%s" %
                            (base_full_name, pull_request_number),
                "base": {
                    "repo": {
                        "full_name": base_full_name
                    }
                },
                "head": {
                    "repo": {
                        "full_name": head_full_name
                    },
                    "sha": sha
                }
            }
        }
        p = requests.post("%s/notification/github" % options.leeroy_url,
                          data=json.dumps(blob),
                          headers={'content-type': 'application/json'})
        print ('%s - %s' % (p.status_code, pr))


if __name__ == '__main__':
    _main()
