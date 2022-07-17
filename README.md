# web service на питоне
Реализация Web-сервиса в рамках тестового задания

Порядорк установки на Ubuntu 20.04 LTS. Я все делал из под root на тестовй машине

Поставить или обновть docker и docker-compose
```
curl -sSL https://get.docker.com/ | sh
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Качаем проект 
```
git clone https://github.com/Froskur/web_service.git
```

**web_service** содалась в домашнем каталоге пользователя переходим в неё 
```
cd web_service
```

Ещё надо распоковать dump базы с точками, их там миллион :)
```
gzip -d _init_db/2-dump-data.sql.gz
```

Всё готово для запуска. Если не помните IP машины, выполните **hostname -I**
Поднимаем контейнеры 
```

```
