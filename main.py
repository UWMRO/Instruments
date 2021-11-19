from flask import Flask, render_template

app = Flask(__name__)

from evora.evora import Evora 

try:
    from evora.andor import andor
except(ImportError):
    print("COULD NOT GET DRIVERS/SDK, STARTING IN DUMMY MODE")
    # TODO: add dummy server if necessary

@app.route('/')
def index():
    evora = Evora()
    tempData = evora.getTemp()
    return render_template('index.html', tempData=tempData)


# REMEMBER: localhost:5000/temperature
@app.route('/temperature')
def route_temperature():
    return Evora().getTemp()


if __name__ == '__main__':
    app.run()
