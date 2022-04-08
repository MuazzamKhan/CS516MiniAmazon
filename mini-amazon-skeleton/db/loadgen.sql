\COPY Users FROM '../generated/Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:

SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);
                         
\COPY Sellers FROM '../generated/Sellers.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Products FROM '../generated/Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);
                         
\COPY Orders FROM '../generated/Orders.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Purchases FROM '../generated/Purchases.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Inventory FROM '../generated/Inventory.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Cart FROM '../generated/Cart.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Reviews FROM '../generated/Reviews.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Reviews_sellers FROM '../generated/Reviews_sellers.csv' WITH DELIMITER ',' NULL '' CSV
