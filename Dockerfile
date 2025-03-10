FROM redhat/ubi9:9.5-1739751568

LABEL maintainer="Lin Gao <aoingl@gmail.com>"

# add user lgao
RUN groupadd -g 1000 lgao && useradd -u 1000 -g 1000 lgao

# install basic utilities
RUN dnf install -y net-tools wget jq python python3-pip

COPY requirements.txt .
RUN pip install -r requirements.txt

USER lgao

ARG USER_HOME_DIR="/home/lgao"
ARG PROJECT_BASE_DIR="${USER_HOME_DIR}/llm"
# create workspace directory to share to all
RUN mkdir -p ${PROJECT_BASE_DIR}
WORKDIR ${PROJECT_BASE_DIR}

RUN jupyter notebook --generate-config

# disable token, use it directly
RUN echo "c.NotebookApp.token = ''" >> ${USER_HOME_DIR}/.jupyter/jupyter_notebook_config.py
# do not check for update, it should be done during the docker build time.
RUN echo "c.ServerApp.disable_check_for_update = True" >> ${USER_HOME_DIR}/.jupyter/jupyter_notebook_config.py

# sys append shared utilties
RUN mkdir -p ${USER_HOME_DIR}/.ipython/profile_default/startup
COPY 00-add-path.py ${USER_HOME_DIR}/.ipython/profile_default/startup/00-add-path.py
RUN sed -i "s|__SHARED_LIB_DIR__|${PROJECT_BASE_DIR}|g" ${USER_HOME_DIR}/.ipython/profile_default/startup/00-add-path.py

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser", "--autoreload", "--notebook-dir=/home/lgao/llm"]