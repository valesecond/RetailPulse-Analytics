-- KPI: Número de Pedidos (total acumulado)
SELECT
    COUNT(DISTINCT id_pedido) AS num_pedidos
FROM sales_pt_br;
