import pathlib
import json


if __name__ == "__main__":
    json_params_file = pathlib.Path(__file__).parent.parent / "cloudformation" / "cfn-config" / "feature-branch-params.json"
    parameters = json.loads(json_params_file.read_text())
    params = [f"{param['ParameterKey']}={param['ParameterValue']}"
              for param in parameters]
    params_in_string = f"{' '.join(params)}"
    conf_txt_location = json_params_file.parent / 'feature-branch-params.txt'
    with open(conf_txt_location, 'w+') as f:
        f.write(params_in_string)
