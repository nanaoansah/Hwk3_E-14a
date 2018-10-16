DROP TABLE IF EXISTS users;
CREATE TABLE users (
    uid serial NOT NULL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users (username, password) VALUES ('u_alpha', '1234');
INSERT INTO users (username, password) VALUES ('u_beta', '1234');

DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    pid serial NOT NULL PRIMARY KEY,
    author serial NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (author) REFERENCES users(uid)
);

INSERT INTO posts (author, content) VALUES (1, 'test alpha post_1');
INSERT INTO posts (author, content) VALUES (2, 'test beta post_2');

DROP TABLE IF EXISTS followers;
CREATE TABLE followers (
    fid serial NOT NULL PRIMARY KEY,
    follower_id serial NOT NULL,
    followed_id serial NOT NULL,
    FOREIGN KEY (follower_id) REFERENCES users(uid),
    FOREIGN KEY (followed_id) REFERENCES users(uid)
);
