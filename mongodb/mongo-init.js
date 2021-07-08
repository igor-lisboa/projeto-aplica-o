db.createUser(
    {
        user: "root",
        pwd: "root_password",
        roles: [
            {
                role: "readWrite",
                db: "tcc"
            }
        ]
    }
);