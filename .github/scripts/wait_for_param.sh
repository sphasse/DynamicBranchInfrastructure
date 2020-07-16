#!/usr/bin/env bash

PARAM_NAME=${1}

REGION=${2}
if [ "$REGION" == "" ]; then
  REGION=us-east-1
fi

EXPECTED_STATE=provisioned

RETRIES=60
DELAY=5

# Loop for the specified number of retries waiting for the param to exist
while [[ ${RETRIES} -ne 0 ]]; do
    STATE=$(aws ssm get-parameter --name ${PARAM_NAME} --region ${REGION} --query "Parameter.Value"  --output text)

    if [[ "${STATE}" == "${EXPECTED_STATE}" ]]; then
        echo "Reached the expected state: ${EXPECTED_STATE}."
        exit 0
    fi

    echo "${EXPECTED_STATE} state not reached.  Sleeping.  $((RETRIES-1)) retries left."
    sleep ${DELAY}
    RETRIES=$((RETRIES-1))
done
echo "${EXPECTED_STATE} state not reached after waiting for $((RETRIES*DURATION)) seconds, terminating with an error."
exit 1
