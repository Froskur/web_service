# web service на питоне
Реализация Web-сервиса в рамках тестового задания

## Порядок установки на Ubuntu 20.04 LTS. Я все делал из под root на тестовой машине

Поставить или обновить docker и docker-compose
```
curl -sSL https://get.docker.com/ | sh
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```

Качаем проект 
```
git clone https://github.com/Froskur/web_service.git
```

**web_service** создалась в домашнем каталоге пользователя, переходим в неё 
```
cd web_service
```

Ещё надо распаковать dump базы с точками, их там миллион :)
```
gzip -d _init_db/2-dump-data.sql.gz
```

Всё готово для запуска. Если не помните IP машины, выполните **hostname -I**
Поднимаем контейнеры 
```
docker-compose up -d
```
Можно без ключа -d, чтобы видеть когда все запустится. Первый запуск будет долгим, так как будет импорт базы большой.

Когда всё запуститься, возможно, нужно открыть порты 8000-8003 и 5443. Работа идет по основному 8000 но остальные тоже открыты, чтобы посмотреть API микро-сервисов и иметь возможность подключиться к базе
```
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```
```
sudo iptables -A INPUT -p tcp --dport 8001 -j ACCEPT
```
```
sudo iptables -A INPUT -p tcp --dport 8002 -j ACCEPT
```
```
sudo iptables -A INPUT -p tcp --dport 8003 -j ACCEPT
```
```
sudo iptables -A INPUT -p tcp --dport 5443 -j ACCEPT
```

Если что-то пошло не так, то остановите все контейнеры и с помощью docker-compose down и снова выполните docker-compose up -d

# Подключение 

После запуска основой и рабочий gate доступен по адресу 
```
http://<Your_IP>:8000/api/v1/docs
```

Для авторизации доступны четыре пользователя user1, user2, user3, user4. Пароли совпадают с именами в том же регистре. Можно обращаться через POSTMAN (например) сразу к методам. Используйте Bearer авторизации с токеном. Токен у каждого пользователя совпадает с логином. 

# Дополнения 

После запуска, API внутренних сервисов, не закрыты и доступны. Там есть расширенные функции (не много). В частности, функции удаления и обновления точки, однако они не нужны были в тестовом задании и неизвестно что будет при попытке удалить точку в маршруте. База-то не даст, а вот API не проверял :)

```
http://<Your_IP>:8001/api/v1/points/docs
```
```
http://<Your_IP>:8002/api/v1/routes/docs
```
```
http://<Your_IP>:8003/api/v1/reports/docs
```
На них нет авторизации, потому как предполагается что они не доступны сами в рабочей среде.


Для подключения к базе можно воспользоваться следующими данными:
```
    POSTGRES_DB: "route"
    POSTGRES_USER: "shared_user"
    POSTGRES_PASSWORD: "shared_pass"

```

