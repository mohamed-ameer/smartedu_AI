
#### 1- Update Agora credentals
In order to use this project you will need to replace the agora credentials in `views.py` and `streams.js`.

Create an account at agora.io and create an `app`.
Once you create your app, you will want to copy the `appid` & `appCertificate` to update `views.py` and `streams.js`.
If you have questions about where to get your app I'd recommend referencing this link `https://youtu.be/HX6AM_1-jNM?t=88`

###### views.py
```
def getToken(request):
    appId = "YOUR APP ID"
    appCertificate = "YOUR APPS CERTIFICATE"
    ......
```

###### streams.js
```
....
const APP_ID = 'YOUR APP ID'
....
```


#### 2 - Start server
```
python manage.py runserver
```


=>python -m venv .\venv
=>venv\scripts\activate
=>pip install -r requirements.txt
=>python manage.py makemigrations
=>python manage.py migrate
=>python manage.py createsuperuser
=>python manage.py runserver


very important
1-download from github
2-delete venv,db.sqlite3,all migrations from all APPS
3-go to models of module app then comment quizzes = models.ManyToManyField(to='quiz.Quizzes')
3-go to models of classroom app then comment 	modules = models.ManyToManyField(to='module.Module')
3-go to models of quiz app then comment course = models.ForeignKey(to='classroom.Course', on_delete=models.CASCADE)

4-py manage.py makemigrations for each app
5-uncomment what we commented in step 3
5-py manage.py makemigrations classroom
5-py manage.py makemigrations module
5-py manage.py makemigrations quiz



<a href="https://documenter.getpostman.com/view/19584619/UzJFwJhM" class="  mb-2 text-decoration-none text-white" target="_blank">APIs</a>


VISIT OUR SITE =====>
https://mohamedameer.pythonanywhere.com/home/
