from django.shortcuts import render,redirect,get_object_or_404
from .models import Course,Batch
from .models import Notice
from .models import Trainer
from .models import Add_Student_table
from .models import Fee


# Create your views here.


def Dashboard(request):

    students_count = Add_Student_table.objects.count()
    trainers_count = Trainer.objects.count()
    courses_count = Course.objects.count()
    batches_count = Batch.objects.count()
    notices_count = Notice.objects.count()
    attendance_count = Attendance.objects.count()

    context = {
        'students': students_count,
        'trainers': trainers_count,
        'courses': courses_count,
        'batches': batches_count,
        'notices': notices_count,
        'attendance': attendance_count
    }

    return render(request, 'dashboard.html', context)

def Homepage(request):
    return render(request, 'home.html')

# Add Batch
def add_batch(request):

    courses = Course.objects.all()
    trainers = Trainer.objects.all()

    if request.method == "POST":

        batch_name = request.POST.get('batch_name')
       
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        timing = request.POST.get('timing')

        Batch.objects.create(
            batch_name=batch_name,
            
            start_date=start_date,
            end_date=end_date,
            timing=timing
        )

    context = {
        'courses': courses,
        'trainers': trainers
    }

    return render(request, 'add_batch.html', context)

# View All Batches
def view_all_batches(request):

    batches = Batch.objects.all()

    return render(request, 'view_all_batches.html', {'batches': batches})


def Add_course(request):
    batches = Batch.objects.all()
    trainers = Trainer.objects.all()  
 


    if request.method == "POST":

        Course.objects.create(
            batch_name = request.POST.get('batch_name'),

            course_name = request.POST.get('course_name'),
            course_code = request.POST.get('course_code'),
            trainer_name = request.POST.get('trainer_name'),
            start_date = request.POST.get('start_date'),
            duration = request.POST.get('duration'),
            # fees = request.POST.get('fees'),
            description = request.POST.get('description'),
            course_image = request.FILES.get('course_image')
        )

        return redirect('view_all_course')

    return render(request, 'add_course.html', {
        'trainers': trainers,'batches': batches
    })

def View_all_course(request):

    courses = Course.objects.all()

    return render(request, 'view_all_course.html', {
        'courses': courses,
    })


def Delete_course(request, id):

    course = get_object_or_404(Course, id=id)
    course.delete()

    return redirect('view_all_course')

def Update_course(request, id):

    course = get_object_or_404(Course, id=id)

    if request.method == "POST":

        course.course_name = request.POST.get('course_name')
        course.course_code = request.POST.get('course_code')
        course.trainer_name = request.POST.get('trainer_name')
        course.start_date = request.POST.get('start_date')
        course.duration = request.POST.get('duration')
        course.fees = request.POST.get('fees')

        if request.FILES.get('course_image'):
            course.course_image = request.FILES.get('course_image')

        course.save()

        return redirect('view_all_course')

    return render(request, 'update_course.html', {'course': course})

def toggle_course_status(request, id):
    course = get_object_or_404(Course, id=id)

    # True -> False , False -> True
    course.status = not course.status
    course.save()

    return redirect('view_all_course')




# Delete Batch
def delete_batch(request, id):

    batch = get_object_or_404(Batch, id=id)
    batch.delete()

    return redirect('view_all_batches')


# Toggle Status
def toggle_batch_status(request, id):

    batch = get_object_or_404(Batch, id=id)

    batch.status = not batch.status
    batch.save()

    return redirect('view_all_batches')

# def Homepage(request):
#     return render(request,'home.html')







def Add_notice(request):

    batches = Batch.objects.all()
    selected_batch = request.GET.get('batch')
    

    if selected_batch:
        # 🔥 MAIN FILTER (IMPORTANT)
        courses = Course.objects.filter(batch_name=selected_batch)
    else:
        courses = Course.objects.none()

    if request.method == 'POST':
        title = request.POST.get('notice_title')
        notice_no = request.POST.get('notice_no')
        description = request.POST.get('notice_description')

        batch = request.POST.get('batch')
        course = request.POST.get('course')

        image = request.FILES.get('image')
        pdf = request.FILES.get('pdf')

        Notice.objects.create(
            batch_name=batch,
            course_name=course,
            notice_title=title,
            notice_description=description,
            image=image,
            notice_no=notice_no,
            pdf=pdf
            
        )

        return redirect('add_notice')
    notices = Notice.objects.all().order_by('-created_at')

    return render(request, 'add_notice.html', {
        'batches': batches,
        'courses': courses,
        'selected_batch': selected_batch
    })

def View_all_notice(request):
    status_filter = request.GET.get('status')

    if status_filter == 'active':
        notices = Notice.objects.filter(status=True)

    elif status_filter == 'inactive':
        notices = Notice.objects.filter(status=False)

    else:
        notices = Notice.objects.all()

    return render(request, 'view_all_notice.html', {'notices': notices})


