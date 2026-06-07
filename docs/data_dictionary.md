# Data Dictionary

_Source: `data\processed\clean_sales.csv` — rows: 9789_

| Column | Type | Non-null | Null % | Unique values | Sample values |
|---|---:|---:|---:|---:|---:|
| row_id | int64 | 9789 | 0.0% | 9789 | 1, 2, 3, 4, 5 |
| order_id | object | 9789 | 0.0% | 4916 | CA-2017-152156, CA-2017-138688, US-2016-108966, CA-2015-115812, CA-2018-114412 |
| order_date | object | 9789 | 0.0% | 1229 | 2017-11-08, 2017-06-12, 2016-10-11, 2015-06-09, 2018-04-15 |
| ship_date | object | 9789 | 0.0% | 1326 | 2017-11-11, 2017-06-16, 2016-10-18, 2015-06-14, 2018-04-20 |
| ship_mode | object | 9789 | 0.0% | 4 | Second Class, Standard Class, First Class, Same Day |
| customer_id | object | 9789 | 0.0% | 793 | CG-12520, DV-13045, SO-20335, BH-11710, AA-10480 |
| customer_name | object | 9789 | 0.0% | 793 | Claire Gute, Darrin Van Huff, Sean O'Donnell, Brosina Hoffman, Andrew Allen |
| segment | object | 9789 | 0.0% | 3 | Consumer, Corporate, Home Office |
| country | object | 9789 | 0.0% | 1 | United States |
| city | object | 9789 | 0.0% | 529 | Henderson, Los Angeles, Fort Lauderdale, Concord, Seattle |
| state | object | 9789 | 0.0% | 48 | Kentucky, California, Florida, North Carolina, Washington |
| postal_code | float64 | 9789 | 0.0% | 626 | 42420.0, 90036.0, 33311.0, 90032.0, 28027.0 |
| region | object | 9789 | 0.0% | 4 | South, West, Central, East |
| product_id | object | 9789 | 0.0% | 1860 | FUR-BO-10001798, FUR-CH-10000454, OFF-LA-10000240, FUR-TA-10000577, OFF-ST-10000760 |
| category | object | 9789 | 0.0% | 3 | Furniture, Office Supplies, Technology |
| sub_category | object | 9789 | 0.0% | 17 | Bookcases, Chairs, Labels, Tables, Storage |
| product_name | object | 9789 | 0.0% | 1848 | Bush Somerset Collection Bookcase, Hon Deluxe Fabric Upholstered Stacking Chairs, Rounded Back, Self-Adhesive Address Labels for Typewriters by Universal, Bretford CR4500 Series Slim Rectangular Table, Eldon Fold 'N Roll Cart System |
| sales | float64 | 9789 | 0.0% | 5750 | 261.96, 731.94, 14.62, 957.5775, 22.368 |
