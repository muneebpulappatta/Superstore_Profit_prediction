from email import message
from unicodedata import category
from flask import Flask, request, render_template
import numpy as np
import pickle

app = Flask(__name__) 
model=pickle.load(open('model.pkl','rb'))
@app.route('/')
def home():
    title = 'Superstore Profit Prediction'
    return render_template('home3.html', title=title)


@app.route('/predict', methods=['POST'])
def predict():

    requests = [ str(x) for x in request.form.values()]
    print(list(request.form.values()))

    sales = float(request.values['sales'])
    Discount =( float(request.values['discount']))/100
    shipping_cost = float(request.values['shipping'])
    
    
    segment= request.form['Segment']
    print({f"segment is {segment}"})

    if(segment=='Consumer'):
        Segment_Consumer=1
        Segment_Corporate=0
        Segment_HomeOffice=0
    elif(segment=='Corporate'):
        Segment_Consumer=0
        Segment_Corporate=1
        Segment_HomeOffice=0
    else:
        Segment_Consumer=0
        Segment_Corporate=0
        Segment_HomeOffice=1
            
    category= request.form['Category']
    print({f"category is {category}"})

    if(category=='Furniture'):
        Category_Furniture=1
        Category_OfficeSupplies=0
        Category_Technology=0
    elif(category=='Office Supplies'):
        Category_Furniture=0
        Category_OfficeSupplies=1
        Category_Technology=0
    else:
        Category_Furniture	=0
        Category_OfficeSupplies=0
        Category_Technology=1

    
    input_data = np.array([[sales,Discount,shipping_cost,Segment_Consumer,Segment_Corporate,Segment_HomeOffice,
    Category_Furniture,Category_OfficeSupplies,Category_Technology]])

    # print(f"input Sales = {sales}")
    # print(f"input Discount = {Discount}")
    # print(f"input Shipping Cost = {shipping_cost}")
    # print(f"input Segment_Consumer = {Segment_Consumer}")
    # print(f"input Segment_Corporate = {Segment_Corporate}")
    # print(f"input Segment_HomeOffice = {Segment_HomeOffice}")
    # print(f"input Category_Furniture = {Category_Furniture}")
    # print(f"input Category_OfficeSupplies = {Category_OfficeSupplies}")
    # print(f"input Category_Technology = {Category_Technology}")

   
    output=model.predict(input_data)
    print(f"output from model is {output}")
    output=round(output.item(),3)

    if output > 0:
        return render_template('home3.html',prediction_text_positive="The profit is ($){}".format(output))
    else:
         return render_template('home3.html',prediction_text_negative="The profit is ($){}".format(output))
    
   #return render_template('home3.html',prediction_text="The profit is ($){}".format(output))

if __name__=='__main__':
    app.run(host="0.0.0.0", port=9090, debug=True)