import json
import mysql.connector
import pandas as pd
from decimal import Decimal
import sys
import os
from typing import Dict, List, Any, Optional


class PropertyETL:
    def __init__(self, db_config: Dict[str, str]):
        """Initialize ETL with database configuration."""
        self.db_config = db_config
        self.connection = None
        self.cursor = None
        
    def connect_db(self):
        """Establish database connection."""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            print("Successfully connected to MySQL database")
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            sys.exit(1)
    
    def close_connection(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed")
    
    def load_json_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load JSON data from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            print(f"Loaded {len(data)} property records from {file_path}")
            return data
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            sys.exit(1)
    
    def clean_value(self, value: Any, data_type: str = 'string') -> Any:
        """Clean and convert values based on data type."""
        if value is None or value == 'Null' or value == '' or value == 'null':
            return None
            
        if data_type == 'boolean':
            if isinstance(value, str):
                return value.lower() in ['yes', 'true', '1']
            return bool(value)
        elif data_type == 'decimal':
            try:
                return float(value) if value is not None else None
            except (ValueError, TypeError):
                return None
        elif data_type == 'integer':
            try:
                return int(float(value)) if value is not None else None
            except (ValueError, TypeError):
                return None
        else:
            return str(value).strip() if value is not None else None
    
    def insert_property(self, property_data: Dict[str, Any]) -> int:
        """Insert property record and return property_id."""
        insert_query = """
        INSERT INTO property (
            title, street_address, city, state, zip, property_type, year_built,
            sqft_basement, sqft_total, bed, bath, parking, occupancy_status,
            neighborhood_rating, latitude, longitude, subdivision, layout,
            pool, basement, highway, train, htw, commercial, water, sewage
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            self.clean_value(property_data.get('Property_Title')),
            self.clean_value(property_data.get('Street_Address')),
            self.clean_value(property_data.get('City')),
            self.clean_value(property_data.get('State')),
            self.clean_value(property_data.get('Zip')),
            self.clean_value(property_data.get('Property_Type')),
            self.clean_value(property_data.get('Year_Built'), 'integer'),
            self.clean_value(property_data.get('SQFT_Basement'), 'integer'),
            self.clean_value(property_data.get('SQFT_Total'), 'integer'),
            self.clean_value(property_data.get('Bed'), 'integer'),
            self.clean_value(property_data.get('Bath'), 'decimal'),
            self.clean_value(property_data.get('Parking')),
            self.clean_value(property_data.get('Occupancy')),
            self.clean_value(property_data.get('Neighborhood_Rating'), 'integer'),
            self.clean_value(property_data.get('Latitude'), 'decimal'),
            self.clean_value(property_data.get('Longitude'), 'decimal'),
            self.clean_value(property_data.get('Subdivision')),
            self.clean_value(property_data.get('Layout')),
            self.clean_value(property_data.get('Pool'), 'boolean'),
            self.clean_value(property_data.get('BasementYesNo'), 'boolean'),
            self.clean_value(property_data.get('Highway'), 'boolean'),
            self.clean_value(property_data.get('Train')),
            self.clean_value(property_data.get('HTW'), 'boolean'),
            self.clean_value(property_data.get('Commercial'), 'boolean'),
            self.clean_value(property_data.get('Water')),
            self.clean_value(property_data.get('Sewage'))
        )
        
        self.cursor.execute(insert_query, values)
        return self.cursor.lastrowid
    
    def insert_valuations(self, property_id: int, valuations: List[Dict[str, Any]]):
        """Insert valuation records for a property."""
        insert_query = """
        INSERT INTO valuation (
            property_id, list_price, zestimate, arv, expected_rent,
            rent_zestimate, low_fmr, high_fmr, net_yield, irr, selling_reason
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for valuation in valuations:
            values = (
                property_id,
                self.clean_value(valuation.get('List_Price'), 'decimal'),
                self.clean_value(valuation.get('Zestimate'), 'decimal'),
                self.clean_value(valuation.get('ARV'), 'decimal'),
                self.clean_value(valuation.get('Expected_Rent'), 'decimal'),
                self.clean_value(valuation.get('Rent_Zestimate'), 'decimal'),
                self.clean_value(valuation.get('Low_FMR'), 'decimal'),
                self.clean_value(valuation.get('High_FMR'), 'decimal'),
                None,  # net_yield from property level
                None,  # irr from property level
                None   # selling_reason from property level
            )
            self.cursor.execute(insert_query, values)
    
    def insert_hoa_records(self, property_id: int, hoa_records: List[Dict[str, Any]], property_data: Dict[str, Any]):
        """Insert HOA records for a property."""
        insert_query = """
        INSERT INTO hoa (
            property_id, hoa_flag, hoa_value, final_reviewer, underwriting_rehab
        ) VALUES (%s, %s, %s, %s, %s)
        """
        
        for hoa in hoa_records:
            values = (
                property_id,
                self.clean_value(hoa.get('HOA_Flag'), 'boolean'),
                self.clean_value(hoa.get('HOA'), 'decimal'),
                self.clean_value(property_data.get('Final_Reviewer')),
                None  # underwriting_rehab from rehab section
            )
            self.cursor.execute(insert_query, values)
    
    def insert_rehab_records(self, property_id: int, rehab_records: List[Dict[str, Any]]):
        """Insert rehab records for a property."""
        insert_query = """
        INSERT INTO rehab (
            property_id, calculation, paint, flooring_flag, foundation_flag,
            roof_flag, hvac_flag, kitchen_flag, bathroom_flag, appliances_flag,
            windows_flag, landscaping_flag, trashout_flag
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for rehab in rehab_records:
            values = (
                property_id,
                self.clean_value(rehab.get('Rehab_Calculation')),
                self.clean_value(rehab.get('Paint'), 'boolean'),
                self.clean_value(rehab.get('Flooring_Flag'), 'boolean'),
                self.clean_value(rehab.get('Foundation_Flag'), 'boolean'),
                self.clean_value(rehab.get('Roof_Flag'), 'boolean'),
                self.clean_value(rehab.get('HVAC_Flag'), 'boolean'),
                self.clean_value(rehab.get('Kitchen_Flag'), 'boolean'),
                self.clean_value(rehab.get('Bathroom_Flag'), 'boolean'),
                self.clean_value(rehab.get('Appliances_Flag'), 'boolean'),
                self.clean_value(rehab.get('Windows_Flag'), 'boolean'),
                self.clean_value(rehab.get('Landscaping_Flag'), 'boolean'),
                self.clean_value(rehab.get('Trashout_Flag'), 'boolean')
            )
            self.cursor.execute(insert_query, values)
    
    def insert_taxes(self, property_id: int, property_data: Dict[str, Any]):
        """Insert tax record for a property."""
        insert_query = """
        INSERT INTO taxes (
            property_id, property_taxes, redfin_value, tax_rate
        ) VALUES (%s, %s, %s, %s)
        """
        
        # Get Redfin value from valuations if available
        redfin_value = None
        if 'Valuation' in property_data:
            for val in property_data['Valuation']:
                if 'Redfin_Value' in val:
                    redfin_value = self.clean_value(val['Redfin_Value'], 'decimal')
                    break
        
        values = (
            property_id,
            self.clean_value(property_data.get('Taxes'), 'decimal'),
            redfin_value,
            self.clean_value(property_data.get('Tax_Rate'), 'decimal')
        )
        self.cursor.execute(insert_query, values)
    
    def insert_leads(self, property_id: int, property_data: Dict[str, Any]):
        """Insert leads record for a property."""
        insert_query = """
        INSERT INTO leads (
            property_id, reviewed_status, most_recent_status, source, market,
            flood, rent_restricted, seller_retained_broker, school_average
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            property_id,
            self.clean_value(property_data.get('Reviewed_Status')),
            self.clean_value(property_data.get('Most_Recent_Status')),
            self.clean_value(property_data.get('Source')),
            self.clean_value(property_data.get('Market')),
            self.clean_value(property_data.get('Flood')),
            self.clean_value(property_data.get('Rent_Restricted'), 'boolean'),
            self.clean_value(property_data.get('Seller_Retained_Broker')),
            self.clean_value(property_data.get('School_Average'), 'decimal')
        )
        self.cursor.execute(insert_query, values)
    
    def process_property(self, property_data: Dict[str, Any]) -> int:
        """Process a single property record and all related data."""
        try:
            # Insert main property record
            property_id = self.insert_property(property_data)
            print(f"Inserted property {property_id}: {property_data.get('Property_Title')}")
            
            # Insert related records
            if 'Valuation' in property_data:
                self.insert_valuations(property_id, property_data['Valuation'])
            
            if 'HOA' in property_data:
                self.insert_hoa_records(property_id, property_data['HOA'], property_data)
            
            if 'Rehab' in property_data:
                self.insert_rehab_records(property_id, property_data['Rehab'])
            
            # Always insert taxes and leads (even if some fields are null)
            self.insert_taxes(property_id, property_data)
            self.insert_leads(property_id, property_data)
            
            return property_id
            
        except mysql.connector.Error as err:
            print(f"Database error processing property: {err}")
            self.connection.rollback()
            return None
        except Exception as err:
            print(f"Unexpected error processing property: {err}")
            self.connection.rollback()
            return None
    
    def run_etl(self, json_file_path: str):
        """Main ETL process."""
        print("Starting Property ETL Process...")
        
        # Load data
        property_data = self.load_json_data(json_file_path)
        
        # Connect to database
        self.connect_db()
        
        # Process each property
        processed_count = 0
        error_count = 0
        
        for property_record in property_data:
            property_id = self.process_property(property_record)
            if property_id:
                processed_count += 1
            else:
                error_count += 1
        
        # Commit all changes
        self.connection.commit()
        
        print(f"\nETL Process Complete!")
        print(f"Processed: {processed_count} properties")
        print(f"Errors: {error_count} properties")
        
        # Close connection
        self.close_connection()


def main():
    """Main function to run the ETL script."""
    
    # Database configuration - update these values as needed
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'database': 'home_db',
        'user': 'root',
        'password': '6equj5_root'
    }
    
    # JSON data file path
    json_file_path = 'data/fake_property_data.json'  # Update this path as needed
    
    # Check if file exists
    if not os.path.exists(json_file_path):
        print(f"Error: JSON file {json_file_path} not found")
        print("Please ensure the data file is in the correct location")
        sys.exit(1)
    
    # Run ETL
    etl = PropertyETL(db_config)
    etl.run_etl(json_file_path)


if __name__ == "__main__":
    main()