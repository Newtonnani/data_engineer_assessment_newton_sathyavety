CREATE TABLE IF NOT EXISTS property (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20),
    property_type VARCHAR(50),
    year_built INT,
    sqft_basement INT,
    sqft_total INT,
    bed INT,
    bath DECIMAL(3,1),
    parking VARCHAR(50),
    occupancy_status VARCHAR(50),
    neighborhood_rating INT,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    subdivision VARCHAR(100),
    layout VARCHAR(100),
    pool BOOLEAN,
    basement BOOLEAN,
    highway VARCHAR(100),
    train VARCHAR(100),
    htw BOOLEAN,
    commercial VARCHAR(100),
    water VARCHAR(100),
    sewage VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS valuation (
    valuation_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    list_price DECIMAL(15,2),
    zestimate DECIMAL(15,2),
    arv DECIMAL(15,2),
    expected_rent DECIMAL(15,2),
    rent_zestimate DECIMAL(15,2),
    low_fmr DECIMAL(15,2),
    high_fmr DECIMAL(15,2),
    net_yield DECIMAL(5,2),
    irr DECIMAL(5,2),
    selling_reason VARCHAR(100),
    CONSTRAINT fk_valuation_property FOREIGN KEY (property_id) REFERENCES property(property_id)
);

CREATE TABLE IF NOT EXISTS hoa (
    hoa_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    hoa_flag BOOLEAN,
    hoa_value DECIMAL(10,2),
    final_reviewer VARCHAR(100),
    underwriting_rehab VARCHAR(100),
    CONSTRAINT fk_hoa_property FOREIGN KEY (property_id) REFERENCES property(property_id)
);

CREATE TABLE IF NOT EXISTS rehab (
    rehab_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    calculation VARCHAR(100),
    paint BOOLEAN,
    flooring_flag BOOLEAN,
    foundation_flag BOOLEAN,
    roof_flag BOOLEAN,
    hvac_flag BOOLEAN,
    kitchen_flag BOOLEAN,
    bathroom_flag BOOLEAN,
    appliances_flag BOOLEAN,
    windows_flag BOOLEAN,
    landscaping_flag BOOLEAN,
    trashout_flag BOOLEAN,
    CONSTRAINT fk_rehab_property FOREIGN KEY (property_id) REFERENCES property(property_id)
);

CREATE TABLE IF NOT EXISTS taxes (
    taxes_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    property_taxes DECIMAL(12,2),
    redfin_value DECIMAL(15,2),
    tax_rate DECIMAL(6,4),
    CONSTRAINT fk_taxes_property FOREIGN KEY (property_id) REFERENCES property(property_id)
);

CREATE TABLE IF NOT EXISTS leads (
    leads_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    reviewed_status VARCHAR(50),
    most_recent_status VARCHAR(100),
    source VARCHAR(100),
    market VARCHAR(100),
    flood VARCHAR(100),
    rent_restricted BOOLEAN,
    seller_retained_broker VARCHAR(100),
    school_average VARCHAR(20),
    CONSTRAINT fk_leads_property FOREIGN KEY (property_id) REFERENCES property(property_id)
);
