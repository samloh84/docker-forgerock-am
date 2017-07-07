FROM samloh84/apache-tomcat:8.5.15

ARG VENDOR=forgerock
ARG PRODUCT=am
ARG PRODUCT_VERSION=5.1.0
ARG TEMP_DIR_ROOT=/tmp/${VENDOR}-${PRODUCT}
ARG TEMP_DIR=${TEMP_DIR_ROOT}/${PRODUCT_VERSION}
ARG INSTALL_DIR_ROOT=/opt/${VENDOR}-${PRODUCT}
ARG INSTALL_DIR=${INSTALL_DIR_ROOT}/${PRODUCT_VERSION}

ARG AM_INSTALL_ZIP=AM-${PRODUCT_VERSION}.zip
ARG AM_SERVLET=AM-${PRODUCT_VERSION}.war
ARG TOOLS_VERSION=14.1.0
ARG INSTALL_ADMIN_TOOLS=SSOAdminTools-${PRODUCT_VERSION}
ARG INSTALL_ADMIN_TOOLS_ZIP=SSOAdminTools-${PRODUCT_VERSION}.zip
ARG INSTALL_CONFIGURATOR_TOOLS=SSOConfiguratorTools-${PRODUCT_VERSION}
ARG INSTALL_CONFIGURATOR_TOOLS_ZIP=SSOConfiguratorTools-${PRODUCT_VERSION}.zip

COPY ${AM_INSTALL_ZIP} entrypoint.sh generate_config.py ${TEMP_DIR}/

USER ${ROOT_UID}

RUN \

yum-install which zip unzip && \

mkdir -p ${INSTALL_DIR} && \
pushd ${TEMP_DIR} && \
unzip -qq ${AM_INSTALL_ZIP} -d ${TEMP_DIR} && \

# Patch WAR file
mkdir -p ${TEMP_DIR}/WEB-INF/classes && \
echo "configuration.dir=${INSTALL_DIR}/config" > WEB-INF/classes/bootstrap.properties && \
zip -u ${TEMP_DIR}/openam/${AM_SERVLET} WEB-INF/classes/bootstrap.properties && \

# Move WAR file to Tomcat directory
rm -rf ${CATALINA_HOME}/webapps/* && \
mv ${TEMP_DIR}/openam/${AM_SERVLET} ${CATALINA_HOME}/webapps/openam.war && \

unzip -qq ${TEMP_DIR}/openam/${INSTALL_ADMIN_TOOLS_ZIP} -d ${INSTALL_DIR}/${INSTALL_ADMIN_TOOLS} && \
unzip -qq ${TEMP_DIR}/openam/${INSTALL_CONFIGURATOR_TOOLS_ZIP} -d ${INSTALL_DIR}/${INSTALL_CONFIGURATOR_TOOLS} && \

# Move scripts to AM directory
mv ${TEMP_DIR}/entrypoint.sh ${INSTALL_DIR}/entrypoint.sh && \
mv ${TEMP_DIR}/generate_config.py ${INSTALL_DIR}/generate_config.py && \
chmod +x ${INSTALL_DIR}/entrypoint.sh && \
chmod +x ${INSTALL_DIR}/generate_config.py && \

fix-ownership ${INSTALL_DIR} ${CATALINA_HOME} && \
fix-permissions ${INSTALL_DIR} ${CATALINA_HOME} && \

popd && \
rm -rf ${TEMP_DIR_ROOT}


ENV M2_HOME ${INSTALL_DIR}
ENV PATH ${PATH}:${M2_HOME}/bin

EXPOSE 8080
EXPOSE 50389
EXPOSE 4444
EXPOSE 1689
EXPOSE 58989

ENV OPENAM_HOME ${INSTALL_DIR}
ENV OPENAM_CONFIGURATOR_TOOLS ${OPENAM_HOME}/${INSTALL_CONFIGURATOR_TOOLS}
ENV OPENAM_CONFIGURATOR_TOOL ${OPENAM_CONFIGURATOR_TOOLS}/openam-configurator-tool-${TOOLS_VERSION}.jar
ENV OPENAM_UPGRADE_TOOL ${OPENAM_CONFIGURATOR_TOOLS}/openam-upgrade-tool-${TOOLS_VERSION}.jar
ENV OPENAM_ADMIN_TOOLS ${OPENAM_HOME}/${INSTALL_ADMIN_TOOLS}

ENV PATH ${PATH}:${OPENAM_ADMIN_TOOLS}/bin

USER ${APP_UID}

WORKDIR ${OPENAM_HOME}

CMD ${OPENAM_HOME}/entrypoint.sh
