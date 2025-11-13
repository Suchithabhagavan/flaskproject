# application.py
"""
Run the FlaskWebProject application.
"""

from os import environ
from FlaskWebProject import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    # Use HTTPS locally only; Azure App Service handles SSL automatically
    use_ssl = environ.get('USE_ADHOC_SSL', 'false').lower() in ('true', '1', 'yes')

    if use_ssl:
        app.run(host=HOST, port=PORT, ssl_context='adhoc')
    else:
        app.run(host=HOST, port=PORT)
