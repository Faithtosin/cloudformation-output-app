version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "cloudformation-output-app"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-12ub2iaem0y2u"
s3_prefix = "cloudformation-output-app"
region = "us-east-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"

[y]
[y.deploy]
[y.deploy.parameters]
stack_name = "cloudformation-output-app"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-12ub2iaem0y2u"
s3_prefix = "cloudformation-output-app"
region = "us-east-1"
capabilities = "CAPABILITY_IAM"
confirm_changeset = true
