INSERT INTO property (title, street_address, city, state, zip, property_type, year_built, sqft_basement, sqft_total, bed, bath, parking, occupancy_status, neighborhood_rating, latitude, longitude, subdivision, layout, pool, basement, highway, train, htw, commercial, water, sewage)
VALUES ('Bright Lakehouse', '1234 Lakeview Dr', 'Austin', 'TX', '73301', 'Single Family', 1999, 500, 3500, 4, 3.5, 'Garage', 'Vacant', 8, 30.2666667, -97.7333300, 'Lakeview', 'Open', FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, TRUE, TRUE);

INSERT INTO valuation (property_id, list_price, zestimate, arv, expected_rent, rent_zestimate, low_fmr, high_fmr, net_yield, irr, selling_reason)
VALUES (1, 500000, 515000, 520000, 3000, 3100, 2900, 3200, 6.5, 12.0, 'Upgrade');

INSERT INTO hoa (property_id, hoa_flag, hoa_value, final_reviewer, underwriting_rehab)
VALUES (1, TRUE, 500, 'Jane Doe', 'Reviewed by Senior Underwriter');

INSERT INTO rehab (property_id, calculation, paint, flooring_flag, foundation_flag, roof_flag, hvac_flag, kitchen_flag, bathroom_flag, appliances_flag, windows_flag, landscaping_flag, trashout_flag)
VALUES (1, '30k needed', TRUE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, TRUE, TRUE, TRUE);

INSERT INTO taxes (property_id, property_taxes, redfin_value, tax_rate)
VALUES (1, 10000, 510000, 0.0250);

INSERT INTO leads (property_id, reviewed_status, most_recent_status, source, market, flood, rent_restricted, seller_retained_broker, school_average)
VALUES (1, 'Reviewed', 'Under Offer', 'Realtor.com', 'Austin Metro', FALSE, FALSE, 'ABC Realty', 'A');
