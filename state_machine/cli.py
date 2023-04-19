from typing import List
from state_machine.constants import (
    PROCESS_PAYMENT_STATE_MACHINE_JSON_FILE,
    CLOUDFORMATION_FILE,
    PAYMENT_SYSTEM_PLACEHOLDER,
    CLOUD_FORMATION_INJECTED_FILE)
from state_machine.payment_state_machine_definition import create_payment_state_machine

def write_state_machine_json():
    state_machines = [
        (create_payment_state_machine(), PROCESS_PAYMENT_STATE_MACHINE_JSON_FILE),
    ]
    for workflow_definition, output_file in state_machines:
        with open(output_file, "w+") as file:
            file.write(workflow_definition.definition.to_json())


def _inject_state_machine(state_machine_json: str, cloudformation_file: str, place_holder_pattern: str) -> str:
    subbed = False
    new_file: List[str] = []

    for line in cloudformation_file.splitlines():
        if place_holder_pattern in line and not subbed:
            new_file.append('            ' + state_machine_json + "\n")
            print("placeholder pattern found and replaced.")
            subbed = True
        else:
            new_file.append(line)
    cfn_file_with_state_machine = str.join("\n", new_file)
    return cfn_file_with_state_machine


def inject_all_state_machines_to_cloud_formation():
  cloud_formation = CLOUDFORMATION_FILE.read_text()
  step_functions = [
      (PROCESS_PAYMENT_STATE_MACHINE_JSON_FILE.read_text(), PAYMENT_SYSTEM_PLACEHOLDER),
  ]
  cloud_formation_with_injected_state_machine = cloud_formation
  for step_function, place_holder_pattern in step_functions:
      cloud_formation_with_injected_state_machine = _inject_state_machine(
          step_function,
          cloud_formation_with_injected_state_machine,
          place_holder_pattern)
  CLOUD_FORMATION_INJECTED_FILE.write_text(
      cloud_formation_with_injected_state_machine)

