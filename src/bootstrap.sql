-- DELETE FROM user;
-- DELETE FROM notification;
-- DELETE FROM review_object;
-- DELETE FROM review;

CREATE TABLE IF NOT EXISTS user(
  id integer PRIMARY KEY NOT NULL,
  email text,
  flags numeric,
  created_at_utc text NOT NULL,
  updated_at_utc text NOT NULL);

CREATE TABLE IF NOT EXISTS notification(
  id text PRIMARY KEY NOT NULL,
  type text,
  kv_json text NOT NULL,
  receivers text NOT NULL,
  sender text NOT NULL,
  flags integer,
  created_at_utc text NOT NULL,
  updated_at_utc text NOT NULL);

CREATE TABLE IF NOT EXISTS review_object(
  id integer PRIMARY KEY NOT NULL,
  uri text NOT NULL,
  flags numeric,
  uid integer,
  filename text NOT NULL,
  description text,
  created_at_utc text NOT NULL,
  updated_at_utc text NOT NULL);

CREATE TABLE IF NOT EXISTS comment(
  id integer PRIMARY KEY NOT NULL,
  created_at_utc text NOT NULL,
  body text NOT NULL
);

CREATE TABLE IF NOT EXISTS review(
  id integer PRIMARY KEY NOT NULL,
  flags numeric,
  created_at_utc text NOT NULL,
  review_object_uri text NOT NULL,
  body text NOT NULL,
  uid integer,
  FOREIGN KEY(review_object_uri) REFERENCES review_object(uri)
);

CREATE TABLE IF NOT EXISTS thumbnail(
  id integer PRIMARY KEY NOT NULL,
  flags numeric,
  filename text NOT NULL,
  size_code integer,
  created_at_utc text NOT NULL,
  updated_at_utc text NOT NULL,
  review_object_uri text NOT NULL,
  FOREIGN KEY(review_object_uri) REFERENCES review_object(uri)
);
