from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    
    
    # Sample input/output 1
    sample_input1 = models.TextField()
    sample_output1 = models.TextField()
    
    # Sample input/output 2
    sample_input2 = models.TextField(blank=True, null=True)  # Optional
    sample_output2 = models.TextField(blank=True, null=True)  # Optional

    # Test cases
    test_case_input_1 = models.TextField(blank=True, null=True)
    test_case_output_1 = models.TextField(blank=True, null=True)
    test_case_input_2 = models.TextField(blank=True, null=True)
    test_case_output_2 = models.TextField(blank=True, null=True)
    # Add more as needed

    def get_test_cases(self):
        # Collect test cases as tuples
        test_cases = []
        if self.test_case_input_1 and self.test_case_output_1:
            test_cases.append((self.test_case_input_1, self.test_case_output_1))
        if self.test_case_input_2 and self.test_case_output_2:
            test_cases.append((self.test_case_input_2, self.test_case_output_2))
        # Add more if needed
        return test_cases

    def __str__(self):
        return self.title

class CodeSubmission(models.Model):
    language = models.CharField(max_length=100)
    code = models.TextField()
    input_data = models.TextField(null=True,blank=True)
    output_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)