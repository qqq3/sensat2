#!/usr/bin/zsh

curl -u alex_kun:J5aJuzm9KXGZVZy "https://scihub.copernicus.eu/dhus/search?format=json&start=0&rows=100&q=(footprint%3A%22Intersects%28POLYGON%28%2829.167019796646976%2052.130895289942316%2C29.080014001016778%2052.166487293313594%2C29.030933808609998%2052.11445861460109%2C29.140248782606918%2052.09733063120845%2C29.167019796646976%2052.130895289942316%2C29.167019796646976%2052.130895289942316%29%29%29%22%29%20AND%20%28%20beginPosition%3A%5B2018-01-01T00%3A00%3A00.000Z%20TO%202018-09-25T23%3A59%3A59.999Z%5D%20AND%20endPosition%3A%5B2018-01-01T00%3A00%3A00.000Z%20TO%202018-09-25T23%3A59%3A59.999Z%5D%20%29%20AND%20%28%20%28platformname%3ASentinel-2%20AND%20producttype%3AS2MSI2A%20AND%20cloudcoverpercentage%3A%5B0%20TO%207%5D%29)" -o search_result