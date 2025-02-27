# dj-tickets
This is a ticketing Django WEb Application.

# Running the app
cd into the ticketing folder. 
python3 -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate it (Linux/Mac)

venv\Scripts\activate(windows os)

pip install -r requirements.txt

python manage.py migrate -  make  migrations to the db

# creating superuser/admin
python manage.py createsuperuser
   -You will be prompted to enter your email, username, password(NB) -  Ypu will use these credentials to access your admin panel(/admin)


# run
python manage.py runserver


