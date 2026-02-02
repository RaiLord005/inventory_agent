import mysql.connector
import pandas as pd
import math
from dotenv import load_dotenv
import os
# Load the variables from the .env file
load_dotenv()

class InventoryAgent:
    def __init__(self):
        # Database Connection Configuration
        self.config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }

    def fetch_compressed_data(self):
        """Simulates fetching compressed data into a Dataframe for fast processing"""
        conn = mysql.connector.connect(**self.config)
        query = "SELECT * FROM inventory"
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def optimize_stock(self):
        """The 'Reasoning' step where the agent makes decisions"""
        df = self.fetch_compressed_data()
        
        print("\n--- AGENT STOCK OPTIMIZATION REPORT ---")
        for index, row in df.iterrows():
            # Logic: If current stock + what we expect to sell < safety level
            # The agent triggers a reorder.
            
            status = "✅ OPTIMAL"
            action = "No action needed."
            ideal_qty = self.calculate_eoq(
                    row['annual_demand'], 
                    row['order_cost_fixed'], 
                    row['holding_cost_per_unit']
                )
            
            if row['current_stock'] <= row['safety_stock_level']:
                status = "❌ CRITICAL LOW"
                reorder_qty = row['forecasted_demand'] - row['current_stock']
                min_req=row['safety_stock_level']-row['current_stock']
                action = f"ORDER {reorder_qty} units IMMEDIATELY.\nMINIMUM ORDER:{min_req}"
            
            elif row['current_stock'] < row['forecasted_demand']:
                status = "🟡 WARNING"
                reorder_qty = row['forecasted_demand'] - row['current_stock']
                action = f"ORDER {reorder_qty} units for Prepare purchase order for next week."

            print(f"Product: {row['product_name']}")
            print(f"Status: {status}")
            print(f"Agent Recommendation: {action}")
            print(f"EOQ:IDEAL QANTITY: {ideal_qty}")
            print("-" * 40)

    def calculate_eoq(self, annual_demand, order_cost, holding_cost):
        """Standard EOQ formula implementation"""
        if holding_cost == 0: return 0
        eoq = math.sqrt((2 * annual_demand * order_cost) / holding_cost)
        return round(eoq)
    
    def update_stock(self, product_id, quantity_change):
        """
        Edits the current stock in MySQL.
        Use a negative number to 'use' stock (e.g., -5).
        Use a positive number to 'add' stock (e.g., 10).
        """
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        
        # SQL logic: Update the specific product
        sql = "UPDATE inventory SET current_stock = current_stock + %s WHERE product_id = %s"
        cursor.execute(sql, (quantity_change, product_id))
        
        conn.commit() # Important: This saves the change to the database
        conn.close()
        print(f"--- Stock Updated: Product {product_id} changed by {quantity_change} ---")


if __name__ == "__main__":
    agent = InventoryAgent()
    agent.optimize_stock()









# import pandas as pd
# from scripts.db_connection import get_connection # Importing your new file

# class InventoryAgent:
#     def fetch_compressed_data(self):
#         conn = get_connection() # Using the central connection
#         if conn:
#             query = "SELECT * FROM inventory"
#             df = pd.read_sql(query, conn)
#             conn.close()
#             return df
#         else:
#             print("Failed to connect to the brain (database).")
#             return pd.DataFrame()

#     def optimize_stock(self):
#         df = self.fetch_compressed_data()
#         if df.empty:
#             return
            
#         print("\n--- AGENT STOCK OPTIMIZATION REPORT ---")
#         for index, row in df.iterrows():
#             # (Rest of the logic from the previous step goes here...)
#             print(f"Analyzing: {row['product_name']}...")

