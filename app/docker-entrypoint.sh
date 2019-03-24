#!/bin/bash
python3 manage.py migrate

# Start Gunicorn processes
if [ "$STAGE" = "production" ] ; then
    python3 manage.py collectstatic --no-input
    
    # Prepare log files and start outputting logs to stdout
    touch /srv/logs/gunicorn.log
    touch /srv/logs/access.log
    tail -n 0 -f /srv/logs/*.log &

    echo "Running production server..."
    exec gunicorn config.wsgi -b 0.0.0.0:8000 \
        --name stavanet
        --workers 3 \
        --log-level=info \
        --log-file=/srv/logs/gunicorn.log \
        --access-logfile=/srv/logs/access.log
else
    echo "Running development server: $@"
    exec "$@"
fi