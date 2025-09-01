from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
import pandas as pd
import os
from datetime import datetime
import json

app = Flask(__name__)

# Configure caching
cache_config = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes
}
app.config.from_mapping(cache_config)
cache = Cache(app)

# Global cache for CSV data
_csv_data_cache = None
_csv_last_modified = None

# Load CSV data with caching
def load_data_from_csv():
    global _csv_data_cache, _csv_last_modified
    
    try:
        csv_path = "LLC Data.csv"
        if not os.path.exists(csv_path):
            # Return sample data if CSV doesn't exist
            return pd.DataFrame({
                'name': ['Sample LLC Service', 'Business Formation Pro', 'Legal Services LLC'],
                'us_state': ['CA', 'NY', 'TX'],
                'city': ['Los Angeles', 'New York', 'Houston'],
                'full_address': ['123 Business St, Los Angeles, CA', '456 Corporate Ave, New York, NY', '789 Enterprise Blvd, Houston, TX'],
                'phone': ['555-0101', '555-0202', '555-0303'],
                'rating': [4.5, 4.8, 4.2],
                'reviews': [25, 42, 18]
            })
        
        # Check if file has been modified
        current_modified = os.path.getmtime(csv_path)
        
        # Return cached data if file hasn't changed
        if _csv_data_cache is not None and _csv_last_modified == current_modified:
            return _csv_data_cache
        
        # Load and cache new data
        df = pd.read_csv(csv_path)
        df = df.dropna(subset=['us_state', 'city', 'full_address'])
        
        _csv_data_cache = df
        _csv_last_modified = current_modified
        
        return df
        
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

# Get unique states
def get_states():
    df = load_data_from_csv()
    if not df.empty:
        return sorted(df['us_state'].unique())
    return []

# Get cities for a state
def get_cities_for_state(state):
    df = load_data_from_csv()
    if not df.empty:
        # Convert state abbreviation to full name if needed
        full_state_name = STATE_MAPPING.get(state, state)
        
        # Try exact match first
        state_data = df[df['us_state'] == full_state_name]
        
        # If no results, try case-insensitive match
        if state_data.empty:
            state_data = df[df['us_state'].str.contains(full_state_name, case=False, na=False)]
        
        return sorted(state_data['city'].unique())
    return []

# Get city count for a state
def get_city_count_for_state(state):
    cities = get_cities_for_state(state)
    return len(cities)

