"""Main module"""

import os
import uvicorn


if __name__ == '__main__':
    # Set hash seed and restart interpreter.
    # This will be done only once if the env var is clear.
    if not os.environ.get('PYTHONHASHSEED'):
        os.environ['PYTHONHASHSEED'] = '1234'

    uvicorn.run(
        'app.routes:app',
        host='localhost',
        port=5000,
        reload=True
    )
