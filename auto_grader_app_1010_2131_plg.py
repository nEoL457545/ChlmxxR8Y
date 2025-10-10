# 代码生成时间: 2025-10-10 21:31:37
import os
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.exceptions import ValidationError

# Models
class Submission(models.Model):
    """
    Model representing a student's submission.
    """
    student_name = models.CharField(max_length=100)
    code_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student_name}'s submission at {self.submitted_at}"

# Views
@method_decorator(csrf_exempt, name='dispatch')
class GradeSubmission(View):
    """
    View to handle submission and grading of code.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles POST request to grade submissions.
        """
        try:
            student_name = request.POST.get('student_name')
            code_file = request.FILES.get('code_file')

            # Validate input
            if not student_name or not code_file:
                raise ValidationError('Student name and code file are required.')

            # Save the submission
            submission = Submission.objects.create(
                student_name=student_name,
                code_file=code_file
            )

            # Grade the submission
            grade = self.grade_submission(submission)

            # Return the grade
            return JsonResponse({'grade': grade})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while grading.'}, status=500)

    def grade_submission(self, submission):
        """
        Placeholder for the grading logic.
        This method should be implemented to grade the submission.
        """
        # For demonstration purposes, returning a static grade
        return 'A'

# URLs
urlpatterns = [
    path('grade/', GradeSubmission.as_view(), name='grade_submission'),
]
