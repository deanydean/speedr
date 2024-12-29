.PHONY: install

SYSTEMD_INSTALL_PATH ?= /etc/systemd/system
SPEEDR_INSTALL_PATH ?= /opt/speedr

install: # Install speedr onto the system
	# Create user if it doesn't exist
	if ! id -u speedr 1>/dev/null 2>&1; then \
		useradd --system --home-dir ${SPEEDR_INSTALL_PATH} --shell /bin/false speedr; \
	fi

	mkdir -p $(SPEEDR_INSTALL_PATH) 
	cp ./app.py ./requirements.txt $(SPEEDR_INSTALL_PATH)/.
	(cd $(SPEEDR_INSTALL_PATH) && pip3 install -r requirements.txt)
	chown -R speedr:speedr $(SPEEDR_INSTALL_PATH)

	cp ./speedr.service $(SYSTEMD_INSTALL_PATH)/.
	systemctl daemon-reload