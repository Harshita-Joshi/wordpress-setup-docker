import subprocess
import sys
import os
import shutil
import fileinput


#Checking installation status of docker and docker-compose services
def check_docker_installation():
    try:
        subprocess.check_output(["docker","--version"])
        subprocess.check_output(["docker-compose","--version"])
    except FileNotFoundError:
        subprocess.run(["apt-get","update"])
        subprocess.run(["apt-get","upgrade"])
        subprocess.run(["apt","install","docker.io"])
        subprocess.run(["apt","install","docker-compose"]) 

#Checking if site name is provided and making entry in host file
def check_site_name_input():
    if len(sys.argv) < 2:
        print("Site name not provided!!")
        sys.exit(1)
    else:
        global sitename
        sitename = sys.argv[1]
        with open('/etc/hosts','a') as hostsfile:
            hostsfile.write(f"127.0.0.1 {sitename}\n")


#Creating nginx and php folders for hosting configuration files
def create_dependency_folders():
    os.makedirs("wpsite/nginx")
    os.makedirs("wpsite/php")

#Creating configuration files inside nginx and php folders
def create_dependency_files(sitename):
    os.chdir("wpsite/nginx")
    config_nginx = f"""events {{}}
http{{
    server {{
        listen 80;
        listen [::]:80;
        server_name {sitename};
        root /var/www/html;
        index  index.php index.html;

        location / {{
            proxy_pass http://127.0.0.1:8000;
            try_files $uri $uri/ /index.php$is_args$args;
        }}

        location ~ \.php$ {{
            #try_files $uri =404;
            fastcgi_split_path_info ^(.+\.php)(/.+)$;
            fastcgi_pass phpfpm:9000;
            fastcgi_index index.php;
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_path_info;
        }}
    }}
}}"""
    #Creating config file for nginx service
    with open('default.conf','w') as filetowrite:
        filetowrite.write(config_nginx)
        
    os.chdir("../php")
    #Creating php and html files for php service
    with open('index.html','w') as filetowrite:
        filetowrite.write("<h1>Welcome to the Site!!</h1>\
<h2 style='text-align:center'>WordPress</h2>")

    with open('index.php','w') as filetowrite:
        filetowrite.write("<?php phpinfo(); ?>")

#Creating docker-compose.yaml file
def create_deploy_docker_compose_file():
    os.chdir("../")
    config_docker = """services:
  #databse
  db:
    image: mysql:8.0.21
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      MYSQL_DATABASE: wp
      MYSQL_USER: wp
      MYSQL_PASSWORD: passwd
      MYSQL_ROOT_PASSWORD: passwd
    networks:
      - wpsitenw
  
  phpfpm:
    image: php:fpm
    depends_on:
      - db
    ports:
      - '9000:9000'
    volumes: ['./public:/var/www/html']
    networks:
      - wpsitenw

  phpmyadmin:
    depends_on:
      - db
    image: phpmyadmin/phpmyadmin
    restart: unless-stopped
    ports:
      - '8080:80'
    environment:
      PMA_HOST: db
      MYSQL_ROOT_PASSWORD: passwd
    networks:
      - wpsitenw

  wordpress:
    depends_on: 
      - db
    image: wordpress:latest
    restart: always
    ports:
      - '8000:80'
    volumes: ['wordpress:/var/www/html']
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wp
      WORDPRESS_DB_PASSWORD: passwd
      WORDPRESS_DB_NAME: wp
    networks:
      - wpsitenw
  
  proxy:
    image: nginx:1.17.10
    depends_on:
      - db
      - wordpress
      - phpmyadmin
      - phpfpm
    ports:
      - '8001:80'
    volumes: 
      - wordpress:/var/www/html
      - ./nginx/default.conf:/etc/nginx/nginx.conf
    networks:
      - wpsitenw
networks:
  wpsitenw:
volumes:
  db_data:
  wordpress:"""
    
    with open('docker-compose.yml','w') as filetowrite:
        filetowrite.write(config_docker)
    subprocess.run(["docker-compose","up","-d"])

#Function prompting user to open a site    
def open_site():
    print(f"Site live!! Open this link in browser: {sitename}:8000")


if __name__ == "__main__":
    if sys.argv[1] == "enable":
        os.chdir("wpsite")
        subprocess.run(["docker-compose","start"])
    elif sys.argv[1] == "disable":
        os.chdir("wpsite")
        subprocess.run(["docker-compose","stop"])
    elif sys.argv[1] == "delete":
        sitename = sys.argv[2]
        os.chdir("wpsite")
        subprocess.run(["docker-compose","down","-v"])
        with fileinput.FileInput('/etc/hosts', inplace=True) as filetoedit:
            for line in filetoedit:
                if sitename not in line:
                    print(line,end='')
        os.chdir("../")        
        shutil.rmtree("wpsite")
    else:
        check_docker_installation()
        check_site_name_input()
        create_dependency_folders()
        create_dependency_files(sys.argv[1])
        create_deploy_docker_compose_file()
        open_site()
        

