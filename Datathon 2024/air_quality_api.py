"""import requests
import json
import pandas as pd

# Define the API endpoint and your API key
API_URL = 'https://aqs.epa.gov/data/api/annualData/byState'
API_KEY = 'bluefrog59'  # Replace with your actual API key
EMAIL = 'cecabagay@gmail.com'  # Your registered email with EPA

# Define parameters for the request
params = {
    'email': EMAIL,
    'key': API_KEY,
    'param': '44201',  # Ozone
    'bdate': '20020101',  # Start date in YYYYMMDD format (Jan 1, 2004)
    'edate': '20021231',  # End date in YYYYMMDD format (Dec 31, 2023)
    'state': '48'  # Texas state code
}

# Send the request to the EPA API
try:
    response = requests.get("https://aqs.epa.gov/data/api/annualData/byState?email=cecabagay@gmail.com&key=bluefrog59&param=44201&bdate=20020101&edate=20021231&state=48")
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json()  # Convert the response to JSON

    # Print the type and structure of the data
    print("Response type:", type(data))
    print("Response content:", data)

    # Access the 'Data' key since it's a list of dictionaries
    if 'Data' in data:
        print("Data retrieved successfully.")
        # Initialize a list to hold records with the specified pollutant standard
        ozone_data = []

        for record in data['Data']:
            # Check for the specific pollutant standard
            if record.get('pollutant_standard') == "Ozone 8-hour 2015":
                ozone_data.append(record)  # Collect the relevant records

        # Convert the list of dictionaries to a DataFrame
        ozone_df = pd.DataFrame(ozone_data)

        # Optionally, display the first few rows of the DataFrame
        print(ozone_df.head())  # Displays the first five rows
        print(f"Total records with 'Ozone 8-hour 2015': {len(ozone_df)}")
    else:
        print("Unexpected response structure. 'Data' missing.")
        
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")

ozone_df.to_csv('ozone_data.csv', index=False)
"""

import requests
import json
import pandas as pd

# Define the API endpoint and your API key
API_URL = 'https://aqs.epa.gov/data/api/annualData/byState'
API_KEY = 'bluefrog59'  # Replace with your actual API key
EMAIL = 'cecabagay@gmail.com'  # Your registered email with EPA

