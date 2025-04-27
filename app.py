from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, static_folder='static')
df = pd.read_csv('Book2_fixed_v2.csv', encoding='cp932')

@app.route('/', methods=['GET'])
def index():
    us_eu_options = sorted(df['US/EU'].dropna().unique())
    working_shape_options = sorted(df['Working Shape'].dropna().unique())
    max_diameter_options = sorted(df['呼び径'].dropna().unique())
    
    selected_us_eu = request.args.get('us_eu', '')
    selected_shape = request.args.get('working_shape', '')
    selected_max_diameter = request.args.get('max_diameter', '')
    
    filtered = df.copy()
    if selected_us_eu:
        filtered = filtered[filtered['US/EU'] == selected_us_eu]
    if selected_shape:
        filtered = filtered[filtered['Working Shape'] == selected_shape]
    if selected_max_diameter:
        try:
            filtered = filtered[filtered['呼び径'] == float(selected_max_diameter)]
        except ValueError:
            pass

    return render_template('index.html', us_eu_options=us_eu_options,
                           working_shape_options=working_shape_options,
                           max_diameter_options=max_diameter_options,
                           results=filtered.to_dict(orient='records'),
                           selected_us_eu=selected_us_eu,
                           selected_shape=selected_shape,
                           selected_max_diameter=selected_max_diameter)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
