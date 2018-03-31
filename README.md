# TODO from core folder

Start project (localhost)
---------------------------------------
1. Make sure nginx-proxy is working (https://github.com/jwilder/nginx-proxy)

2. Adding hosts 

    Add a few lines in file /etc/hosts:

    127.0.0.1 eatbot.loc
    
3. Start project

    console# docker-compose up

4. Create admin user. Get output "admin@admin.com created successfully"

    console# docker/create_superuser.sh  (in dev environment only.)

5. Final test

    - Check admin with credentials admin@admin.com / 123123
    http://eatbot.loc/admin/
    - Check API swagger
    http://eatbot.loc/docs/
    - Check home page
    http://eatbot.loc/


6. To run scrapy parser
scrapy crawl food_spider -a id=1 -a do_action=yes