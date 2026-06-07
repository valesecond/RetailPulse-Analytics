-- KPI: Ticket Médio (total acumulado)
SELECT
    SUM(vendas)::float / NULLIF(COUNT(DISTINCT id_pedido),0) AS ticket_medio
FROM sales_pt_br;
