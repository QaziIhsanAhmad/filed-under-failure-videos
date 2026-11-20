explain (analyze, buffers off, timing on) select id, status, total_pence, created_at from orders where customer_id = 4217 order by created_at desc limit 20;
