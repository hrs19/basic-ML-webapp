from flask import Flask, render_template, flash, redirect, request, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import FileField
import pandas as pd
import os
from flask_uploads import configure_uploads, DATA, UploadSet
import folium
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('Pickle_SVC_Model.pkl','rb'))

name = 'default'

class MyForm(FlaskForm):
    file = FileField('file')

# Upload file module 
app.config["UPLOADED_FILES_DEST"] = "/Harshit/Accenture/work-practice-project/basic-ML-webapp/uploads"
app.config["UPLOADED_FILES_ALLOW"] = ["CSV"]
app.config["SECRET_KEY"] = 'secret'

# def allowed_files(filename):
#     if not "." in filename:
#         return False
#     ext = filename.split(".",1)[1]

#     if ext.upper() in app.config["UPLOADED_FILES_DEST"]:
#         return True
#     else:
#         return False
files = UploadSet('files', DATA)
configure_uploads(app, files)

@app.route('/', methods=['GET','POST'])
def index():

    form = MyForm()
    title = 'Home'
    if form.validate_on_submit():
        print()
        filename = files.save(form.file.data)
        name = filename
        flash("File saved.") #Ensure thsi workss
        #print(filename)

        return redirect(url_for('model_predict', name=filename))


    return render_template("index.html", title=title, form=form)

@app.route('/model_predict/<name>')
def model_predict(name):
    
    print(name)
    df = pd.read_csv(f'uploads/{name}')
    #print(df.head())
    os.remove(f'uploads/{name}')
    # l = (len(data))
    df =  predict(df)
    headings = list(df[:0])
    data = list(df.to_records(index=False))
    name = name.split(".",1)[0]
    df.to_csv(f'downloads/{name}-result.csv')


    return render_template('model_predict.html', headings=headings, data=data, name=str(name))

def predict(df):
    final_features = []
    prediction = []
    data = list(df.to_records(index=False))
    for i in range(len(data)):

        x =  [np.array(list(data[i]))]
        final_features.append(x)
        y = model.predict(final_features[i])
        prediction.append(y)
        
        #print(f'Result {prediction[i]}')
    df['prediction']=prediction
    return df

# @app.route('/download')
# def download():
#     return render_template('')

@app.route('/return-files/<filename>')
def return_files_tut(filename):#name):
    #filename = filename+'-result.csv'
    file_path = 'downloads/' + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


@app.route('/disp_map')
def disp_map():
    title = 'Map Visualization'
    start_coords = (19.076090, 72.877426)
    folium_map = folium.Map(location=start_coords, zoom_start=12)
    folium_map.save('templates/map1.html')    
    start_coords = (19.218330, 72.978088)
    folium_map = folium.Map(location=start_coords, zoom_start=12)
    folium_map.save('templates/map2.html')
    map_name = ["Mumbai","Thane"]        
    return render_template("disp_map.html",map_name = map_name, title=title)







if __name__ == '__main__':
    app.run(debug=True)