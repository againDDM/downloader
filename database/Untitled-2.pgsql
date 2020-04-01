
INSERT INTO users (u_name, pass_hash, email) VALUES  ('nobody', '#nohash', 'nobody@nobody');
INSERT INTO users (u_name, pass_hash, email) VALUES  ('noone', '#nohash', 'noone@nobody');
INSERT INTO workers (ip_address, domain_name) VALUES ('192.169.254.31', 'noworker');
INSERT INTO movies VALUES ('ololotrololo', 'TROLOLO-OLOLO-SMOTRETVSEM');
INSERT INTO movies VALUES ('trololoololo', 'TROLOLO-OLOLO-SMOTRETVSEM');
INSERT INTO w_tasks (m_id) VALUES ('trololoololo');
SELECT * FROM movies;
SELECT * FROM workers;
SELECT * FROM users;
SELECT * FROM w_tasks;
SELECT * FROM u_tasks;
SELECT add_u_task(1, 'trololoololo') as status;
SELECT add_u_task(1, 'ololotrololo') as status;