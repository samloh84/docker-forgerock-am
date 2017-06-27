#!/bin/bash

AM_BASE_DIR=${AM_BASE_DIR:-${OPENAM_HOME}/config}
AUTO_CONFIGURE=${AUTO_CONFIGURE:-1}
DEBUG_AUTO_CONFIGURE=${DEBUG_AUTO_CONFIGURE:-0}

POLL_INTERVAL=3
POLL_TIMEOUT=180

function configure() {

CONFIG_JAR=""
if [[ ! -d ${AM_BASE_DIR} ]]; then
    echo "AM Config Directory [${AM_BASE_DIR}] is missing, configuring..."
    CONFIG_JAR=${OPENAM_CONFIGURATOR_TOOL}
elif [[ "AM_UPDATE" == "true" ]]; then
    echo "Updating AM Config Directory [${AM_BASE_DIR}] ..."
    CONFIG_JAR=${OPENAM_UPGRADE_TOOL}
fi

if [[ ! -z "${CONFIG_JAR}" ]]; then
    echo "Generating configuration..."
    python2 generate_config.py | tee /tmp/am_config
    if [[ ! $? -eq 0 ]]; then
        echo "Error generating configuration..."
        if [[ ${DEBUG_AUTO_CONFIGURE} -eq 0 ]]; then
        	terminate 1
		else
			return 1
    	fi
    fi
    echo "Configuration generated... Running Configuration Tool."
    java -jar ${CONFIG_JAR} -f /tmp/am_config
    if [[ ! $? -eq 0 ]]; then
        echo "Error configuring AM..."
        if [[ ${DEBUG_AUTO_CONFIGURE} -eq 0 ]]; then
        	terminate 1
		else
			return 1
    	fi
    fi
    echo "Setting up Admin Tool..."
    pushd ${OPENAM_ADMIN_TOOLS}
    ./setup --path ${AM_BASE_DIR} --acceptLicense
    if [[ ! $? -eq 0 ]]; then
        echo "Error setting up Admin Tool..."
        if [[ ${DEBUG_AUTO_CONFIGURE} -eq 0 ]]; then
        	terminate 1
		else
			return 1
    	fi
    fi

    echo "AM Configuration complete!"
fi

}

function poll() {


START_TIMESTAMP=$(date +%s)
TIMEOUT=$(expr ${START_TIMESTAMP} + ${POLL_TIMEOUT})

while true; do
	curl --silent --fail ${AM_SERVER_URL}/openam
	if [[ $? -eq 0 ]]; then
		configure
		break;
	else
		CURRENT_TIMESTAMP=$(date +%s)
		TIME_ELAPSED=$(expr ${CURRENT_TIMESTAMP} - ${START_TIMESTAMP})
		if [[ ${TIME_ELAPSED} -ge ${TIMEOUT} ]]; then
			echo "Exceeded poll timeout, exiting."
			terminate
			exit 1
		fi
		echo "[${TIME_ELAPSED} seconds] Polling for ${AM_SERVER_URL}/openam endpoint... Sleeping for ${POLL_INTERVAL} seconds..."
		sleep ${POLL_INTERVAL}
	fi
done

}

function start(){
	echo "Starting Apache Tomcat..."
	${CATALINA_HOME}/bin/catalina.sh run &
	export CATALINA_PID=$!
	echo "Apache Tomcat started with PID ${CATALINA_PID}..."


	if [[ ${AUTO_CONFIGURE} -eq 1 ]]; then
		echo "Autoconfiguration enabled..."
		poll
	else
		echo "Autoconfiguration disabled..."
	fi

	wait ${CATALINA_PID}
}

function terminate(){
	echo "Terminating Apache Tomcat with PID ${CATALINA_PID}..."
	kill ${CATALINA_PID}
	echo "Terminated Apache Tomcat."
	exit ${1:-0}
}

if [[ "${1}" == "configure" ]]; then
	configure
	exit
fi


trap terminate EXIT
start
