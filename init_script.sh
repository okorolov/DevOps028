#!/usr/bin/env bash

sudo echo "nameserver 8.8.8.8" > /etc/resolv.conf

export SAMSARA_DIR="/vagrant"
export LIQUIBASE_DIR="$SAMSARA_DIR/liquibase"
export BUILD_DIR="/build_env"

export LIQUIBASE_URL="https://github.com/liquibase/liquibase/releases/download/liquibase-parent-3.5.3/liquibase-3.5.3-bin.tar.gz"
export JDBC_URL="https://jdbc.postgresql.org/download/postgresql-42.1.4.jar"

export DB_PORT="5432"
export DB_HOST="localhost"
export DB_PASS="$(grep password $LIQUIBASE_DIR/liquibase.properties | awk '{print $2}')"
export DB_USER="$(grep username $LIQUIBASE_DIR/liquibase.properties | awk '{print $2}')"
export DB_NAME="$(grep url $LIQUIBASE_DIR/liquibase.properties | awk '{print $2}' | sed  's/.*5432\///')"
sed -i "s/localhost/$DB_HOST/g" $LIQUIBASE_DIR/liquibase.properties

sudo apt-get update
sudo apt-get -y install openjdk-8-jdk
sudo apt-get -y install maven
sudo apt-get -y install postgresql

sudo -u postgres createdb $DB_NAME
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME to $DB_USER;"

mkdir $BUILD_DIR
cd $BUILD_DIR
wget $LIQUIBASE_URL
wget $JDBC_URL

sudo tar -xzf liquibase-3.5.3-bin.tar.gz

sudo bash $BUILD_DIR/liquibase --defaultsFile=$LIQUIBASE_DIR/liquibase.properties --changeLogFile=$LIQUIBASE_DIR/changelogs/changelog-main.xml --classpath=$BUILD_DIR/postgresql-42.1.4.jar update

cd $SAMSARA_DIR
sudo mvn clean verify
java -jar target/*.jar
