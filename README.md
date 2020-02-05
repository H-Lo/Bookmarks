Your task, should you choose to accept it, is to create a bookmarking application with these properties:

1. Multiple users, can create an account on the system by themselves.
2. Users can create, edit or delete private or public bookmarks.
	- the mandatory bookmark structure is:
		1. description
		2. bookmark link
		3. is public
	  the rest is up to you
3. Users can list their own bookmarks and public bookmarks made by everyone.

For this task you must use the latest versions of Python, Django and Django Rest Framework.
Feel free to add any other libraries you need.
The application only exposes the API.
Do not implement the frontend, but provide a way to demonstrate that the API endpoints work.
This can be a bash script with Curl commands.

Try to achieve as much test coverage as possible.

In addition, please answer these questions:

1. What database would you choose to use for this application?
	- relational one beacuse of the feature to filter bookmarks by foreign key

2. How would you scale this application to support millions of users?
	- implement caching at least for basic feature as "list my own bookmarks"
	- more caching strategy depending on app usage pattern
	- distribute app to many cloud servers and put a load balancer in front
	- extend the database to cluster
	- depending on user beahavior maybe introduce replicated read only database nodes to speed up reads
	- maybe build a separate bookmark storage service to handle create bookmark requests and implement queue

3. How would you implement a background service that checks the validity of links stored in the database?
	- extend a model with some timestamp "last checked" and run a scheduled task which would check the URLs periodically
	- in case when URL is not available, maybe put a bookmark into a state "Unavailable" and give it some time to recover
	- after X amount of time mark a bookmark as "Invalid" and give a user notification and a way to edit or remove it

4. Describe approaches you can use to test this code.
	- by TestCase of Django
	- by unit tests
	- by curl or http from shell
	- by Selenium
	- by cron job to test application health (and also implement health info at some endpoint)

5. Bonus: describe what online resources you used to build this application and prepare answers to these questions.
	- https://www.django-rest-framework.org/
	- https://docs.djangoproject.com/

Please time-box this project to no more than 2-3 hours.
The application does not have to be in perfect working condition,
it is more important for us to see your approach to building applications.
