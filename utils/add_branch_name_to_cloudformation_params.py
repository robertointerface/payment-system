import argparse
import pathlib
import json

parser = argparse.ArgumentParser(description="get git branch")


parser.add_argument(dest='branch_name',
                    metavar='branch_name',
                    help="github branch name")

if __name__ == "__main__":
    args = parser.parse_args()
    branch_name = args.branch_name
    params_directory = pathlib.Path(__file__).parent.parent / "cloudformation" / "cfn-config"
    params_json_file = params_directory / "feature-branch-params.json"
    parameters = json.loads(params_json_file.read_text())
    parameters_no_branch = [param for param in parameters if param["ParameterKey"] != "CurrentBranch"]
    parameters_no_branch.append({
        "ParameterKey": "CurrentBranch",
        "ParameterValue": branch_name
    })
    params_deploy = params_directory / "feature-branch-params-deploy.json"
    with open(params_deploy, "w+") as fp:
        fp.write(json.dumps(parameters_no_branch))
