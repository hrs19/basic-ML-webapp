from flask import Flask, render_template, flash, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import FileField
import pandas as pd
import os
from flask_uploads import configure_uploads, DATA, UploadSet
import folium
import pickle
app = Flask(__name__)

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
        flash("File saved.") 
        #print(filename)

        return redirect(url_for('model_predict', name=filename))


    return render_template("index.html", title=title, form=form)

@app.route('/model_predict/<name>')
def model_predict(name):
    print(name)
    df = pd.read_csv(f'uploads/{name}')
    #print(df.head())
    os.remove(f'uploads/{name}')
    headings = list(df[:0])
    data = list(df.to_records(index=False))
    print(data[0])
    return render_template('model_predict.html', headings=headings, data=data)



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