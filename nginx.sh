#!/bin/bash

export DM_CLOUDFRONT_IPS=$(/app/scripts/get-cloudfront-ips.py)
export DM_RESOLVER_IP=$(awk '/nameserver/{ print $2; exit}' /etc/resolv.conf)

/app/scripts/render-template.py /app/templates/nginx.conf.j2 > /etc/nginx/nginx.conf

if [[ $DM_MODE == 'maintenance' ]]; then
    templates="maintenance healthcheck"
else
    templates="api assets www healthcheck"
fi

for template in $templates; do
    echo "Compiling $template" >&2
    /app/scripts/render-template.py /app/templates/$template.j2 > /etc/nginx/sites-enabled/$template.conf
done

exec /usr/sbin/nginx
