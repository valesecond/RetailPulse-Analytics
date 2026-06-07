CREATE OR REPLACE VIEW vw_sales_by_region AS
SELECT
    region,
    SUM(sales) AS total_sales
FROM sales
GROUP BY region;


CREATE OR REPLACE VIEW vw_sales_by_category AS
SELECT
    category,
    SUM(sales) AS total_sales
FROM sales
GROUP BY category;


CREATE OR REPLACE VIEW vw_monthly_sales AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(sales) AS monthly_sales
FROM sales
GROUP BY month
ORDER BY month;


-- Portuguese views for the translated dataset
CREATE OR REPLACE VIEW vw_vendas_mensais AS
SELECT
    DATE_TRUNC('month', data_pedido) AS mes,
    SUM(vendas) AS vendas_mensais
FROM sales_pt_br
GROUP BY mes
ORDER BY mes;


CREATE OR REPLACE VIEW vw_vendas_por_categoria AS
SELECT
    categoria,
    SUM(vendas) AS total_vendas
FROM sales_pt_br
GROUP BY categoria;


CREATE OR REPLACE VIEW vw_vendas_por_regiao AS
SELECT
    regiao,
    SUM(vendas) AS total_vendas
FROM sales_pt_br
GROUP BY regiao;