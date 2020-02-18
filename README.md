# A cloud storage of files

Users are provided with AES encrption of files 
Clone this Repository into your Folder.

## Instructions for Web Client:

Run these commands inside the project directory:
```python
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver
```

Now open the url 127.0.0.1:8000 in your browser 

## Instructions for Linux Client:

Install the djagno's db-file storage :
```python
	pip install django-database-storage
```
Install tabulate :
```python
	pip install tabulate
```

Add the bash executable spc ( Found in Secure-Personal-Cloud/bin/ directory ) to your environment PATH variable and run:

```bash 
	spc help
```

