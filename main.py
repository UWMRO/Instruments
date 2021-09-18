from flask import Flask
app = Flask(__name__)

# REMEMBER: localhost:<port>/temperature
@app.route('/temperature')
def route_temperature():
    andor_temp = 0 # add something here to output the actual temperature
    # limitation: does not update realtime
    return '{} F'.format(andor_temp)
