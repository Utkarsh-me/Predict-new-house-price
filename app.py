from flask import Flask, request, render_template
from supabase import create_client , Client
import pickle
import numpy as np

app = Flask(__name__)


# Supabase credentials
SUPABASE_URL = "https://ivarjhpbeasabwwtmvnx.supabase.co"  # Add your Supabase URL here
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml2YXJqaHBiZWFzYWJ3d3Rtdm54Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4MjA3NDksImV4cCI6MjA1MzM5Njc0OX0.ZxUCDNIPBWLjJuN71fc7xlTdplOqNGRI2JPPpEjfW9U"  # Add your Supabase Service Role Key here

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

model = pickle.load(open('house_price.pkl', 'rb'))


@app.route('/')
def index():
    return render_template('new_house_land.html') # Ensure your HTML file is named index.html


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    try :
        if request.method == "POST":
            posted_by = (request.form['posted_by'])
            under_construction = (request.form['under_construction'])
            bhk_no = (request.form['bhk_no'])
            bhk_or_rk = (request.form['bhk_or_rk'])
            square_ft = (request.form['square_ft'])
            ready_to_move = (request.form['ready_to_move'])
            resale = (request.form['resale'])
            longitude = (request.form['longitude'])
            latitude = (request.form['latitude'])
        
             # Prepare input data for the model
            arr = np.array([[posted_by, under_construction, bhk_no, bhk_or_rk, square_ft, ready_to_move, resale, longitude, latitude]])
            prediction = model.predict(arr)


            data = {
                'posted_by' : posted_by,
                'under_construction' : under_construction,
                'bhk_no' : bhk_no,
                'bhk_or_rk' : bhk_or_rk,
                'square_ft' : square_ft,
                'ready_to_move' : ready_to_move,
                'resale' : resale,
                'longitude' : longitude,
                'latitude' : latitude,
                'predicted_price': float(prediction[0])
            }
            response = supabase.table("house_price_prediction").insert(data).execute()

        return render_template('new_house_res.html', prediction=prediction)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)

