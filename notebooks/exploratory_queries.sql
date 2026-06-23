SELECT COUNT(*) FROM companies;

SELECT COUNT(*) FROM profitandloss;

SELECT COUNT(*) FROM balancesheet;

SELECT COUNT(*) FROM cashflow;

SELECT COUNT(*) FROM analysis;

SELECT COUNT(*) FROM documents;

SELECT COUNT(*) FROM prosandcons;

SELECT company_id, COUNT(*)
FROM profitandloss
GROUP BY company_id
ORDER BY COUNT(*) DESC
LIMIT 10;

SELECT company_id, year, sales, net_profit
FROM profitandloss
LIMIT 10;

SELECT company_id, year, total_assets, total_liabilities
FROM balancesheet
LIMIT 10;