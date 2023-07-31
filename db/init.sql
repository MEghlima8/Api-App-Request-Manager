CREATE TABLE users (
    id SERIAL PRIMARY KEY ,
    username VARCHAR (50) UNIQUE NOT NULL ,
    password VARCHAR (50) NOT NULL ,
    email VARCHAR (255) UNIQUE NOT NULL ,
    token VARCHAR (255) ,
    active bool ,
    confirm_link VARCHAR (255)
);

CREATE TABLE request (
    id SERIAL PRIMARY KEY ,
    user_id INT NOT NULL ,
    type VARCHAR (50) NOT NULL ,
    params JSONB NOT NULL ,
    time VARCHAR (255) ,
    agent VARCHAR (255) ,
    method VARCHAR (50) ,
    ip VARCHAR (255) ,
    status VARCHAR (50) ,
    api_req_id INT ,
    result JSONB ,
    uuid VARCHAR (255) ,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
