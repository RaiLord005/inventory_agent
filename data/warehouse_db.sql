CREATE DATABASE IF NOT EXISTS WarehouseDB;
USE WarehouseDB;

CREATE TABLE inventory (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    current_stock INT,
    safety_stock_level INT,
    forecasted_demand INT,
    lead_time_days INT
);
ALTER TABLE inventory 
ADD COLUMN annual_demand INT,
ADD COLUMN order_cost_fixed DECIMAL(10,2), -- Cost to place one order (shipping, admin)
ADD COLUMN holding_cost_per_unit DECIMAL(10,2); -- Cost to store one unit for a year
-- Sample Data for your Agent to analyze

INSERT INTO inventory 
(product_id, product_name, current_stock, safety_stock_level, forecasted_demand, lead_time_days, annual_demand, order_cost_fixed, holding_cost_per_unit)
VALUES 
(1, 'Warm White Wall Paint', 45, 20, 100, 5, 1200, 50.00, 3.00),    -- Healthy
(2, 'Slate Grey External Paint', 8, 15, 60, 7, 500, 45.00, 3.00),   -- 🔴 Critical Low
(3, 'Natural Oak Flooring', 150, 100, 300, 14, 2400, 150.00, 0.50), -- High Order Cost
(4, 'Polished Brass Handle', 12, 25, 50, 10, 400, 25.00, 1.20),     -- 🔴 Critical Low
(5, 'Smart Light Switch', 18, 15, 40, 3, 300, 30.00, 2.00),         -- 🟡 Medium Warning
(6, 'Copper Extension Wire', 60, 20, 100, 4, 800, 40.00, 4.50),     -- Healthy
(7, 'Eco-Friendly Primer', 22, 20, 50, 5, 600, 40.00, 2.50),        -- 🟡 Medium Warning
(8, 'Zinc Screws (500pk)', 15, 40, 500, 2, 5000, 10.00, 0.10),      -- 🔴 Critical / High Demand
(9, 'Luxury Vinyl Tiles', 500, 100, 200, 21, 1800, 150.00, 0.40),   -- Overstocked
(10, 'Stainless Steel Hinge', 35, 30, 80, 6, 1200, 20.00, 0.80);    -- 🟡 Medium Warning

-- drop table inventory;
select * from inventory;
