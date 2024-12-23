CREATE TABLE IF NOT EXISTS public."user"
(
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  full_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  user_type VARCHAR(50) NOT NULL,
  is_active boolean NOT NULL
);