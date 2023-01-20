region=us-west-2
aws configure set region $region

https://github.com/jovian-temple/lambda-netspeed.git

cd lambda-netspeed

virtualenv venv
source venv/bin/activate

chmod -R o+rX .

docker build -t netspeed .
aws ecr create-repository --repository-name netspeed --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
registryId=$(aws ecr describe-repositories --repository-name netspeed --query "repositories[0].registryId" --output text)
aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $registryId.dkr.ecr.$region.amazonaws.com 
docker tag  netspeed:latest $registryId.dkr.ecr.$region.amazonaws.com/netspeed:latest
docker push $registryId.dkr.ecr.$region.amazonaws.com/netspeed:latest        

aws iam create-role --role-name LambdaBasicExecutionRole --assume-role-policy-document file://LambdaBasicExecutionRole-Trust-Policy.json
aws iam attach-role-policy --policy arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole --role-name LambdaBasicExecutionRole

role = arn:aws:iam::$registryId:role/LambdaBasicExecutionRole
# --architectures x86_64 | arm64
aws lambda create-function --function-name netspeed \
    --package-type Image  \
    --timeout 60 \
    --architectures x86_64 \
    --memory-size 256 \
    --code ImageUri=$registryId.dkr.ecr.$region.amazonaws.com/netspeed:latest  \
    --role arn:aws:iam::$registryId":role/LambdaBasicExecutionRole"

aws lambda wait function-exists --function-name netspeed

aws lambda invoke --function-name netspeed response.json

aws lambda update-function-configuration --function-name  netspeed --memory-size 512

# run speed test loop
pip install boto3
python3 test.py

# references
https://www.speedtest.net/apps/cli
https://pypi.org/project/speedtest-cli/
https://hub.docker.com/r/amazon/aws-lambda-python
https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
https://docs.aws.amazon.com/lambda/latest/dg/troubleshooting-deployment.html

pip install speedtest-cli
