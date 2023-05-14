from flask import Flask, jsonify, render_template, request, redirect, url_for
import pandas as pd 
# import json 
# import psycopg2
import pickle
import numpy as np
from sklearn.utils import check_array

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################


# from sqlalchemy import create_engine
# from config import username, password, host, port, database
# connection_string = f'{username}:{password}@{host}:{port}/{database}'
# engine = create_engine(f'postgresql://{connection_string}')



#Flask Route 
@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/page2")
def page2(): 
    return render_template("page2.html")

@app.route("/page3")
def page3(): 
    return render_template("page3.html")


filename = 'model.pkl'
loaded_model = pickle.load(open(filename, 'rb'))

@app.route("/model", methods=["POST"])
def model():
     key = [i for i in request.form.keys()]
     value = [i for i in request.form.values()]
     df = pd.DataFrame([value],columns=key)
     df['RoofMatl']=pd.Categorical(df['RoofMatl'],categories=['WdShngl', 'Metal', 'WdShake', 'Membran', 'Tar&Grv','Roll'])
     df['Condition2']=pd.Categorical(df['Condition2'],categories=['Norm', 'RRNn', 'Feedr', 'PosN', 'PosA', 'RRAn', 'RRAe'])
     df['GarageQual']=pd.Categorical(df['GarageQual'],categories=['TA', 'Fa', 'Gd','Po'])
     df['SaleType']=pd.Categorical(df['SaleType'],categories=['WD', 'New','ConLD', 'ConLI', 'CWD', 'ConLw', 'Con', 'Oth'])
     df['Exterior2nd']=pd.Categorical(df['Exterior2nd'],categories=['VinylSd', 'MetalSd', 'Wd Shng', 'HdBoard', 'Plywood', 'Wd Sdng','CmentBd', 'BrkFace', 'Stucco', 'Brk Cmn', 'ImStucc','AsphShn', 'Stone', 'Other', 'CBlock'])
     df['Exterior1st']=pd.Categorical(df['Exterior1st'],categories=['VinylSd', 'MetalSd', 'Wd Sdng', 'HdBoard', 'BrkFace', 'WdShing','CemntBd', 'Plywood', 'Stucco', 'BrkComm', 'AsphShn','Stone', 'ImStucc', 'CBlock'])
     df['SaleCondition']=pd.Categorical(df['SaleCondition'],categories=['Normal', 'Partial', 'AdjLand', 'Alloca', 'Family'])
     df['RoofStyle']=pd.Categorical(df['RoofStyle'],categories=['Gable', 'Hip', 'Gambrel', 'Mansard','Shed'])
     df['Functional']=pd.Categorical(df['Functional'],categories=['Typ', 'Min1','Min2', 'Mod', 'Maj2', 'Sev'])
     df['Neighborhood']=pd.Categorical(df['Neighborhood'],categories=['Blueste','BrDale', 'BrkSide','ClearCr','CollgCr','Crawfor','Edwards','Gilbert','IDOTRR','MeadowV','Mitchel','NAmes','NPkVill','NWAmes','NoRidge','NridgHt','OldTown','SWISU','Sawyer','SawyerW','Somerst','StoneBr','Timber','Veenker'])
     df1= pd.get_dummies(df, columns=['RoofMatl', 'Condition2','GarageQual','SaleType','Exterior2nd','Exterior1st','SaleCondition','RoofStyle','Functional','Neighborhood'])
     dummies_frame = pd.get_dummies(df1)
     df1.reindex(columns = dummies_frame.columns, fill_value=0)

     prediction = loaded_model.predict(df1)

     prediction = "${0:,.2f}".format(prediction[0])
     print(prediction)

     return render_template("page3.html", prediction = prediction)




@app.route("/prediction")
def prediction():
    df_prediction = pd.read_sql_table(table_name="Prediction", con = engine.connect(), schema ="public")
    df_prediction_json = df_prediction.to_dict(orient="records")
    return jsonify(df_prediction_json)



if __name__ == "__main__":
    app.run(debug=True)