texas_counties_fips = {
    "Anderson": "001",
    "Andrews": "003",
    "Angelina": "005",
    "Aransas": "007",
    "Armstrong": "009",
    "Atascosa": "011",
    "Austin": "013",
    "Bailey": "015",
    "Bandera": "017",
    "Bastrop": "019",
    "Baylor": "021",
    "Bee": "023",
    "Bell": "027",
    "Bexar": "029",
    "Blanco": "031",
    "Borden": "033",
    "Bosque": "035",
    "Bowie": "037",
    "Brazoria": "051",
    "Brazos": "053",
    "Breckenridge": "055",
    "Briscoe": "057",
    "Brooks": "059",
    "Brown": "061",
    "Burleson": "063",
    "Burnet": "065",
    "Caldwell": "067",
    "Calhoun": "069",
    "Callahan": "071",
    "Cameron": "073",
    "Camp": "075",
    "Carson": "077",
    "Cass": "079",
    "Castro": "081",
    "Chambers": "083",
    "Cherokee": "085",
    "Childress": "087",
    "Clay": "089",
    "Cochran": "091",
    "Coke": "093",
    "Coleman": "095",
    "Collin": "097",
    "Collingsworth": "099",
    "Colorado": "101",
    "Comal": "103",
    "Comanche": "105",
    "Concho": "107",
    "Cooke": "109",
    "Coryell": "111",
    "Crosby": "113",
    "Dallam": "115",
    "Dallas": "113",
    "Dawson": "119",
    "DeWitt": "121",
    "Dickens": "123",
    "Dimmit": "125",
    "Donley": "127",
    "Duval": "129",
    "Eastland": "131",
    "Ector": "133",
    "Edwards": "135",
    "Ellis": "137",
    "El Paso": "141",
    "Erath": "143",
    "Falls": "145",
    "Fannin": "147",
    "Fayette": "149",
    "Fisher": "151",
    "Floyd": "153",
    "Foard": "155",
    "Fort Bend": "157",
    "Franklin": "159",
    "Freestone": "161",
    "Frio": "163",
    "Gaines": "165",
    "Galveston": "167",
    "Garza": "169",
    "Gillespie": "171",
    "Glasscock": "173",
    "Goliad": "175",
    "Gonzales": "177",
    "Grayson": "179",
    "Gregg": "181",
    "Grimes": "183",
    "Guadalupe": "185",
    "Hale": "187",
    "Hall": "189",
    "Hamilton": "191",
    "Hansford": "193",
    "Hardeman": "195",
    "Harris": "197",
    "Harrison": "199",
    "Hartley": "201",
    "Haskell": "203",
    "Hays": "205",
    "Henderson": "207",
    "Hidalgo": "209",
    "Hill": "211",
    "Hockley": "213",
    "Hood": "215",
    "Hopkins": "217",
    "Houston": "219",
    "Howard": "221",
    "Hudspeth": "223",
    "Hunt": "225",
    "Hutchinson": "227",
    "Irion": "229",
    "Jack": "231",
    "Jackson": "233",
    "Jasper": "235",
    "Jefferson": "237",
    "Jim Hogg": "239",
    "Jim Wells": "241",
    "Johnson": "243",
    "Karnes": "245",
    "Kaufman": "247",
    "Kendall": "249",
    "Kent": "251",
    "Kerr": "253",
    "Kimble": "255",
    "King": "257",
    "Kinney": "259",
    "Kleberg": "261",
    "Knox": "263",
    "Lamar": "265",
    "Lamb": "267",
    "Lampasas": "269",
    "La Salle": "271",
    "Lavaca": "273",
    "Lee": "275",
    "Leon": "277",
    "Liberty": "279",
    "Limestone": "281",
    "Lipscomb": "283",
    "Live Oak": "285",
    "Llano": "287",
    "Lubbock": "289",
    "Lynn": "291",
    "McCulloch": "293",
    "McLennan": "295",
    "McMullen": "297",
    "Madison": "299",
    "Marion": "301",
    "Martin": "303",
    "Mason": "305",
    "Matagorda": "307",
    "Maverick": "309",
    "Medina": "311",
    "Menard": "313",
    "Midland": "315",
    "Milam": "317",
    "Mills": "319",
    "Mitchell": "321",
    "Montague": "323",
    "Montgomery": "325",
    "Moore": "327",
    "Nacogdoches": "329",
    "Navarro": "331",
    "Newton": "333",
    "Nolan": "335",
    "Nueces": "337",
    "Ochiltree": "339",
    "Oldham": "341",
    "Orange": "343",
    "Palo Pinto": "345",
    "Panola": "347",
    "Parker": "349",
    "Parmer": "351",
    "Pecos": "353",
    "Polk": "355",
    "Potter": "357",
    "Presidio": "359",
    "Rains": "361",
    "Randall": "363",
    "Reagan": "365",
    "Real": "367",
    "Red River": "369",
    "Reeves": "371",
    "Richardson": "373",
    "Runnels": "375",
    "Rusk": "377",
    "Sabine": "379",
    "San Augustine": "381",
    "San Jacinto": "383",
    "San Patricio": "385",
    "San Saba": "387",
    "Schleicher": "389",
    "Scurry": "391",
    "Shackelford": "393",
    "Shelby": "395",
    "Sherman": "397",
    "Smith": "399",
    "Somervell": "401",
    "Starr": "403",
    "Stephens": "405",
    "Sterling": "407",
    "Stonewall": "409",
    "Sutton": "411",
    "Swisher": "413",
    "Tarrant": "415",
    "Taylor": "417",
    "Terrell": "419",
    "Throckmorton": "421",
    "Titus": "423",
    "Tom Green": "425",
    "Travis": "427",
    "Trinity": "429",
    "Tyler": "431",
    "Upshur": "433",
    "Uvalde": "435",
    "Val Verde": "437",
    "Van Zandt": "439",
    "Victoria": "441",
    "Walker": "443",
    "Waller": "445",
    "Washington": "447",
    "Webb": "449",
    "Wharton": "451",
    "Wheeler": "453",
    "Williamson": "455",
    "Wilson": "457",
    "Winkler": "495",
    "Wise": "497",
    "Wood": "499",
    "Yoakum": "501",
    "Young": "503",
    "Zapata": "505",
    "Zavala": "507"
}

# Initialize a list to collect results
results = []

# Loop through each county to get data
for county_name, fips in texas_counties_fips.items():
    # Define the parameters for the API request
    params = {
        'email': EMAIL,
        'key': API_KEY,
        'param': '44201',  # Ozone
        'bdate': '20020101',
        'edate': '20021231',
        'state': '48',  # Texas state code
        'county': fips
    }
    
    # Send the request to the EPA API
    try:
        response = requests.get("https://aqs.epa.gov/data/api/annualData/byCounty", params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()  # Convert the response to JSON
        
        # Check if 'Data' key is present
        if 'Data' in data:
            # Filter the records for the desired pollutant standard
            filtered_data = [record for record in data['Data'] if record.get('pollutant_standard') == "Ozone 8-hour 2015"]
            results.extend(filtered_data)
        else:
            print(f"No data found for {county_name}.")
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for {county_name}: {http_err}")
    except Exception as err:
        print(f"An error occurred for {county_name}: {err}")

# Create a DataFrame from the results
ozone_data_df = pd.DataFrame(results)

# Display the DataFrame
print(ozone_data_df.head())

ozone_data_df.to_csv('ozone_data_tx_2002.csv', index=False)