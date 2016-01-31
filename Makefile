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
	@echo '   make regenerate              regenerate files upon modification '
	@echo '   make publish                 generate using production settings '
	@echo '   make serve [PORT=8000]       serve site at http://localhost:8000'
	@echo '   make devserver [PORT=8000]   start/restart develop_server.sh    '
	@echo '   make stopserver              stop local server                  '
	@echo '   make ssh_upload              upload the web site via SSH        '
	@echo '   make rsync_upload            upload the web site via rsync+ssh  '
	@echo '   make dropbox_upload          upload the web site via Dropbox    '
	@echo '   make ftp_upload              upload the web site via FTP        '
	@echo '   make s3_upload               upload the web site via S3         '
	@echo '   make cf_upload               upload the web site via Cloud Files'
	@echo '   make github                  upload the web site via gh-pages   '
	@echo '   make pre_process             run only the pre-processor tasks   '
	@echo '   make tmp_cache               build the site and save to a temp cache dir'
	@echo '   make upload_cache            upload the temp cache dir'
	@echo '                                                                       '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html'
	@echo '                                                                       '

pre_process:
	./bin/pre-process.sh

html: pre_process
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)
	git clean -fd
	git submodule update

regenerate: pre_process
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve:
ifdef PORT
	cd $(OUTPUTDIR) && $(PY) -m pelican.server $(PORT)
else
	cd $(OUTPUTDIR) && $(PY) -m pelican.server
endif

devserver:
ifdef PORT
	$(BASEDIR)/develop_server.sh restart $(PORT)
else
	$(BASEDIR)/develop_server.sh restart
endif

stopserver:
	kill -9 `cat pelican.pid`
	kill -9 `cat srv.pid`
	@echo 'Stopped Pelican and SimpleHTTPServer processes running in background.'

publish: pre_process
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

dev: pre_process
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(DEVCONF) $(PELICANOPTS)

ssh_upload: publish
	scp -P $(SSH_PORT) -r $(OUTPUTDIR)/* $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

rsync_upload: publish
	rsync -e "ssh -p $(SSH_PORT)" -a --delete $(OUTPUTDIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

make_tmp_cache:
	mkdir -p $(CACHEDIR)

upload_cache: make_tmp_cache
	rsync -e "ssh -p $(SSH_PORT)" -a $(CACHEDIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

tmp_cache: publish make_tmp_cache
	rsync -ha --no-whole-file --inplace --delete $(OUTPUTDIR)/ $(CACHEDIR) --cvs-exclude

dropbox_upload: publish
	cp -r $(OUTPUTDIR)/* $(DROPBOX_DIR)

ftp_upload: publish
	lftp ftp://$(FTP_USER)@$(FTP_HOST) -e "mirror -R $(OUTPUTDIR) $(FTP_TARGET_DIR) ; quit"

s3_upload: publish
	s3cmd sync $(OUTPUTDIR)/ s3://$(S3_BUCKET) --acl-public --delete-removed

cf_upload: publish
	cd $(OUTPUTDIR) && swift -v -A https://auth.api.rackspacecloud.com/v1.0 -U $(CLOUDFILES_USERNAME) -K $(CLOUDFILES_API_KEY) upload -c $(CLOUDFILES_CONTAINER) .

github: publish
	ghp-import $(OUTPUTDIR)
	git push origin gh-pages

.PHONY: html help clean regenerate serve devserver publish ssh_upload rsync_upload dropbox_upload ftp_upload s3_upload cf_upload github dev pre_process