# Get top cities by population (top 50)
def get_top_cities():
    # Top 50 US cities by population
    top_cities = [
        {'name': 'New York', 'state': 'NY', 'population': '8,804,190'},
        {'name': 'Los Angeles', 'state': 'CA', 'population': '3,898,747'},
        {'name': 'Chicago', 'state': 'IL', 'population': '2,746,388'},
        {'name': 'Houston', 'state': 'TX', 'population': '2,304,580'},
        {'name': 'Phoenix', 'state': 'AZ', 'population': '1,608,139'},
        {'name': 'Philadelphia', 'state': 'PA', 'population': '1,603,797'},
        {'name': 'San Antonio', 'state': 'TX', 'population': '1,434,625'},
        {'name': 'San Diego', 'state': 'CA', 'population': '1,386,932'},
        {'name': 'Dallas', 'state': 'TX', 'population': '1,304,379'},
        {'name': 'San Jose', 'state': 'CA', 'population': '1,013,240'},
        {'name': 'Austin', 'state': 'TX', 'population': '978,908'},
        {'name': 'Jacksonville', 'state': 'FL', 'population': '949,611'},
        {'name': 'Fort Worth', 'state': 'TX', 'population': '918,915'},
        {'name': 'Columbus', 'state': 'OH', 'population': '898,553'},
        {'name': 'Charlotte', 'state': 'NC', 'population': '885,708'},
        {'name': 'San Francisco', 'state': 'CA', 'population': '873,965'},
        {'name': 'Indianapolis', 'state': 'IN', 'population': '887,642'},
        {'name': 'Seattle', 'state': 'WA', 'population': '744,955'},
        {'name': 'Denver', 'state': 'CO', 'population': '727,211'},
        {'name': 'Washington', 'state': 'DC', 'population': '689,545'},
        {'name': 'Boston', 'state': 'MA', 'population': '675,647'},
        {'name': 'El Paso', 'state': 'TX', 'population': '678,815'},
        {'name': 'Nashville', 'state': 'TN', 'population': '689,447'},
        {'name': 'Detroit', 'state': 'MI', 'population': '674,841'},
        {'name': 'Oklahoma City', 'state': 'OK', 'population': '681,054'},
        {'name': 'Portland', 'state': 'OR', 'population': '652,503'},
        {'name': 'Las Vegas', 'state': 'NV', 'population': '651,319'},
        {'name': 'Memphis', 'state': 'TN', 'population': '651,073'},
        {'name': 'Louisville', 'state': 'KY', 'population': '633,045'},
        {'name': 'Baltimore', 'state': 'MD', 'population': '585,708'},
        {'name': 'Milwaukee', 'state': 'WI', 'population': '590,157'},
        {'name': 'Albuquerque', 'state': 'NM', 'population': '564,559'},
        {'name': 'Tucson', 'state': 'AZ', 'population': '542,629'},
        {'name': 'Fresno', 'state': 'CA', 'population': '542,107'},
        {'name': 'Sacramento', 'state': 'CA', 'population': '513,624'},
        {'name': 'Mesa', 'state': 'AZ', 'population': '504,258'},
        {'name': 'Kansas City', 'state': 'MO', 'population': '508,090'},
        {'name': 'Atlanta', 'state': 'GA', 'population': '498,715'},
        {'name': 'Long Beach', 'state': 'CA', 'population': '466,742'},
        {'name': 'Colorado Springs', 'state': 'CO', 'population': '478,961'},
        {'name': 'Raleigh', 'state': 'NC', 'population': '474,069'},
        {'name': 'Miami', 'state': 'FL', 'population': '442,241'},
        {'name': 'Virginia Beach', 'state': 'VA', 'population': '449,974'},
        {'name': 'Omaha', 'state': 'NE', 'population': '486,051'},
        {'name': 'Oakland', 'state': 'CA', 'population': '440,646'},
        {'name': 'Minneapolis', 'state': 'MN', 'population': '429,954'},
        {'name': 'Tulsa', 'state': 'OK', 'population': '413,066'},
        {'name': 'Arlington', 'state': 'TX', 'population': '398,112'},
        {'name': 'Tampa', 'state': 'FL', 'population': '384,959'},
        {'name': 'New Orleans', 'state': 'LA', 'population': '383,997'},
        {'name': 'Wichita', 'state': 'KS', 'population': '397,532'},
        {'name': 'Cleveland', 'state': 'OH', 'population': '372,624'},
        {'name': 'Bakersfield', 'state': 'CA', 'population': '403,455'},
        {'name': 'Aurora', 'state': 'CO', 'population': '386,261'},
        {'name': 'Anaheim', 'state': 'CA', 'population': '346,824'},
        {'name': 'Honolulu', 'state': 'HI', 'population': '350,964'},
        {'name': 'Santa Ana', 'state': 'CA', 'population': '310,227'},
        {'name': 'Corpus Christi', 'state': 'TX', 'population': '326,586'},
        {'name': 'Riverside', 'state': 'CA', 'population': '314,998'},
        {'name': 'Lexington', 'state': 'KY', 'population': '322,570'},
        {'name': 'Stockton', 'state': 'CA', 'population': '320,804'},
        {'name': 'Henderson', 'state': 'NV', 'population': '320,189'},
        {'name': 'Newark', 'state': 'NJ', 'population': '311,549'},
        {'name': 'Saint Paul', 'state': 'MN', 'population': '307,193'},
        {'name': 'St. Louis', 'state': 'MO', 'population': '301,578'},
        {'name': 'Chandler', 'state': 'AZ', 'population': '275,987'},
        {'name': 'Greensboro', 'state': 'NC', 'population': '299,035'},
        {'name': 'Anchorage', 'state': 'AK', 'population': '291,247'},
        {'name': 'Plano', 'state': 'TX', 'population': '285,494'},
        {'name': 'Lincoln', 'state': 'NE', 'population': '289,102'},
        {'name': 'Orlando', 'state': 'FL', 'population': '307,573'},
        {'name': 'Irvine', 'state': 'CA', 'population': '307,670'},
        {'name': 'Newark', 'state': 'NJ', 'population': '311,549'},
        {'name': 'Durham', 'state': 'NC', 'population': '283,506'},
        {'name': 'Chula Vista', 'state': 'CA', 'population': '275,487'},
        {'name': 'Toledo', 'state': 'OH', 'population': '275,116'},
        {'name': 'Fort Wayne', 'state': 'IN', 'population': '267,927'},
        {'name': 'St. Petersburg', 'state': 'FL', 'population': '258,308'},
        {'name': 'Laredo', 'state': 'TX', 'population': '261,639'},
        {'name': 'Jersey City', 'state': 'NJ', 'population': '292,449'},
        {'name': 'Chandler', 'state': 'AZ', 'population': '275,987'},
        {'name': 'Madison', 'state': 'WI', 'population': '258,366'},
        {'name': 'Lubbock', 'state': 'TX', 'population': '257,141'},
        {'name': 'Scottsdale', 'state': 'AZ', 'population': '241,361'},
        {'name': 'Reno', 'state': 'NV', 'population': '255,601'},
        {'name': 'Buffalo', 'state': 'NY', 'population': '255,284'},
        {'name': 'Gilbert', 'state': 'AZ', 'population': '267,918'},
        {'name': 'Glendale', 'state': 'AZ', 'population': '248,325'},
        {'name': 'North Las Vegas', 'state': 'NV', 'population': '251,974'},
        {'name': 'Winston-Salem', 'state': 'NC', 'population': '249,545'},
        {'name': 'Chesapeake', 'state': 'VA', 'population': '244,835'},
        {'name': 'Norfolk', 'state': 'VA', 'population': '238,005'},
        {'name': 'Fremont', 'state': 'CA', 'population': '230,504'},
        {'name': 'Garland', 'state': 'TX', 'population': '239,928'},
        {'name': 'Irving', 'state': 'TX', 'population': '239,798'},
        {'name': 'Hialeah', 'state': 'FL', 'population': '223,109'},
        {'name': 'Richmond', 'state': 'VA', 'population': '226,610'},
        {'name': 'Boise', 'state': 'ID', 'population': '235,684'},
        {'name': 'Spokane', 'state': 'WA', 'population': '228,989'},
        {'name': 'Baton Rouge', 'state': 'LA', 'population': '225,374'}
    ]
    return top_cities[:50]  # Return top 50

