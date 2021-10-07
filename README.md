It is a API where you can create a user user using "\register" route use the postman script, which is provided for testing.
And you can login by providing the email and password of that user you created. The password will be save in the hashed form in the database, Use my database url and MongoDB compas to see how your datas are stored.
You can use the "\templates" for careating the post of the user you are logedin.
And by the same route you can get all the post you are made.(of that partcular user your are logged in).You can't get any post of any other user.
You can also view, update, delete the particular post by using "\templates\<templates_id>" route.
