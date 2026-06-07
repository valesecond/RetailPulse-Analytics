CREATE TABLE sales (

    row_id INTEGER,
    order_id VARCHAR(50),

    order_date DATE,
    ship_date DATE,

    ship_mode VARCHAR(50),

    customer_id VARCHAR(50),
    customer_name VARCHAR(255),

    segment VARCHAR(50),

    country VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),

    postal_code VARCHAR(20),

    region VARCHAR(50),

    product_id VARCHAR(50),

    category VARCHAR(100),
    sub_category VARCHAR(100),

    product_name TEXT,

    sales NUMERIC
);

CREATE TABLE sales_pt_br (

    id_linha INTEGER,
    id_pedido VARCHAR(50),

    data_pedido DATE,
    data_envio DATE,

    modo_envio VARCHAR(50),

    id_cliente VARCHAR(50),
    nome_cliente VARCHAR(255),

    segmento VARCHAR(50),

    pais VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(100),

    codigo_postal VARCHAR(20),

    regiao VARCHAR(50),

    id_produto VARCHAR(50),

    categoria VARCHAR(100),
    subcategoria VARCHAR(100),

    nome_produto TEXT,

    vendas NUMERIC
);