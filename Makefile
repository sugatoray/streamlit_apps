.PHONY: streamlit_demo streamlit_run strun


ALT_STREAMLIT_PORT := 12321

## Streamlit App

streamlit_demo:
	# Note: To run the following command the port 8051 needs to be available.
	#       If somehow, a previously running streamlit session did not exit
	#		properly, you need to manually and forcibly stop it.
	#       Stop an already running streamlit server:
	#
	#       sudo fuser -k 8051/tcp
	streamlit run $(STREAMLIT_DEMO_APP) --server.port=8051 &

streamlit_run:
	# Note: To run the following command the port 8051 needs to be available.
	#       If somehow, a previously running streamlit session did not exit
	#		properly, you need to manually and forcibly stop it.
	#       Stop an already running streamlit server:
	#
	#       sudo fuser -k $(STREAMLIT_PORT)/tcp
	streamlit run $(STREAMLIT_DEMO_APP) --server.port=$(ALT_STREAMLIT_PORT) &

strun:
	# Example Usage:
	# $ make strun APP_NAME=streamlit_repl
	$(eval STREAMLIT_PORT := $(shell if [ -z $(STREAMLIT_PORT) ]; then echo 8051; else echo $(STREAMLIT_PORT); fi))
	@echo STREAMLIT_PORT is: [$(STREAMLIT_PORT)]
	streamlit run ./apps/$(APP_NAME)/app.py --server.port=$(STREAMLIT_PORT)
