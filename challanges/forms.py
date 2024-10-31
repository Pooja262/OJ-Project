from django import forms
from .models import Problem, CodeSubmission

LANGUAGE_CHOICES = [
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('c', 'C'),
    ('cpp', 'C++'),
]

class CodeSubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = CodeSubmission
        fields = ["language", "code", "input_data"]

class CodeCompileForm(forms.Form):
    code = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your code here...'}),
        label="Your Code"
    )
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, label="Select Language")
    custom_input = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter custom input...'}),
        required=False,
        label="Custom Input"
    )

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'title', 
            'description', 
            'difficulty',
            'sample_input1', 
            'sample_output1',
            'sample_input2', 
            'sample_output2',
            'test_case_input_1', 
            'test_case_output_1',
            'test_case_input_2', 
            'test_case_output_2',
            # Add more test case fields as needed
        ]
        labels = {
            'sample_input1': 'Sample Input1',
            'sample_output1': 'Sample Output1',
            'sample_input2': 'Sample Input2',
            'sample_output2': 'Sample Output2',
            'test_case_input_1': 'Test Case Input 1',
            'test_case_output_1': 'Test Case Output 1',
            'test_case_input_2': 'Test Case Input 2',
            'test_case_output_2': 'Test Case Output 2',
            # Update labels for additional test cases as required
        }
