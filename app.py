from flask import Flask, render_template, jsonify
import sys
import os

# Ensure Python looks in the scripts folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from scripts.inventory_agent import InventoryAgent

app = Flask(__name__)
agent = InventoryAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/inventory')
def get_inventory():
    try:
        df = agent.fetch_compressed_data()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/advise')
def get_advice():
    try:
        df = agent.fetch_compressed_data()
        recommendations = []
        for _, row in df.iterrows():
            if row['current_stock'] <= row['safety_stock_level']:
                # Running your EOQ logic
                status = "❌ CRITICAL LOW"
                reorder_qty = row['forecasted_demand'] - row['current_stock']
                min_req=row['safety_stock_level']-row['current_stock']
                action = f"ORDER {reorder_qty} units IMMEDIATELY._______MINIMUM ORDER:{min_req}"
                eoq = agent.calculate_eoq(row['annual_demand'], row['order_cost_fixed'], row['holding_cost_per_unit'])
                recommendations.append({
                    "product": row['product_name'],
                    "current": int(row['current_stock']),
                    "recommendation": f"   {status}:   {action}:________ideal EOQ:{eoq}"
                })
            
            elif row['current_stock'] < row['forecasted_demand']:
                status = "🟡 WARNING"
                reorder_qty = row['forecasted_demand'] - row['current_stock']
                action = f"ORDER {reorder_qty} units for Prepare purchase order for next week."
                eoq = agent.calculate_eoq(row['annual_demand'], row['order_cost_fixed'], row['holding_cost_per_unit'])
                recommendations.append({
                    "product": row['product_name'],
                    "current": int(row['current_stock']),
                    "recommendation": f"   {status}:   {action}:_________ideal EOQ:{eoq}"
                })

        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)