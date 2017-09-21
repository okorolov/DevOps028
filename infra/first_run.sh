#!/bin/bash
yum update -y
yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
yum install -y java-1.8.0-openjdk
/usr/sbin/alternatives --set java /usr/lib/jvm/jre-1.8.0-openjdk.x86_64/bin/java
mkdir build_env
cd /build_env
aws s3 cp s3://samsara-infrastructure/samsara_infra.tar.gz .
aws s3 cp s3://samsara-infrastructure/liquibase.sh .
aws s3 cp s3://samsara-infrastructure/liquibase.jar .
aws s3 cp s3://samsara-infrastructure/postgresql.jar .
aws s3 cp s3://samsara-builds/$BUILD_NAME .
tar -xvf samsara_infra.tar.gz
whilerun=1
while [ $whilerun = 1 ]; do state=$(aws rds describe-db-instances --region eu-west-1 --query "DBInstances[*].DBInstanceStatus" --output text); if [ "$state" == "available" ]; then whilerun='0'; else sleep 10; fi; done
export DB_PASS="$(grep password /build_env/liquibase/liquibase.properties | awk '{print $2}')"
export DB_USER="$(grep username /build_env/liquibase/liquibase.properties | awk '{print $2}')"
export DB_NAME="$(grep url /build_env/liquibase/liquibase.properties | awk '{print $2}' | sed  's/.*5432\///')"
export DB_HOST="$(aws rds describe-db-instances --region eu-west-1 --query "DBInstances[*].Endpoint.Address" --output text)"
sed -i "s/localhost/$DB_HOST/g" /build_env/liquibase/liquibase.properties
bash /build_env/liquibase.sh --defaultsFile=/build_env/liquibase/liquibase.properties --changeLogFile=/build_env/liquibase/changelogs/changelog-main.xml --classpath=/build_env/postgresql.jar update
java -jar Samsara-1.3.5.RELEASE.jar
