import pandas as pd

def clean_data(df):

    df.columns = (
        df.columns
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Converter datas
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        format="%d/%m/%Y"
    )

    df["ship_date"] = pd.to_datetime(
        df["ship_date"],
        format="%d/%m/%Y"
    )

    df = df.dropna()

    return df


def translate_to_pt_br(df):

    translated_df = df.copy()

    translated_df = translated_df.rename(
        columns={
            "row_id": "id_linha",
            "order_id": "id_pedido",
            "order_date": "data_pedido",
            "ship_date": "data_envio",
            "ship_mode": "modo_envio",
            "customer_id": "id_cliente",
            "customer_name": "nome_cliente",
            "segment": "segmento",
            "country": "pais",
            "city": "cidade",
            "state": "estado",
            "postal_code": "codigo_postal",
            "region": "regiao",
            "product_id": "id_produto",
            "category": "categoria",
            "sub_category": "subcategoria",
            "product_name": "nome_produto",
            "sales": "vendas",
        }
    )

    translated_df["modo_envio"] = translated_df["modo_envio"].replace(
        {
            "Standard Class": "Classe padrao",
            "Second Class": "Segunda classe",
            "First Class": "Primeira classe",
            "Same Day": "Mesmo dia",
        }
    )

    translated_df["segmento"] = translated_df["segmento"].replace(
        {
            "Consumer": "Consumidor",
            "Corporate": "Corporativo",
            "Home Office": "Home office",
        }
    )

    translated_df["pais"] = translated_df["pais"].replace(
        {
            "United States": "Estados Unidos",
        }
    )

    translated_df["regiao"] = translated_df["regiao"].replace(
        {
            "South": "Sul",
            "West": "Oeste",
            "Central": "Centro",
            "East": "Leste",
        }
    )

    translated_df["categoria"] = translated_df["categoria"].replace(
        {
            "Furniture": "Moveis",
            "Office Supplies": "Material de escritorio",
            "Technology": "Tecnologia",
        }
    )

    translated_df["subcategoria"] = translated_df["subcategoria"].replace(
        {
            "Bookcases": "Estantes",
            "Chairs": "Cadeiras",
            "Tables": "Mesas",
            "Furnishings": "Mobiliario",
            "Labels": "Etiquetas",
            "Storage": "Armazenamento",
            "Art": "Arte",
            "Binders": "Pastas",
            "Appliances": "Eletrodomesticos",
            "Paper": "Papel",
            "Phones": "Telefones",
            "Fasteners": "Fixadores",
            "Accessories": "Acessorios",
            "Envelopes": "Envelopes",
            "Supplies": "Suprimentos",
            "Machines": "Maquinas",
            "Copiers": "Copiadoras",
        }
    )

    return translated_df