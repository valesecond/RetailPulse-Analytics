-- Top 10 Clientes por Vendas
SELECT
    cliente,
    SUM(vendas) AS total_vendas
FROM sales_pt_br
GROUP BY cliente
ORDER BY total_vendas DESC
LIMIT 10;
