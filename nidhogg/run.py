#!/usr/bin/env python3
from application import create_app

if __name__ == '__main__':
    app = create_app('settings.main')
    app.run(use_reloader=False)
