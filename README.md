# {{ project_title }}

Run `python3 setup.py` to apply the project title. The setup pass renames
`microservice.service` to `{{ project_title }}.service` and leaves the service
directory, port, and all other template slots available for the later
configuration routine.

Replace `src/frontend/favicon.png` to customize the icon served from both
`/favicon.png` and `/favicon.ico`.
