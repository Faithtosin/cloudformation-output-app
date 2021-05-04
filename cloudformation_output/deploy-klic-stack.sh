
#!/bin/bash




stack_name=$1
stack_num=$2

if [ -z "$stack_name" ]; then
  echo "stack_name not set";
  exit 1;
fi;

if [ -z "$stack_num" ]; then
  echo "stack_num not set";
  exit 1;
fi;

export STACKNAME=$stack_name
export STACKNUMBER=$stack_num

echo "Deploying cloudformation stack"

python3 create-stack.py

