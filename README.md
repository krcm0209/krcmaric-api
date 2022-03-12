# krcmaric-api

This project contains source code and supporting files for a serverless API that can be deployed with the SAM CLI. It includes the following files and folders.

- api - Code for the API's Lambda function.
- events - Invocation events that can be used to invoke the function.
- tests - (WIP) Unit tests for the API code. 
- template.yaml - A template that defines the API's AWS resources.

The API uses several AWS resources, including Lambda functions and API Gateway. These resources are defined in the `template.yaml` file in this project. The template can be updated to add AWS resources through the same deployment process that updates the API code.

If an integrated development environment (IDE) is used to build and test the API, the AWS Toolkit can be used.  
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS. The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code. See the following links to get started.

* [CLion](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [GoLand](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [WebStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [Rider](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PhpStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [RubyMine](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [DataGrip](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

## Deploy the API

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run functions in an Amazon Linux environment that matches Lambda. It can also emulate the application's build environment and API.

To use the SAM CLI, the following tools are needed.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy the application for the first time, run the following in the shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of the application. The second command will package and deploy the application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to the account and region, and a good starting point would be something matching the project name.
* **AWS Region**: The AWS region to deploy the API to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example `--capabilities CAPABILITY_IAM` must be explicitly passed to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, the choices will be saved to a configuration file inside the project, so that in the future `sam deploy` can just be re-run without parameters to deploy changes to the application.

The API Gateway Endpoint URL can be found in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build the application with the `sam build --use-container` command.

```bash
krcmaric-api$ sam build --use-container
```

The SAM CLI installs dependencies defined in `api/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
krcmaric-api$ sam local invoke ApiFunction --event events/event.json
```

The SAM CLI can also emulate the application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
krcmaric-api$ sam local start-api
krcmaric-api$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        GetViews:
          Type: HttpApi
          Properties:
            Path: /views
            Method: get
```

## Add a resource to the API
The API template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), the standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types can be used.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets logs generated by your deployed Lambda function from the command line get fetched. In addition to printing the logs on the terminal, this command has several nifty features to help find the bug quickly.

`NOTE`: This command works for all AWS Lambda functions; not just the ones deployed using SAM.

```bash
krcmaric-api$ sam logs -n ApiFunction --stack-name krcmaric-api --tail
```

More information and examples about filtering Lambda function logs can be found in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
krcmaric-api$ pip install -r tests/requirements.txt --user
# unit test
krcmaric-api$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack under test
krcmaric-api$ AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```

## Cleanup

To delete the API that was created, use the AWS CLI. Assuming the project name was used for the stack name, the following can be run:

```bash
aws cloudformation delete-stack --stack-name krcmaric-api
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.
