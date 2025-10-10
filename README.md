crowdsupply.com product feeds, aka 'rss feeds'.

Announcement article: https://medium.com/@tedder42/newsfeed-for-crowd-supply-projects-b03730da03d0

The main 'browse' feed: https://dyn.tedder.me/rss/crowdsupply-browse.json

MIT licensed.

## docker-compose

```
  crowdsupply:
    build: ./crowdsupply-feed
    container_name: crowdsupply
    user: nobody
    restart: unless-stopped
    volumes:
    - ./_aws_credentials:/.aws/credentials:ro
    # 21600=6 hours
    command: sh -c 'while true; do python3 scrape-browse.py; echo "scrape done"; sleep 21600; done'
    environment:
    - AWS_SHARED_CREDENTIALS_FILE=/.aws/credentials
```
