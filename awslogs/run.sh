#!/bin/sh

sed -i -e "s/{DM_ENVIRONMENT}/$DM_ENVIRONMENT/g" -e "s/{DM_APP_NAME}/$DM_APP_NAME/g" /etc/awslogs.conf

# nohup because we want awslogs to keep running when everything else is stopping - see supervisord.conf
exec nohup /usr/local/bin/aws logs push --region eu-west-1 --config-file /etc/awslogs.conf
