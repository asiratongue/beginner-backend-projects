from flask import Flask, request, render_template

app = Flask(__name__)

# Function to handle weight conversions
def weightConv(value, convert_from, convert_to):
    unit_list = {
        'milligram': 0.001,
        'gram': 1,
        'kilogram': 1000,
        'ounce': 28.3,
        'pound': 453.6
    }
    gram_value = float(value) * float(unit_list[convert_from])
    result = float(gram_value) * float(1 / unit_list[convert_to])
    return result

# Function to handle temperature conversions
def tempConv(value, convert_from, convert_to):

    if convert_from == 'Celsuis':
        fahrenheit_value = (float(value) * 1.8) + 32
    elif convert_from == 'Fahrenheit':
        fahrenheit_value = float(value)
    elif convert_from == 'Kelvin':
        fahrenheit_value = ((float(value) - 273.15) * 1.8) + 32

    if convert_to == 'Celsuis':
        result = (fahrenheit_value - 32) / 1.8
    elif convert_to == 'Fahrenheit':
        result = fahrenheit_value
    elif convert_to == 'Kelvin':
        result = ((fahrenheit_value - 32) / 1.8) + 273.15
    return result

# Function to handle length conversions
def lengthConv(value, convert_from, convert_to):
    unit_list = {
        'millimeter': 0.001,
        'centimeter': 0.01,
        'meter': 1,
        'kilometer': 1000,
        'inch': 0.0254,
        'foot': 0.3048,
        'yard': 0.9144,
        'mile': 1609.34
    }
    meter_value = float(value) * float(unit_list[convert_from])
    result = float(meter_value) * float(1 / unit_list[convert_to])
    return result


# Routes and views
@app.route('/')
def home():
    return render_template('length_converter.html')

@app.route('/weighthome')
def weight_home():
    return render_template('weight_converter.html')

@app.route('/convertweight', methods=['POST', 'GET'])
def weight_convert():
    value = request.form['Weight']
    ConvertFrom = request.form['convert_from_W']
    ConvertTo = request.form['convert_to_W']

    final_value = weightConv(value, ConvertFrom, ConvertTo)

    if final_value == 1.0:
        result_statement = f"{final_value} {ConvertTo}"  
    else:
       result_statement = f"{final_value} {ConvertTo}'s" 

    return render_template('weight_converter.html', value=value, ConvertFrom=ConvertFrom, ConvertTo=ConvertTo, 
                            result_statement = result_statement)

@app.route('/temperaturehome')
def temperature_home():
    return render_template('temperature_converter.html')

@app.route('/converttemperature', methods=['POST', 'GET'])
def temperature_convert():
    value = request.form['Temperature']
    ConvertFrom = request.form['convert_from_T']
    ConvertTo = request.form['convert_to_T']
    final_value = tempConv(value, ConvertFrom, ConvertTo)
    result_statement = f"{final_value} {ConvertTo}"  

    return render_template('temperature_converter.html', value=value, ConvertFrom=ConvertFrom, ConvertTo=ConvertTo, result_statement=result_statement)

@app.route('/convertlength', methods=['POST'])
def length_convert():
    value = request.form['Length']
    ConvertFrom = request.form['convert_from']
    ConvertTo = request.form['convert_to']

    final_value = lengthConv(value, ConvertFrom, ConvertTo)

    if final_value == 1.0:
        result_statement = f"{final_value} {ConvertTo}"  
    elif ConvertTo == 'inch':
        result_statement = f"{final_value} {ConvertTo}es"
    else:
       result_statement = f"{final_value} {ConvertTo}'s" 

    return render_template('length_converter.html', value=value, ConvertFrom=ConvertFrom, ConvertTo=ConvertTo, result_statement=result_statement)


if __name__ == '__main__':
    app.run(debug=True)  