#run nginx
sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

#sudo ln -sf /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/test
#sudo gunicorn -c hello.py hello:app

# run MySQL & create DB
#sudo -s /etc/init.d/mysql start && mysql -uroot -e "create database django"
sudo -s /etc/init.d/mysql start
sudo mysql -uroot -e "create database django;"
sudo mysql -uroot -e "grant all privileges on django.* to 'root'@'localhost' with grant option;"

sudo ln -sf /home/box/web/etc/django-gunicorn.conf /etc/gunicorn.d/ask	
sudo gunicorn -c /home/box/web/etc/django-gunicorn.conf ask/ask/wsgi:application
#~/web/ask/ask.wsgi:application
sudo /etc/init.d/gunicorn restart

~/web/ask/manage.py makemigrations
~/web/ask/manage.py migrate
#~/web/ask/manage.py runserver 0.0.0.0:8000