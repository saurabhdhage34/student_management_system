from django.db import models
from django.utils import timezone

# Create your models here.

class Course(models.Model):
    batch_name = models.CharField(max_length=100)
    
    course_name = models.CharField(max_length=100)

    course_code = models.CharField(max_length=50)
    trainer_name = models.CharField(max_length=100)
    start_date = models.DateField()
    duration = models.IntegerField()
    # fees = models.IntegerField()
    description = models.TextField()
    course_image = models.ImageField(upload_to="courses/", null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name

class Batch(models.Model):

    batch_name = models.CharField(max_length=100)
    

    start_date = models.DateField()
    end_date = models.DateField()

    timing = models.CharField(max_length=50)  

    status = models.BooleanField(default=True)

    def __str__(self):
        return self.batch_name

   # ✅ add this

class Notice(models.Model):

    batch_name = models.CharField(max_length=100, default="General")
    course_name = models.CharField(max_length=100, default="General")

    notice_title = models.CharField(max_length=200)
    notice_description = models.TextField()
    notice_no=models.IntegerField(primary_key=True)

    image = models.ImageField(upload_to="notice_images/", null=True, blank=True)
    pdf = models.FileField(upload_to="notice_pdfs/", null=True, blank=True)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.notice_title
    

    

class Trainer(models.Model):
    photo = models.ImageField(upload_to='trainer_photos/')
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience = models.PositiveIntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    assigned_course = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Add_Student_table(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    photo = models.ImageField(upload_to="static/img",null=True,default=None)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    aadhar_no = models.CharField(max_length=12, null=True, blank=True)
    parent_name = models.CharField(max_length=100)
    admission_date = models.DateField(null=True, blank=True)
    batch_name = models.CharField(max_length=100)
    student_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    fee_status = models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)





# ================= STUDENT ADMIN FORM =================
# class Add_Student_admin_tbl(models.Model):
# class Add_Student_table(models.Model):
#     STATUS_CHOICES = (
#         ('Active', 'Active'),
#         ('Inactive', 'Inactive'),
#     )

#     photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
#     name = models.CharField(max_length=100)
#     gender = models.CharField(max_length=20)
#     email = models.EmailField()
#     address = models.CharField(max_length=200)
#     course_name = models.CharField(max_length=100)
#     number = models.CharField(max_length=15)
#     dob = models.DateField(null=True, blank=True)
#     aadhar_no = models.CharField(max_length=12, null=True, blank=True)
#     parent_name = models.CharField(max_length=100)
#     admission_date = models.DateField(null=True, blank=True)
#     batch_name = models.CharField(max_length=100)
#     student_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
#     fee_status = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name 


# ================ STUDENT REGISTER (Self Signup) ================
class Ragistar_tbl(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    status = models.BooleanField(default=True)  # Active/Inactive student
    added_by_admin = models.BooleanField(default=False)  # True if added by admin, False if self-registered

    def __str__(self):
        return self.username 




class Fee(models.Model):

    batch_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)

    total_fees = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)  # optional but useful

    def __str__(self):
        return self.course_name
    






class Task(models.Model):
    batch_name = models.CharField(max_length=100, default="General")
    course_name = models.CharField(max_length=100, default="General")
    task_no = models.IntegerField()  
    task_title = models.CharField(max_length=255)
    task_definition = models.TextField()

    image = models.ImageField(upload_to='task_images/', null=True, blank=True)
    pdf = models.FileField(upload_to='task_pdfs/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.task_no} - {self.task_title}"    

from django.db import models

class Attendance(models.Model):
    student = models.ForeignKey('Add_Student_table', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present','Present'),('Absent','Absent')], default='Present')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


from django.db import models

class StudentFee(models.Model):
    student_name = models.CharField(max_length=100)
    batch_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True) # Automatically adds date/time

    def save(self, *args, **kwargs):
        # Logic: Auto-calculate remaining fee before saving to DB
        self.remaining_fee = float(self.total_fee) - float(self.paid_amount)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_name} - {self.course_name}"
    




class TaskReport(models.Model):
    student_name = models.CharField(max_length=100)
    batch_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    task_no = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    remark = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.student_name} - {self.task_no}"
    




from django.db import models

class TaskReport_1(models.Model):
    student_name = models.ForeignKey('Add_Student_table', on_delete=models.CASCADE)
    task_title = models.CharField(max_length=100)
    task_id = models.IntegerField()
    submission_date = models.DateField()
    task_answer = models.TextField()
    file = models.FileField(upload_to='task_files/', null=True, blank=True)
    
    STATUS_CHOICES = [
        ('Complete', 'Complete'),
        ('Incomplete', 'Incomplete'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


    marks = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
      return str(self.student_name)



from django.shortcuts import render, redirect
from .models import TaskReport_1

def submit_task(request):
    if request.method == "POST":
        student_name = request.POST.get('student_name')
        task_title = request.POST.get('task_title')
        task_id = request.POST.get('task_id')
        submission_date = request.POST.get('submission_date')
        task_answer = request.POST.get('task_answer')
        file = request.FILES.get('task_file')
        status = request.POST.get('status')

        TaskReport_1.objects.create(
            student_name=student_name,
            task_title=task_title,
            task_id=task_id,
            submission_date=submission_date,
            task_answer=task_answer,
            file=file,
            status=status
        )

        return redirect('student_dashboard')  # किंवा success page

    return render(request, 'submit_task.html')




from django.db import models
from django.contrib.auth.models import User

# १. प्रश्नांचे मॉडेल
class Question(models.Model):
    question_text = models.CharField(max_length=500)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])

    def __str__(self):
        return self.question_text

# २. विद्यार्थ्यांच्या निकालाचे मॉडेल
class ExamResult(models.Model):
    student = models.ForeignKey(Add_Student_table, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    score_percentage = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.score_percentage}%"