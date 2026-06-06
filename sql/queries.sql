-- Total de vendas

SELECT
    SUM(sales) AS total_sales
FROM sales;


-- Vendas por região

SELECT
    region,
    SUM(sales) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;


-- Top produtos

SELECT
    product_name,
    SUM(sales) AS total_sales
FROM sales
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;


-- Vendas por categoria

SELECT
    category,
    SUM(sales) AS total_sales
FROM sales
GROUP BY category
ORDER BY total_sales DESC;


-- Evolução mensal

SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(sales) AS monthly_sales
FROM sales
GROUP BY month
ORDER BY month;