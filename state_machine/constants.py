import pathlib

PROJECT_DIRECTORY = pathlib.Path(__file__).parent.parent
STATE_MACHINE_DIRECTORY = pathlib.Path(__file__).parent
PROCESS_PAYMENT_STATE_MACHINE_JSON_FILE = STATE_MACHINE_DIRECTORY / 'state-machine-json' / 'process-payment-state-machine.json'
CLOUDFORMATION_FILE = PROJECT_DIRECTORY / 'cloudformation' / 'cfn.yml'
PAYMENT_SYSTEM_PLACEHOLDER = '##{{PROCESS_PAYMENT_DEF}}'
CLOUD_FORMATION_INJECTED_FILE = PROJECT_DIRECTORY / "cfn-injected.yml"