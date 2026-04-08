FROM osrf/ros:jazzy-desktop

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-lc"]

# Dev tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential python3-pip python3-colcon-common-extensions \
    python3-vcstool ros-dev-tools sudo xauth \
 && rm -rf /var/lib/apt/lists/*

# ---------- Non-root user ----------
ARG USERNAME=robot
ARG UID=1000
ARG GID=1000

RUN set -eux; \
    if getent group "${GID}" >/dev/null; then \
        GROUP_NAME="$(getent group ${GID} | cut -d: -f1)"; \
    else \
        GROUP_NAME="${USERNAME}"; \
        groupadd -g "${GID}" "${GROUP_NAME}"; \
    fi; \
    if getent passwd "${UID}" >/dev/null; then \
        EFFECTIVE_USER="$(getent passwd ${UID} | cut -d: -f1)"; \
        usermod -aG sudo,dialout,video "${EFFECTIVE_USER}" || true; \
    else \
        EFFECTIVE_USER="${USERNAME}"; \
        useradd -m -u "${UID}" -g "${GID}" -s /bin/bash "${EFFECTIVE_USER}"; \
        usermod -aG sudo,dialout,video "${EFFECTIVE_USER}"; \
    fi; \
    echo "${EFFECTIVE_USER} ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/${EFFECTIVE_USER}"; \
    mkdir -p /home/${USERNAME}/ws; \
    chown -R "${UID}:${GID}" /home/${USERNAME}; \
    echo "EFFECTIVE_USER=${EFFECTIVE_USER}" >> /etc/environment

RUN set -eux; \
    for H in "/home/${USERNAME}"; do \
        echo 'source /opt/ros/jazzy/setup.bash' >> "$H/.bashrc"; \
    done

WORKDIR /home/${USERNAME}/ws

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER ${USERNAME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
