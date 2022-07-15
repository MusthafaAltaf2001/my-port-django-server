Instructions to run the server
- Open CMD terminal(not powershell) in vs code.
- navigate to Scripts folder using cd command
- run the file activate.bat. This step is performed to enter the virtual environment.
- go back to the onlineinvestmentdjango folder from the terminal
- enter the command "python manage.py runserver" and run it to run the server.


Api endpoints:
- `http://127.0.0.1:8000/lands/updateLandValues/` - Updates the database with latest land values. The algorithm at this endpoint may take about 10 minutes to run depending on the speed of your cpu.
- `http://127.0.0.1:8000/lands/getLandValues/` - Fetches all the land values from the database.