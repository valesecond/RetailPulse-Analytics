-- Top 10 Produtos por Vendas
SELECT
    produto,
    SUM(vendas) AS total_vendas
FROM sales_pt_br
GROUP BY produto
ORDER BY total_vendas DESC
LIMIT 10;
