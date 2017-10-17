pipeline {

    agent {label 'Slave'}
    tools {maven 'maven 3.5.0'}

    stages {
        stage('AWS Cleanup') {
            steps {
				sh "chmod +x infra/aws_cleanup.py"
				sh "./infra/aws_cleanup.py"
            }
        }
        stage('Checkout') {
            steps {git url: 'https://github.com/okorolov/DevOps028'}
        }
		stage('Build Project') {
			steps {
				echo 'Building and Packaging Project..'
				sh "mvn clean compile"
			}
		}
		stage('Test and Package') {
			steps {
				echo 'Testing and Packaging Project..'
				sh "mvn package"
			}
		}
		stage('Archive Artifact') {
			steps {
			    sh 'export BUILD_NAME=`ls ./target | grep jar | grep -v original` && ' +
			       'aws ssm put-parameter --region=eu-west-1 --name BUILD_NAME --value="${BUILD_NAME}" --type String --overwrite'
			    archive 'target/*.jar'
			}
		}
		stage('Upload to S3') {
			steps {
				sh "tar cvzf samsara_infra.tar.gz liquibase/changelogs/sql/ src/main/resources/application.properties liquibase/liquibase.properties liquibase/changelogs/changelog-main.xml liquibase/changelogs/changelog-v1.0.xml"
				sh "wget https://github.com/liquibase/liquibase/releases/download/liquibase-parent-3.5.3/liquibase-3.5.3-bin.tar.gz"
				sh "wget https://jdbc.postgresql.org/download/postgresql-42.1.4.jar"
				sh "aws s3 --region eu-west-1 cp target/*.jar	s3://samsara-builds/"
				sh "aws s3 --region eu-west-1 cp liquibase-3.5.3-bin.tar.gz	s3://samsara-infrastructure/liquibase-3.5.3-bin.tar.gz"
				sh "aws s3 --region eu-west-1 cp postgresql-42.1.4.jar s3://samsara-infrastructure/postgresql-42.1.4.jar"
				sh "aws s3 --region eu-west-1 cp liquibase/liquibase.properties s3://samsara-infrastructure/liquibase.properties"
				sh "aws s3 --region eu-west-1 cp infra/first_run.sh s3://samsara-infrastructure/first_run.sh"
				sh "aws s3 --region eu-west-1 cp samsara_infra.tar.gz s3://samsara-infrastructure/samsara_infra.tar.gz"
            }
		}
		stage('Prepare RDS') {
			steps {
				sh "chmod +x infra/aws_rds_create.py"
				sh "./infra/aws_rds_create.py"
			}
		}
		stage('Prepare Launch Configuration') {
			steps {
				sh "chmod +x infra/aws_autoscale_lg.py"
				sh "./infra/aws_autoscale_lg.py"
			}
		}
		stage('Prepare Load Balancer') {
			steps {
				sh "chmod +x infra/aws_autoscale_lb.py"
				sh "./infra/aws_autoscale_lb.py"
			}
		}
		stage('Start Autoscaling Group') {
			steps {
				sh "chmod +x infra/aws_autoscale_as.py"
				sh "./infra/aws_autoscale_as.py"
			}
		}

	}
}
