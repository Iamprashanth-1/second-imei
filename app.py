
from flask import Flask, render_template, request , redirect
from flask import jsonify
from flask import url_for

app = Flask(__name__)


def sumDig( n ):
    a = 0
    while n > 0:
        a = a + n % 10
        n = int(n / 10)
 
    return a
 
# Returns True if n is valid EMEI
def isValidEMEI(n):
 
    # Converting the number into
    # String for finding length
    s = str(n)
    l = len(s)
 
    # If length is not 15 then IMEI is Invalid
    if l != 15:
        return False
 
    d = 0
    sum = 0
    for i in range(15, 0, -1):
        d = (int)(n % 10)
        if i % 2 == 0:
 
            # Doubling every alternate digit
            d = 2 * d
 
        # Finding sum of the digits
        sum = sum + sumDig(d)
        n = n / 10
    return (sum % 10 == 0)
 
# Driver code

def get_siblings(imei):
    
    try:
        first_imei = int(imei)
        all_siblings = []
        for i in range(first_imei-20,first_imei+20):
            if isValidEMEI(i):
                all_siblings.append(i)
        return all_siblings ,True
    except:
        return "Invalid IMEI number. Please enter a valid IMEI number." ,False

@app.route('/')
def index(all_siblings=None ,error=None):
    all_siblings = request.args.get('all_siblings')
    error = request.args.get('error')
    if all_siblings:
        all_siblings = all_siblings.replace('[','').replace(']','').replace(' ','').split(',')
        return render_template('index.html',all_siblings=all_siblings)
    else:
        all_siblings = []


    return render_template('index.html',all_siblings=list(all_siblings) ,error=error)

@app.route('/get_siblings', methods=['POST'])
def do_magic():
    imei = request.form['imei']
    all_siblings, status = get_siblings(imei)
    if status:
        return redirect(url_for('index', all_siblings=str(all_siblings), ))
        return render_template('index.html', imei=imei, all_siblings=all_siblings)
        return jsonify({'imei': all_siblings})
    else:
        return redirect(url_for('index', error=str(all_siblings), ))
        return jsonify({'error': all_siblings})

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8005)