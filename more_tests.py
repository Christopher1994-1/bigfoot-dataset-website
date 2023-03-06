# @app.route('/individual_case')
# def individual_case():
#     months = {
#     "01":"January",
#     "02":"February",
#     "03":"March",
#     "04":"April",
#     "05":"May",
#     "06":"June",
#     "07":"July",
#     "08":"August",
#     "09":"September",
#     "10":"October",
#     "11":"November",
#     "12":"December",
#     }
#     # value = str(value_get[0]).split('.')[0]
    
#     # original_value = value_get[0]
#     # state = state_selected[0]
#     # county = county_selected[0]
#     # image = images[state]
    
#     # rows = one_case(state, county, original_value)
#     # print(state_selected)
#     # print(county_selected)
#     # print(value_get)
#     # class_ = rows[0]['classification'] # pass this

#     # date = str(rows[0]['date']).split('-')

#     # YEAR = date[0] # pass this
#     # MONTH = months[date[1]] # pass this
#     # DAY = date[2] # pass this


#     # observed = rows[0]['observed'] # pass this


#     # season = rows[0]['season'] # pass this

#     # lat = rows[0]['latitude'] # pass this
#     # lon = rows[0]['longitude'] # pass this
#     # summary = rows[0]['summary'] # pass this
#     # location_details = rows[0]['location_details'] # pass this
#     # witness_date = f"{MONTH} {DAY} {YEAR}" # pass this
    
    
    
    
#     return render_template('individual_case.html' 
#                         #    value=value,
#                         #    original_value=original_value,
#                         #    state=state,
#                         #    county=county,
#                         #    image=image,
#                         #    class_=class_,
#                         #    year=YEAR,
#                         #    month=MONTH,
#                         #    day=DAY,
#                         #    observed=observed,
#                         #    season=season,
#                         #    lat=lat,
#                         #    lon=lon,
#                         #    summary=summary,
#                         #    location_details=location_details,
#                         #    witness_date=witness_date,
#                 )