# Get businesses for a state
def get_businesses_for_state(state):
    df = load_data_from_csv()
    if not df.empty:
        # Convert state abbreviation to full name if needed
        full_state_name = STATE_MAPPING.get(state, state)
        
        # Try exact match first
        state_data = df[df['us_state'] == full_state_name]
        
        # If no results, try case-insensitive match
        if state_data.empty:
            state_data = df[df['us_state'].str.contains(full_state_name, case=False, na=False)]
        
        return state_data.to_dict('records')
    return []

# State name to abbreviation mapping
STATE_MAPPING = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'DC': 'District Of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
    'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
    'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
    'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska',
    'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
    'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
    'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# Get businesses for a city
def get_businesses_for_city(state, city):
    df = load_data_from_csv()
    if not df.empty:
        # Convert state abbreviation to full name if needed
        full_state_name = STATE_MAPPING.get(state, state)
        
        # Try exact match first
        city_data = df[(df['us_state'] == full_state_name) & (df['city'] == city)]
        
        # If no results, try case-insensitive match
        if city_data.empty:
            city_data = df[
                (df['us_state'].str.contains(full_state_name, case=False, na=False)) & 
                (df['city'].str.contains(city, case=False, na=False))
            ]
        
        # If still no results, try partial city name match
        if city_data.empty:
            city_data = df[
                (df['us_state'].str.contains(full_state_name, case=False, na=False)) & 
                (df['city'].str.contains(city.split()[0], case=False, na=False))
            ]
        
        return city_data.to_dict('records')
    return []

