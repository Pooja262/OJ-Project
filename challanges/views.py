import json
#import requests
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseForbidden,HttpResponse, JsonResponse
from .models import Problem
from .forms import ProblemForm,CodeCompileForm,CodeSubmissionForm
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt

# List of problems
def problem_list_view(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problem_list.html', {'problems': problems})

# Detail view for a specific problem
def problem_detail_view(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    output, verdict = None, None

    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        custom_input = request.POST.get('custom_input')
        action = request.POST.get('action')

        if action == 'run':  # Run code with custom input
            if code and language:
                output = run_code(language, code, custom_input, pk)
            else:
                output = "Please provide both code and language."
        
        elif action == 'submit':  # Submit code for inbuilt test cases
            # Run code for each test case and compare output
            all_passed = True
            for test_case in problem.test_cases.all():
                expected_output = test_case.expected_output
                actual_output = run_code(code=code, language=language, input_data=test_case.input_data, pk=pk)
                
                if actual_output != expected_output.strip():
                    all_passed = False
                    output = actual_output
                    break
            verdict = "Accepted" if all_passed else "Wrong Answer"

    return render(request, 'problems/problem_detail.html', {
        'problem': problem,
        'output': output,
        'verdict': verdict,
    })

'''def compile_code(code, language, input_data):
    api_url = 'https://api.judge0.com/submissions/?base64_encoded=false&wait=true'
    language_map = {
        'python': 71, 'javascript': 63, 'c': 50, 'cpp': 54
    }
    headers = {'Content-Type': 'application/json'}
    payload = {
        'language_id': language_map[language],
        'source_code': code,
        'stdin': input_data,
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json().get('stdout', 'Error executing code')
    return "Error connecting to compiler service"
'''

@login_required
def problem_create_view(request):
    # Check if the user is an admin
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to add problems.")

    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('problem_list')  # Redirect to the challenges list
    else:
        form = ProblemForm()

    return render(request, 'problems/add_problem.html', {'form': form})




def submit(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = problem
            code = submission.code
            language = submission.language

            test_cases = problem.get_test_cases()
            verdicts = []

            for test_input, expected_output in test_cases:
                output = run_code_logic(language, code, test_input)

                verdict = {
                    "input": test_input,
                    "expected_output": expected_output,
                    "actual_output": output.strip().lower(),
                    "result": "Accepted" if output.strip().lower() == expected_output.strip() else "Wrong Answer"
                }
                verdicts.append(verdict)

            return render(request, "result.html", {"verdicts": verdicts, "problem": problem})
    else:
        form = CodeSubmissionForm()
    
    return render(request, "index.html", {"form": form})

@csrf_exempt
def run_code(request, pk=None):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code")
            language = data.get("language")
            action = data.get("action")

            if action == "submit":
                problem = Problem.objects.get(id=pk)
                test_cases = problem.get_test_cases()  # Get all test cases as tuples

                # Collect results for each test case
                verdicts = []
                for input_data, expected_output in test_cases:
                    actual_output = run_code_logic(language, code, input_data, pk)
                    verdicts.append({
                        "input": input_data,
                        "expected_output": expected_output,
                        "actual_output": actual_output,
                        "status": "Accepted" if actual_output.strip().lower() == expected_output.strip() else "Wrong Answer",
                        "is_correct": actual_output.strip().lower() == expected_output.strip(),  # True for correct, False for incorrect
})
                    
                
                return JsonResponse({"verdict": verdicts})

            elif action == "run":
                # Run with custom input (not part of test cases)
                custom_input = data.get("custom_input", "")
                output = run_code_logic(language, code, custom_input, pk)
                return JsonResponse({"output": output.lower()})

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON payload", "details": str(e)}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)


def run_code_logic(language, code, input_data="", pk=None):
    # Set up directories and file paths
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]
    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())
    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    # Initialize executable_path to None for cleanup
    executable_path = None

    # Write code and input files
    with code_file_path.open("w") as file:
        file.write(code)
    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)
    with open(output_file_path, "w") as output_file:
        pass

    try:
        print(language)
        if language == "cpp":
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ["clang++", str(code_file_path), "-o", str(executable_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("Compilation Result:", compile_result)  # Debug

            if compile_result.returncode != 0:
                return "Compilation Error: " + compile_result.stderr.decode()

            # Run executable and capture output
            with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                exec_result = subprocess.run(
                    [str(executable_path)],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.PIPE
                )
                print("Execution Result:", exec_result)  # Debug
                if exec_result.returncode != 0:
                    return "Runtime Error: " + exec_result.stderr.decode()

        elif language == "python":
            
        # Code for executing Python script
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    
                    subprocess.run(
                        ["python", str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )
                
                

        # Check if output file exists and return its content
        if output_file_path.exists():
            with open(output_file_path, "r") as output_file:
                return output_file.read()
        else:
            print("Output file not found.")
            return "Error: Output file not found. Code execution might have failed."

    finally:
        # Cleanup
        for path in [code_file_path, input_file_path, output_file_path, executable_path]:
            if path and path.exists():
                path.unlink(missing_ok=True)
