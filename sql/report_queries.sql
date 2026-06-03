-- 1. Customers with multiple vehicles

SELECT c.name,
       COUNT(v.vehicle_id) AS total_vehicles
FROM customers c
JOIN vehicles v
ON c.customer_id = v.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(v.vehicle_id) > 1;


-- 2. Total service revenue

SELECT SUM(service_cost) AS total_revenue
FROM service_requests;


-- 3. Vehicles with highest number of services

SELECT v.vehicle_number,
       COUNT(s.service_id) AS total_services
FROM vehicles v
JOIN service_requests s
ON v.vehicle_id = s.vehicle_id
GROUP BY v.vehicle_id, v.vehicle_number
ORDER BY total_services DESC;


-- 4. Monthly service report

SELECT strftime('%Y-%m', service_date) AS month,
       COUNT(*) AS total_services,
       SUM(service_cost) AS revenue
FROM service_requests
GROUP BY strftime('%Y-%m', service_date);


-- 5. Pending service requests

SELECT *
FROM service_requests
WHERE status = 'Pending';


-- 6. Rank customers by service spending

SELECT
    customer_name,
    total_spent,
    RANK() OVER (ORDER BY total_spent DESC) AS spending_rank
FROM (
    SELECT
        c.name AS customer_name,
        SUM(s.service_cost) AS total_spent
    FROM customers c
    JOIN vehicles v
        ON c.customer_id = v.customer_id
    JOIN service_requests s
        ON v.vehicle_id = s.vehicle_id
    GROUP BY c.customer_id, c.name
) ranked_customers;