@app.route('/')
@cache.cached(timeout=300)  # Cache for 5 minutes
def index():
    states = get_states()
    
    # Get city counts for each state
    state_data = []
    for state in states:
        city_count = get_city_count_for_state(state)
        state_data.append({
            'name': state,
            'city_count': city_count
        })
    
    # Get top cities by population
    top_cities = get_top_cities()
    
    # Get some featured businesses
    df = load_data_from_csv()
    featured_businesses = []
    if not df.empty:
        featured_businesses = df.head(6).to_dict('records')
    
    return render_template('index.html', 
                         states=state_data, 
                         top_cities=top_cities,
                         featured_businesses=featured_businesses)

@app.route('/state/<state>')
def state_page(state):
    businesses = get_businesses_for_state(state)
    cities = get_cities_for_state(state)
    
    return render_template('state.html', 
                         state=state, 
                         businesses=businesses, 
                         cities=cities)

@app.route('/city/<state>/<city>')
def city_page(state, city):
    businesses = get_businesses_for_city(state, city)
    
    return render_template('city.html', 
                         state=state, 
                         city=city, 
                         businesses=businesses)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/locations')
@cache.cached(timeout=300)  # Cache for 5 minutes
def locations():
    # Get all states with their cities
    all_states = get_states()
    states_data = []
    total_cities = 0
    
    for state in all_states:
        cities = get_cities_for_state(state)
        total_cities += len(cities)
        
        # Get state abbreviation from mapping
        state_abbreviation = None
        for abbrev, full_name in STATE_MAPPING.items():
            if full_name == state:
                state_abbreviation = abbrev
                break
        
        states_data.append({
            'name': state,
            'abbreviation': state_abbreviation or state,
            'cities': cities
        })
    
    # Sort states alphabetically
    states_data.sort(key=lambda x: x['name'])
    
    # Create alphabet for quick navigation
    alphabet = [chr(i) for i in range(65, 91)]  # A-Z
    
    return render_template('locations.html', 
                         states=states_data, 
                         total_cities=total_cities,
                         alphabet=alphabet)



@app.route('/sitemap.xml')
def sitemap():
    states = get_states()
    df = load_data_from_csv()
    
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add main pages with proper priorities
    main_pages = [
        ('', '1.0', 'weekly'),
        ('/about', '0.8', 'monthly'),
        ('/contact', '0.8', 'monthly'),
        ('/privacy', '0.5', 'yearly'),
        ('/locations', '0.9', 'weekly')
    ]
    
    for page, priority, changefreq in main_pages:
        sitemap_content += f'  <url>\n'
        sitemap_content += f'    <loc>https://www.baronllc.online{page}</loc>\n'
        sitemap_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap_content += f'    <changefreq>{changefreq}</changefreq>\n'
        sitemap_content += f'    <priority>{priority}</priority>\n'
        sitemap_content += f'  </url>\n'
    
    # Add state pages
    for state in states:
        sitemap_content += f'  <url>\n'
        sitemap_content += f'    <loc>https://www.baronllc.online/state/{state}</loc>\n'
        sitemap_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap_content += f'    <changefreq>weekly</changefreq>\n'
        sitemap_content += f'    <priority>0.8</priority>\n'
        sitemap_content += f'  </url>\n'
        
        # Add city pages
        cities = get_cities_for_state(state)
        for city in cities:
            sitemap_content += f'  <url>\n'
            sitemap_content += f'    <loc>https://www.baronllc.online/city/{state}/{city}</loc>\n'
            sitemap_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
            sitemap_content += f'    <changefreq>weekly</changefreq>\n'
            sitemap_content += f'    <priority>0.7</priority>\n'
            sitemap_content += f'  </url>\n'
    
    sitemap_content += '</urlset>'
    
    return app.response_class(sitemap_content, mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    robots_content = """User-agent: *
Allow: /

Sitemap: https://www.baronllc.online/sitemap.xml"""
    return app.response_class(robots_content, mimetype='text/plain')

@app.route('/api/states')
def api_states():
    states = get_states()
    return jsonify(states)

@app.route('/api/cities/<state>')
def api_cities(state):
    cities = get_cities_for_state(state)
    return jsonify(cities)

@app.route('/api/businesses/<state>')
def api_businesses_state(state):
    businesses = get_businesses_for_state(state)
    return jsonify(businesses)

@app.route('/api/businesses/<state>/<city>')
def api_businesses_city(state, city):
    businesses = get_businesses_for_city(state, city)
    return jsonify(businesses)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
