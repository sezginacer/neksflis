## Neksflis - Subscription Based Content Consuming
- In order to run the project, execute in the project root directory `docker-compose up`
- There is a problem with PostgreSQL when running project with *docker* for the first time. PostgreSQL may be unavailable for first time of running `docker-compose up`. Terminating it and triggering `docker-compose up` again solves this problem.
- There are some scripts to ease to understand project structure & API calls. You can
 run these script as follows:\
    `docker-compose exec web python manage.py runscript setup`\
    `docker-compose exec web python manage.py runscript subscription`

## Flowchart for Neksflis
![Flowchart](https://github.com/sezginacer/neksflis/blob/master/flowchart.png?raw=true)
### Notes about the Flowchart
- Neksflis has unsubscription scenario, but I could not mount the scenario into the flowchart.
- Customers can consume content for 5 days even if their payment for new subscription period is pending. I could not mount this scenario into the flowchart too.
