from flask import Flask,request, url_for, redirect, render_template
import pickle
import joblib
import numpy as np
import os
import re
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer




app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
def getTokens(url):

  # Split by slash (/) and dash (-)
  tokens = re.split('[/-]', url)
  
  for i in tokens:
    # Include the splits extensions and subdomains
    if i.find(".") >= 0:
      dot_split = i.split('.')
      
      # Remove .com and www. since they're too common
      if "com" in dot_split:
        dot_split.remove("com")
      if "www" in dot_split:
        dot_split.remove("www")
      
      tokens += dot_split
      
  return tokens


location = r'C:\Users\Ashwek\Documents\project_final\.env\pkl'

fullpath = os.path.join(location, 'model.pkl')
model = pickle.load(open(fullpath,'rb'))
tVec = joblib.load(os.path.join(location,"tVec.pkl"),'rb')




@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    


    obj = request.form.values()
    i = ''
    for i in obj:
        print("My url is:",i)
        
    xp = model.predict(tVec.transform(getTokens(i)))

    '''''
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    prediction=model.predict(final)
    
    output='{0:.{1}f}'.format(prediction[0][1], 2)

    if output>str(1):
        return render_template('index.html',pred='MALICIOUS URL.\n Probability is {}'.format(output))
    else:
        return render_template('index.html',pred='NOT MALICIOUS.\n Probability is {}'.format(output))

    '''''
    
    return render_template('index.html',pred='NOT MALICIOUS.\n Probability is {}'.format(xp[0]))



if __name__ == '__main__': 
    app.run(debug=True)
