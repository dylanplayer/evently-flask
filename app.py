from distutils.log import debug
from event_app import app

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=8000)