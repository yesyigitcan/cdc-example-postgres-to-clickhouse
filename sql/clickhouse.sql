-- SETUP
CREATE TABLE dw_currency_postgres(
    id  Nullable(String),
    create_time Nullable(datetime),
    currency_date Nullable(DATE),
    currency_code Nullable(String),
    currency_name Nullable(String),
    value_to_try Nullable(FLOAT)
)
ENGINE = MergeTree()
ORDER BY ();

-- TEST
select id, create_time, currency_date, currency_code, currency_name, value_to_try from clkdb.dw_currency_postgres;
