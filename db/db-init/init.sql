CREATE TABLE IF NOT EXISTS quotes (
                                      id SERIAL PRIMARY KEY,
                                      quote TEXT NOT NULL,
                                      name TEXT NOT NULL,
                                      year TEXT NOT NULL,
                                      first_found TIMESTAMP NOT NULL
);
