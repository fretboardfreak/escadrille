# Squadron Makefile
#
# Squadron is an automation extension of the pelican website generator.
#

ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

help:
	@echo 'Makefile for a pelican Web site                                        '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make html                    (re)generate the web site          '
	@echo '   make clean                   remove the generated files         '
	@echo '   make publish                 generate using production settings '
	@echo '   make dev                     generate using dev settings '
	@echo '   make ssh_upload              upload the web site via SSH        '
	@echo '   make rsync_upload            upload the web site via rsync+ssh  '
	@echo '   make pre_process             run only the pre-processor tasks   '
	@echo '   make tmp_cache               build the site and save to a temp cache dir'
	@echo '   make upload_cache            upload the temp cache dir'
	@echo '                                                                       '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html'
	@echo '                                                                       '

pre_process:
	./bin/pre-process.sh

html: pre_process
	$(PELICAN) $(INPUT_DIR) -o $(OUTPUT_DIR) -s $(CONFFILE) $(PELICANOPTS)

clean:
	[ ! -d $(OUTPUT_DIR) ] || rm -rf $(OUTPUT_DIR)
	git clean -fd
	git submodule update

publish: pre_process
	$(PELICAN) $(INPUT_DIR) -o $(OUTPUT_DIR) -s $(PUBLISHCONF) $(PELICANOPTS)

dev: pre_process
	$(PELICAN) $(INPUT_DIR) -o $(OUTPUT_DIR) -s $(DEVCONF) $(PELICANOPTS)

ssh_upload: publish
	scp -P $(SSH_PORT) -r $(OUTPUT_DIR)/* $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

rsync_upload: publish
	rsync -e "ssh -p $(SSH_PORT)" -a --delete $(OUTPUT_DIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

make_tmp_cache:
	mkdir -p $(CACHE_DIR)

upload_cache: make_tmp_cache
	rsync -e "ssh -p $(SSH_PORT)" -a $(CACHE_DIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

tmp_cache: publish make_tmp_cache
	rsync -ha --no-whole-file --inplace --delete $(OUTPUT_DIR)/ $(CACHE_DIR) --cvs-exclude

.PHONY: html help clean regenerate serve devserver publish ssh_upload rsync_upload github dev pre_process