def update_notice(request, id):
    notice = get_object_or_404(Notice, id=id)

    if request.method == "POST":
        notice.notice_title = request.POST.get('notice_title')
        notice.notice_description = request.POST.get('notice_description')
        notice.status = request.POST.get('status') == "on"
        notice.save()
        return redirect('view_all_notice')

    return render(request, 'update_notice.html', {'notice': notice})



def delete_notice(request, notice_id):  # Change 'id' to 'notice_id'
    # Use filter().delete() to avoid the "MultipleObjectsReturned" error from earlier
    Notice.objects.filter(id=notice_id).delete() 
    return redirect('view_all_notice')


#  DELETE TASK
# def delete_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     task.delete()
#     return redirect('view_task')


def toggle_notice(request, id):
    notice = Notice.objects.get(id=id)
    notice.status = not notice.status
    notice.save()
    return redirect('view_all_notice')



def Add_trainer(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        name = request.POST.get('name')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        assigned_course = request.POST.get('assigned_course')
        salary = request.POST.get('salary')

        Trainer.objects.create(
            photo=photo,
            name=name,
            qualification=qualification,
            experience=experience,
            email=email,
            phone=phone,
            assigned_course=assigned_course,
            salary=salary
        )

        return redirect('add_trainer')

    return render(request, 'add_trainer.html')





def view_all_trainer(request):
    trainers = Trainer.objects.all()
    return render(request, 'view_all_trainer.html', {'trainers': trainers})


def edit_trainer(request, id):
    trainer = get_object_or_404(Trainer, id=id)

    if request.method == "POST":
        trainer.name = request.POST.get('name')
        trainer.qualification = request.POST.get('qualification')
        trainer.experience = request.POST.get('experience')
        trainer.email = request.POST.get('email')
        trainer.phone = request.POST.get('phone')
        trainer.assigned_course = request.POST.get('assigned_course')
        trainer.salary = request.POST.get('salary')

        if request.FILES.get('photo'):
            trainer.photo = request.FILES.get('photo')

        trainer.save()
        return redirect('view_all_trainer')

    return render(request, 'add_trainer.html', {'trainer': trainer})


def delete_trainer(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    trainer.delete()
    return redirect('view_all_trainer')

def update_trainer(request, id):
    trainer = get_object_or_404(Trainer, id=id)

    if request.method == "POST":
        trainer.name = request.POST.get('name')
        trainer.qualification = request.POST.get('qualification')
        trainer.experience = request.POST.get('experience')
        trainer.email = request.POST.get('email')
        trainer.phone = request.POST.get('phone')
        trainer.assigned_course = request.POST.get('assigned_course')
        trainer.salary = request.POST.get('salary')

        if request.FILES.get('photo'):
            trainer.photo = request.FILES.get('photo')

        trainer.save()
        return redirect('view_all_trainer')

    return render(request, 'update_trainer.html', {'trainer': trainer})

from django.shortcuts import render, redirect
from .models import Course, Batch, Add_Student_table

def Add_Student(request):

    # 🔥 dropdown साठी data
    courses = Course.objects.all()
    batches = Batch.objects.all()
    fees = Fee.objects.all()

    if request.method == "POST":

        photo = request.FILES.get('student_photo')
        name = request.POST.get('student_name')
        gender = request.POST.get('student_gender')
        email = request.POST.get('student_email')
        address = request.POST.get('student_address')

        batch_name = request.POST.get('batch_name')   # 🔥 NEW
        course_name = request.POST.get('student_course_name')

        number = request.POST.get('student_number')
        dob = request.POST.get('student_dob')
        parent_name = request.POST.get('parent_name')
        aadhar_no = request.POST.get('aadhar_no')
        admission_date = request.POST.get('admission_date')

        student_status = request.POST.get('student_status')
        fee_status = request.POST.get('fee_status')

        username = request.POST.get("username")
        password = request.POST.get("password")
        # ✅ SAVE DATA
        Add_Student_table.objects.create(
            photo=photo,
            name=name,
            gender=gender,
            email=email,
            address=address,
            course_name=course_name,
            batch_name=batch_name,
            number=number,
            dob=dob,
            parent_name=parent_name,
            aadhar_no=aadhar_no,
            admission_date=admission_date,
            student_status=student_status,
           
            fee_status=fee_status,
            username=username,
            password=password
        )

        return redirect('view_all_student')

    return render(request, 'add_student.html', {
        'courses': courses,
        'batches': batches,
        'fees': fees
    })    
def Toggle_Status(request, id):
    student = get_object_or_404(Add_Student_table, id=id)

    if student.student_status == "Active":
        student.student_status = "Inactive"
    else:
        student.student_status = "Active"

    student.save()

    return redirect('view_all_student')

def Edit_Student(request, id):

    student = Add_Student_table.objects.get(id=id)

    if request.method == "POST":

        if request.FILES.get('student_photo'):
            student.photo = request.FILES.get('student_photo')

        student.name = request.POST.get('student_name')
        student.gender = request.POST.get('student_gender')
        student.email = request.POST.get('student_email')
        student.address = request.POST.get('student_address')
        student.course_name = request.POST.get('student_course_name')
        student.number = request.POST.get('student_number')

        student.dob = request.POST.get("student_dob") or None
        student.admission_date = request.POST.get("admission_date") or None

        student.parent_name = request.POST.get('parent_name')
        student.aadhar_no = request.POST.get('aadhar_no')
        student.batch_name = request.POST.get('batch_name')
        student.student_status = request.POST.get('student_status')
        student.fee_status = request.POST.get('fee_status')

        
       
        student.save()

        return redirect('view_all_student')

    return render(request, 'edit_student.html', {'student': student})

def Delete_Student(request, id):
    student = Add_Student_table.objects.get(id=id)
    student.delete()
    return redirect('view_all_student')


def View_all_student(request):
    students = Add_Student_table.objects.all()
    return render(request, 'view_all_student.html',{'students':students})




from django.contrib import messages
from .models import Ragistar_tbl


# ================= HOME PAGE =================
def Home_page(request):
    return render(request, 'student_home_1.html')


# ================= STUDENT SECTION =================



# ================= STUDENT LOGIN SECTION =================

def Stlogin_page_view(request):
    if request.method == "POST":
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')

        try:
            student = Add_Student_table.objects.get(username=u_name, password=p_word)

            request.session['student_id'] = student.id
            
            return redirect('student_home_1', id=student.id)
        
        except Add_Student_table.DoesNotExist:
            return render(request, 'student_login.html', {'error': 'Invalid Username or Password'})

    return render(request, 'student_login.html')

from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Sum


from .models import StudentFee

from .models import Notice
from .models import TaskReport_1


from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import TaskReport_1, StudentFee, Notice, Task, Add_Student_table

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .models import *

def student_home_1(request, id):

    # ✅ Session check
    session_student_id = request.session.get('student_id')
    if str(session_student_id) != str(id):
        return redirect('student_login')

    # ✅ Student object
    student = get_object_or_404(Add_Student_table, id=id)


    attendance = Attendance.objects.filter(student=student).order_by('-date')[:10]

    # ✅ Submitted task IDs (HIDE logic)
    submitted_task_ids = TaskReport_1.objects.filter(
        student_name=student
    ).values_list('task_id', flat=True)

    # ✅ ONLY not submitted tasks show
    tasks = Task.objects.filter(
        batch_name=student.batch_name,
        course_name=student.course_name
    ).exclude(id__in=submitted_task_ids).order_by('-task_no')

    # ✅ Reports (for result / history)
    reports = TaskReport_1.objects.filter(student_name=student)

    # ✅ Fee logic
    fee_history = StudentFee.objects.filter(
        student_name=student.name
    ).order_by('-id')

    total_paid = fee_history.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    last_record = fee_history.first()

    # चुकीचे:
# my_attendance = Attendance.objects.filter(student=student_obj).order_items('-date')

# बरोबर (हा कोड वापरा):
    present_count = Attendance.objects.filter(student=student, status="Present").count()
    
    remaining_fee = last_record.remaining_fee if last_record else 0
    total_fee = last_record.total_fee if last_record else 0

    # ✅ Notices
    notices = Notice.objects.filter(
        batch_name=student.batch_name,
        course_name=student.course_name,
        status=True
    ).order_by('-created_at')
    exam_given = ExamResult.objects.filter(student=student).exists()
    # ✅ Final context
    context = {
        'student': student,
        'tasks': tasks,
        'exam_given': exam_given,         # 🔥 hidden tasks applied
        'reports': reports,
        'attendance': attendance,
        'notices': notices,
        'total_fee': total_fee,
        'paid_fee': total_paid,
        'present_count': present_count,

        'remaining_fee': remaining_fee,
        'fee_history': fee_history,
    }

    return render(request, 'student_home_1.html', context)

def Strag_page_view(request):
    if request.method == "POST":

        name = request.POST.get('name')
        surname = request.POST.get('surname')
        mobile = request.POST.get('mobile')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Ragistar_tbl.objects.filter(username=username).exists():

            messages.error(request, f"Username '{username}' already exists.")
            return redirect('strag')

        Ragistar_tbl.objects.create(

            name=name,
            surname=surname,
            mobile=mobile,
            username=username,
            password=password,
            added_by_admin=False

        )

        messages.success(request, "Student Registered Successfully")

        return redirect('stlogin')

    return render(request, 'student_registration.html')


# Student Home
def Student_Home(request):

    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('stlogin')

    student = get_object_or_404(Ragistar_tbl, id=student_id)

    return render(request, 'student_home.html', {'student': student})


# Student Logout
def Student_Logout(request):

    request.session.flush()

    return redirect('stlogin')


# ================= ADMIN SECTION =================

# Admin Login
def Admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "saurabhdhage20114@gmail.com" and password == "Saurabh@123":

            request.session['admin'] = username

            return redirect('dashboard')

        else:

            messages.error(request, "Invalid Admin Credentials")

    return render(request, 'admin_login.html')


# Admin Dashboard
def Dashbord(request):

    if not request.session.get('admin'):
        return redirect('admin_login')

    return render(request, 'dashbord.html')



def Admin_Logout(request):
    request.session.flush()
    return redirect('admin_login')


def Homepage2(request):
    return render(request,'index.html')


def Add_fee(request):
    batches = Batch.objects.all()
    selected_batch = request.GET.get('batch')

    if selected_batch:
        courses = Course.objects.filter(batch_name=selected_batch)
    else:
        courses = Course.objects.none()

    if request.method == 'POST':
        batch = request.POST.get('batch_name')
        course = request.POST.get('course_name')
        fees_raw = request.POST.get('fees')

        # --- THE FIX ---
        try:
            # This converts '1000' to 1000. 
            # If it gets 'exit', it jumps straight to the 'except' block.
            final_fees = int(fees_raw) 
        except (ValueError, TypeError):
            # If data is 'exit' or empty, we set it to 0 so the database doesn't crash
            final_fees = 0 
        # ----------------

        Fee.objects.create(
            batch_name=batch,
            course_name=course,
            total_fees=final_fees
        )

        return redirect('add_fee')

    return render(request, 'add_fee.html', {
        'batches': batches,
        'courses': courses,
        'selected_batch': selected_batch
    })

# def View_all_fee(request):
#     # Fetch all records to show in the table
#     fees_records = Add_Student_table.objects.all()
#     return render(request, 'view_all_fee.html', {'fees_records': fees_records})

def View_all_fee(request):
    fees_records = Fee.objects.all()   
    return render(request, 'view_all_fee.html', {'fees_records': fees_records})






from django.shortcuts import render, redirect, get_object_or_404
from .models import Fee, Batch, Course  

# --- Delete Fee Record ---
def delete_fee(request, id):
  
    record = get_object_or_404(Fee, id=id) 
    record.delete()
    return redirect('view_all_fee')

# --- Edit Fee Record ---
def edit_fee(request, id):
    # येथे सुद्धा Fee मॉडेल वापरा
    record = get_object_or_404(Fee, id=id) 
    courses = Course.objects.all()
    batches = Batch.objects.all()

    if request.method == "POST":
        record.course_name = request.POST.get('course_name')
        record.batch_name = request.POST.get('batch_name')
        record.total_fees = request.POST.get('fees')
        record.save()
        return redirect('view_all_fee')

    return render(request, 'add_fee.html', {
        'record': record, 
        'courses': courses, 
        'batches': batches,
    })

from .models import Task
from django.shortcuts import render, redirect


def add_taskss(request):
    batches = Batch.objects.all()
    
    # 1. Get the batch from the URL (for filtering the course dropdown)
    selected_batch = request.GET.get('batch_name') 

    if selected_batch:
        courses = Course.objects.filter(batch_name=selected_batch)
    else:
        courses = Course.objects.none()

    if request.method == "POST":
        # 2. Use 'batch_name' here to match the HTML select name
        batch = request.POST.get('batch_name') 
        course = request.POST.get('course')
        task_no = request.POST.get('task_no')
        task_title = request.POST.get('task_title')
        task_definition = request.POST.get('task_definition')
        image = request.FILES.get('image')
        pdf = request.FILES.get('pdf')

        # 3. Create the task (Make sure 'batch' is not None)
        if batch:
            Task.objects.create(
                batch_name=batch,
                course_name=course,
                task_no=task_no,
                task_title=task_title,
                task_definition=task_definition,
                image=image,
                pdf=pdf
            )
            return redirect('view_task') # Redirect to the view page
        
    return render(request, 'add_task.html', {
        'courses': courses,
        'batches': batches,
        'selected_batch': selected_batch
    })
    


def view_all_task(request):
    tasks = Task.objects.all()
    return render(request, 'view_task.html', {'tasks': tasks})





from django.shortcuts import render, redirect, get_object_or_404

# DELETE TASK
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('view_task')

# EDIT/UPDATE TASK
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    batches = Batch.objects.all()
    
    # Filtering logic for the course dropdown
    selected_batch = request.GET.get('batch_name') or task.batch_name
    courses = Course.objects.filter(batch_name=selected_batch)

    if request.method == "POST":
        task.batch_name = request.POST.get('batch_name')
        task.course_name = request.POST.get('course')
        task.task_no = request.POST.get('task_no')
        task.task_title = request.POST.get('task_title')
        task.task_definition = request.POST.get('task_definition')
        
        # Only update files if new ones are uploaded
        if request.FILES.get('image'):
            task.image = request.FILES.get('image')
        if request.FILES.get('pdf'):
            task.pdf = request.FILES.get('pdf')

        task.save()
        return redirect('view_task')

    return render(request, 'edit_task.html', {
        'task': task,
        'batches': batches,
        'courses': courses,
        'selected_batch': selected_batch
    })

from .models import Batch,Course,Add_Student_table,StudentFee

from  .models import StudentFee








from django.shortcuts import render, redirect
def add_student_fee(request):
    batches = Batch.objects.all()
    selected_batch = request.GET.get('batch_name')
    selected_course = request.GET.get('course_name')
    selected_student = request.GET.get('student_name')

    courses = Course.objects.none()
    students = Add_Student_table.objects.none()
    auto_total_fee = 0

    if selected_batch:
        courses = Course.objects.filter(batch_name=selected_batch)

    if selected_batch and selected_course:
        students = Add_Student_table.objects.filter(batch_name=selected_batch, course_name=selected_course)
        
        # जर विद्यार्थी निवडला असेल, तर डेटाबेसमध्ये त्याची जुनी 'Remaining Fee' तपासा
        if selected_student:
            from .models import StudentFee # तुमच्या मॉडेलचे नाव तपासा
            last_record = StudentFee.objects.filter(student_name=selected_student, course_name=selected_course).order_by('-id').first()
            
            if last_record:
                auto_total_fee = last_record.remaining_fee
            else:
                # जर नवीन विद्यार्थी असेल तर कोर्सची मूळ फी आणा
                fee_obj = Fee.objects.filter(course_name=selected_course, batch_name=selected_batch).first()
                auto_total_fee = fee_obj.total_fees if fee_obj else 0
        else:
            # विद्यार्थी निवडण्यापूर्वी कोर्स फी दाखवा
            fee_obj = Fee.objects.filter(course_name=selected_course, batch_name=selected_batch).first()
            auto_total_fee = fee_obj.total_fees if fee_obj else 0

    if request.method == "POST":
        # डेटा सेव्ह करण्याचे लॉजिक
        StudentFee.objects.create(
            student_name=request.POST.get('student_name'),
            batch_name=request.POST.get('batch_name'),
            course_name=request.POST.get('course_name'),
            total_fee=float(request.POST.get('total_fee')),
            paid_amount=float(request.POST.get('paid_amount'))
        )
        return redirect('view_all_student_fees')

    return render(request, 'add_student_fee.html', {
        'batches': batches, 'courses': courses, 'students': students,
        'selected_batch': selected_batch, 'selected_course': selected_course,
        'selected_student': selected_student, 'auto_total_fee': auto_total_fee,
    })


def view_all_student_fees(request):
    # Fetch all records from the StudentFee model
    fees_records = StudentFee.objects.all().order_by('-id') # Shows latest records first
    
    return render(request, 'view_all_student_fees.html', {
        'fees_records': fees_records
    })




from .models import TaskReport

def add_task_report(request):
    batches = Batch.objects.all()
    selected_batch = request.GET.get('batch_name')
    selected_course = request.GET.get('course_name')
    selected_student = request.GET.get('student_name')

    courses = Course.objects.none()
    students = Add_Student_table.objects.none()

    if selected_batch:
        courses = Course.objects.filter(batch_name=selected_batch)

    if selected_batch and selected_course:
        students = Add_Student_table.objects.filter(batch_name=selected_batch, course_name=selected_course)

    if request.method == "POST":
       
        TaskReport.objects.create(
            student_name=request.POST.get('student_name'),
            batch_name=request.POST.get('batch_name'),
            course_name=request.POST.get('course_name'),
            task_no=request.POST.get('task_no'),
            status=request.POST.get('status'),
            remark=request.POST.get('remark'),
            date=request.POST.get('date')
        )
        return redirect('view_task_reports') 

    return render(request, 'add_task_report.html', {
        'batches': batches,
        'courses': courses,
        'students': students,
        'selected_batch': selected_batch,
        'selected_course': selected_course,
        'selected_student': selected_student,
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import TaskReport_1, Task, Add_Student_table

def submit_task(request, id):
    
    student_id = request.session.get('student_id')
    
    
    student_id = request.session.get('student_id')
    student_obj = get_object_or_404(Add_Student_table, id=student_id)
    student = get_object_or_404(Add_Student_table, id=student_id)
    task = get_object_or_404(Task, id=id)

    if request.method == "POST":
        # Form madhun baki data ghene
        task_answer = request.POST.get('task_answer')
        file = request.FILES.get('task_file')
        status = request.POST.get('status', 'Complete') 
        submission_date = request.POST.get('submission_date')

        # 3. Data Save kara
        TaskReport_1.objects.create(
            student_name_id = student.id,       
            task_title=task.task_title,  
            task_id=task.id,            
            submission_date=submission_date,
            task_answer=task_answer,
            file=file,
            status=status
        )

        return redirect('student_home_1', id=student.id)

    return render(request, 'submit_task.html', {'task': task, 'student': student})


from .models import Task

def select_students(request):

    batches = Batch.objects.all()

    selected_batch = request.GET.get('batch_name')
    selected_course = request.GET.get('course_name')

    courses = Course.objects.none()
    reports = TaskReport_1.objects.all()
    students = Add_Student_table.objects.none()
    tasks = Task.objects.none()   

    if selected_batch:
        courses = Course.objects.filter(batch_name=selected_batch)

    # Batch + Course → Students + Tasks
    if selected_batch and selected_course:
        students = Add_Student_table.objects.filter(
            batch_name=selected_batch,
            course_name=selected_course
        )

        
        tasks = Task.objects.filter(
            batch_name=selected_batch,
            course_name=selected_course
        )

    return render(request, 'select_students.html', {
        'batches': batches,
        'reports': reports,
        'courses': courses,
        
        'students': students,
        'tasks': tasks,  
        'selected_batch': selected_batch,
        'selected_course': selected_course,
    })



from django.shortcuts import render, get_object_or_404, redirect
from .models import TaskReport_1

def evaluate_task(request, id):
    
    task = get_object_or_404(TaskReport_1, id=id)

    if request.method == "POST":
        task.marks = request.POST.get('marks')
        task.feedback = request.POST.get('feedback')
        task.status = request.POST.get('status')

        task.save()

        return redirect('dashboard')  

    return render(request, 'evaluate_task.html', {'task': task})













from .models import Attendance
from django.utils.timezone import now

def mark_attendance(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('stlogin')

    student = Add_Student_table.objects.get(id=student_id)
    today = now().date()

   
    if Attendance.objects.filter(student=student, date=today).exists():
        return render(request, 'mark_attendance.html', {
            'message': 'Attendance already marked today'
        })

    if request.method == "POST":
        status = request.POST.get('status')  

        Attendance.objects.create(
            student=student,
            status=status
        )

        return render(request, 'mark_attendance.html', {
            'message': 'Attendance marked successfully'
        })

    return render(request, 'mark_attendance.html')
from django.db import models
from .models import Attendance

from django.db.models import Count
from django.db.models.functions import TruncDate

def view_attendance(request):

    attendance = Attendance.objects.all().order_by('-date')

    total = attendance.count()
    present = attendance.filter(status="Present").count()
    absent = attendance.filter(status="Absent").count()

    
    daily_data = Attendance.objects.annotate(day=TruncDate('date')) \
        .values('day') \
        .annotate(
            present_count=Count('id', filter=models.Q(status="Present")),
            absent_count=Count('id', filter=models.Q(status="Absent"))
        ).order_by('day')

    labels = [str(i['day']) for i in daily_data]
    present_data = [i['present_count'] for i in daily_data]
    absent_data = [i['absent_count'] for i in daily_data]

    return render(request, 'view_attendance.html', {
        'attendance': attendance,
        'total': total,
        'present': present,
        'absent': absent,
        'labels': labels,
        'present_data': present_data,
        'absent_data': absent_data
    })























from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, ExamResult
from .forms import QuestionFormSet



# =====================================================================

def add_q_section(request):
    """
    Handles rendering the question formset to populate new test banks.
    Maps directly to URL path name 'add_q_section'.
    """
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST)
        if formset.is_valid():
            formset.save() 
            return redirect('view_all_q_sections')
    else:
        formset = QuestionFormSet(queryset=Question.objects.none()) 
    return render(request, 'admin_add_questions.html', {'formset': formset})


def view_all_q_sections(request):
    """
    Renders a comprehensive list of all exam results and performance metrics.
    Maps directly to URL path name 'view_all_q_sections'.
    """
    results = ExamResult.objects.all().order_by('-submitted_at')
    return render(request, 'admin_dashboard.html', {'results': results})


# =====================================================================
#  LEGACY BACKWARD-COMPATIBLE ADMIN PATHS
# =====================================================================

def admin_add_questions(request):
    """Fallback router keeping older paths valid."""
    return add_q_section(request)


def admin_dashboard(request):
    """Fallback router keeping older dashboard paths valid."""
    return view_all_q_sections(request)


def admin_add_questions(request):
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST)
        if formset.is_valid():
            formset.save() 
            return redirect('admin_dashboard')
    else:
        formset = QuestionFormSet(queryset=Question.objects.none()) 
    return render(request, 'admin_add_questions.html', {'formset': formset})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Question, ExamResult

def student_exam_page(request):

    # 🔥 LOGIN CHECK
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('index')   # login page

    student = Add_Student_table.objects.get(id=student_id)

    questions = Question.objects.all()[:50]
    total_q = questions.count()

    if request.method == 'POST':
        correct_count = 0

        for q in questions:
            selected_option = request.POST.get(f'question_{q.id}')

            if selected_option:
                if int(selected_option) == int(q.correct_option):
                    correct_count += 1

        percentage = (correct_count / total_q) * 100 if total_q > 0 else 0

        result = ExamResult.objects.create(
            student=student,
            total_questions=total_q,
            correct_answers=correct_count,
            score_percentage=percentage
        )

        return render(request, 'exam_success.html', {'result': result})

    return render(request, 'exam.html', {'questions': questions})
def admin_dashboard(request):
    results = ExamResult.objects.all().order_by('-submitted_at')
    return render(request, 'admin_dashboard.html', {'results': results})










def view_result(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('index')

    student = Add_Student_table.objects.get(id=student_id)

    result = ExamResult.objects.filter(student=student).last()

    return render(request, 'result.html', {'result':result})
















from django.http import JsonResponse
import json

def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            msg = data.get("message")

            return JsonResponse({
                "reply": "AI 🤖: " + msg
            })

        except Exception as e:
            return JsonResponse({
                "reply": "Error: " + str(e)
            })

    return JsonResponse({"reply": "Invalid request"})





    
# import random
# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from django.contrib.auth.models import User
# from django.core.mail import send_mail

# def login_view(request):
#      # Your file variable

#     if request.method == "POST":
#         email = request.POST.get("email")
#         otp = request.POST.get("otp")

#         # STEP 1: OTP send
#         if email and not otp:
#             otp_code = str(random.randint(1000, 9999))
#             request.session['otp'] = otp_code
#             request.session['email'] = email

#             send_mail(
#                 "Login OTP | EMP Manage Software",
#                 f"Welcome to EMP Manage Software from Saurabh Dhage (Owner).\n\nYour OTP is: {otp_code}",
#                 "saurabhdhage20114@gmail.com",
#                 [email],
#                 fail_silently=False,
#             )

#             return render(request, "login.html", {
#                 "email": email,
#                 "msg": "OTP sent to your email for file: ",
                
#             })

#         # STEP 2: OTP verify
#         elif otp:
#             session_otp = request.session.get("otp")
#             session_email = request.session.get("email")

#             if otp == session_otp:
#                 user, created = User.objects.get_or_create(
#                     username=session_email,
#                     email=session_email
#                 )
#                 login(request, user)
#                 return redirect("home")
#             else:
#                 return render(request, "login.html", {
#                     "error": "Invalid OTP. Please try again.",
#                     "email": session_email # Keep the email visible
#                 })
        
#         # FIX: If POST is sent but logic fails (e.g. empty fields)
#         else:
#             return render(request, "login.html", {"error": "Please enter your details."})

#     # STEP 3: Initial GET request (User first opens the page)
#     return render(request, "login.html")
        # ... rest of your OTP verification logic ...



import random
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.html import strip_tags  # 👈 हा नवीन import वरती नक्की जोडा

def mock_ai_domain_validator(email):
    """
    AI Filter Engine: Screens for valid educational/corporate domain health 
    and blocks malicious disposable temporary email services.
    """
    if not email or "@" not in email:
        return False, "Invalid syntax parsing structure."
        
    domain = email.split("@")[1].lower()
    disposable_domains = [
        "mailinator.com", "trashmail.com", "yopmail.com", 
        "10minutemail.com", "tempmail.com", "sharklasers.com"
    ]
    if domain in disposable_domains:
        return False, "Security Alert: Disposable temporary email domains are restricted."
    if not re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", domain):
        return False, "Domain analysis failure: Suspicious hostname configuration detected."
    return True, "Domain passed AI structural integrity verification check."


def login_view(request):
    current_file_context = "ACAD_STUDENT_MASTER_LOG.xlsx"

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        otp = request.POST.get("otp", "").strip()

        # STEP 1: Process and Dispatch Secure Email Token Authentication
        if email and not otp:
            is_valid_domain, message = mock_ai_domain_validator(email)
            if not is_valid_domain:
                return render(request, "login.html", {
                    "error": message,
                    "filename": current_file_context
                })

            # Generate 4-digit code
            otp_code = str(random.randint(1000, 9999))
            request.session['otp'] = otp_code
            request.session['email'] = email
            request.session.modified = True 

            # ==================== 🔒 इथे तुमचा नवीन प्रोग्रॅम आणि ईमेल कोड सुरू होतो ====================
            subject = "🔒 Secure Access Token | Academia AI Studio"
            
            html_message = f"""
            <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 550px; margin: 0 auto; padding: 30px; border: 1px solid #e5e7eb; border-radius: 12px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
                <div style="text-align: center; margin-bottom: 25px; border-bottom: 1px solid #f3f4f6; padding-bottom: 20px;">
                    <h2 style="color: #6366f1; margin: 0; font-size: 24px; font-weight: 700; letter-spacing: 0.5px;">ACADEMIA AI</h2>
                    <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 1px;">Student & Academy Management Suite</p>
                </div>
                <div style="color: #1f2937; line-height: 1.6; font-size: 15px;">
                    <p style="margin-top: 0;">Hello,</p>
                    <p>An access request was initialized for your security account profile to view data log asset: <span style="font-family: monospace; background-color: #f1f5f9; padding: 3px 6px; border-radius: 4px; color: #0f172a; font-weight: 600;">{current_file_context}</span>.</p>
                    <p style="color: #4b5563;">Please use the following verification code to secure your session workspace wrapper:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <div style="display: inline-block; background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color: #ffffff; font-size: 32px; font-weight: 700; letter-spacing: 6px; padding: 14px 40px; border-radius: 10px; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25); font-family: 'Courier New', Courier, monospace;">
                            {otp_code}
                        </div>
                        <p style="color: #9ca3af; font-size: 12px; margin-top: 10px; font-weight: 500;">(This security verification token is active and valid for 10 minutes)</p>
                    </div>
                    
                    <div style="background-color: #fff5f5; border-left: 4px solid #f56565; padding: 12px 16px; border-radius: 6px; margin-bottom: 25px;">
                        <p style="color: #9b2c2c; margin: 0; font-size: 13px; font-weight: 500;">
                            <strong>Security Alert:</strong> If you did not initialize this dynamic sign-in token cycle, please update your master credentials or contact support staff instantly.
                        </p>
                    </div>
                </div>
                <div style="margin-top: 35px; border-top: 1px solid #f3f4f6; padding-top: 20px; text-align: center; color: #9ca3af; font-size: 12px; line-height: 1.5;">
    
    <!-- 👤 तुमचा प्रोफाईल फोटो (इथे तुमची लाईव्ह इमेज लिंक टाका) -->
    <div style="margin-bottom: 12px;">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:&s" 
             alt="Saurabh Dhage" 
             style="width: 65px; height: 65px; border-radius: 50%; object-fit: cover; border: 2px solid #6366f1; padding: 2px; background-color: #ffffff; display: inline-block;">
    </div>
    

    <p style="margin: 0; font-weight: 600; color: #6b7280; font-size: 14px;">Saurabh Dhage</p>
    <p style="margin: 2px 0 0 0; font-style: italic; color: #818cf8; font-weight: 500;">Lead Operations Engineer & System Owner</p>
    <p style="margin: 12px 0 0 0; font-size: 11px; opacity: 0.7;">This is an automated system notification message. Please do not reply directly to this mail node network address.</p>
</div>
            </div>
            """
            
            plain_message = strip_tags(html_message)

            try:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email="saurabhdhage20114@gmail.com",
                    recipient_list=[email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                return render(request, "login.html", {
                    "email": email,
                    "msg": "AI Verification Engine approved domain. OTP dispatched safely for data asset: ",
                    "filename": current_file_context,
                    "show_otp": True
                })
            # ==================== 🔒 ईमेल सेंड करण्याचा कोड इथे संपतो ====================
                
            except Exception as e:
                return render(request, "login.html", {
                    "error": "Mailing Node Dispatch Error. Please verify server backend connectivity parameters.",
                    "filename": current_file_context
                })

        # STEP 2: Token Verification Checkpoint Logic Execution
        elif otp:
            session_otp = request.session.get("otp")
            session_email = request.session.get("email")

            if session_otp and otp == session_otp:
                del request.session['otp']
                user, created = User.objects.get_or_create(
                    username=session_email,
                    email=session_email
                )
                login(request, user)
                return redirect("index")
            else:
                return render(request, "login.html", {
                    "error": "Invalid token code entry verification sequence. Access denied.",
                    "email": session_email,
                    "show_otp": True,
                    "filename": current_file_context
                })
        else:
            return render(request, "login.html", {
                "error": "Missing form identity properties.",
                "filename": current_file_context
            })

    return render(request, "login.html", {
        "filename": current_file_context
    })
