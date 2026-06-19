
from django.contrib import admin
from django.urls import path
from student_management_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('/', views.Homepage2, name='index'),
    path('admin/', admin.site.urls),

     

   
    path('student_home_1/<int:id>/',views.student_home_1, name='student_home_1'),

    path('home/', views.Homepage, name='home'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('add_course/', views.Add_course, name='add_course'),
    path('view_all_course/', views.View_all_course, name='view_all_course'),
    path('delete_course/<int:id>/', views.Delete_course, name='delete_course'),
    path('update_course/<int:id>/', views.Update_course, name='update_course'),
    path('add_batch/', views.add_batch, name='add_batch'),
    path('delete_batch/<int:id>', views.delete_batch, name='delete_batch'),
    path('view_all_batches/', views.view_all_batches, name='view_all_batches'),
    path('add_notice/', views.Add_notice, name='add_notice'),
    path('view_all_notice/', views.View_all_notice, name='view_all_notice'),

    path('update_notice/<int:id>/', views.update_notice, name='update_notice'),
    path('delete_notice/<int:id>/', views.delete_notice, name='delete_notice'),
    path('toggle_notice/<int:id>/', views.toggle_notice, name='toggle_notice'),

    path('add_trainer/', views.Add_trainer, name='add_trainer'),
    path('view_all_trainer/', views.view_all_trainer, name='view_all_trainer'),
    path('update_trainer/<int:id>/', views.update_trainer, name='update_trainer'),
    path('edit_trainer/<int:id>/', views.edit_trainer, name='edit_trainer'),
    path('delete_trainer/<int:id>/', views.delete_trainer, name='delete_trainer'),
    path('toggle_course_status/<int:id>/',views.toggle_course_status,name='toggle_course_status'),
    path('toggle_batch_status/<int:id>/',views.toggle_batch_status,name='toggle_batch_status'),
    path('add_student',views.Add_Student,name='add_student'),
    path('view_all_student/', views.View_all_student, name='view_all_student'),
    path('edit_student/<int:id>/', views.Edit_Student, name='edit_student'),
    path('delete_student/<int:id>/', views.Delete_Student, name='delete_student'),
    path('toggle_status/<int:id>/', views.Toggle_Status, name='toggle_status'),
    path('add-fee/', views.Add_fee, name='add_fee'),
    path('view-all-fee/', views.View_all_fee, name='view_all_fee'),
    path('add-task-report/', views.add_task_report, name='add_task_report'),
    path('view-task/', views.view_all_task,name='view_task'),
    path('add-student-fee/', views.add_student_fee, name='add_student_fee'),
    path('view-all-student-fees/', views.view_all_student_fees, name='view_all_student_fees'),
    path('add_task/',views.add_taskss, name='add_task'),
    path('edit_task/<int:task_id>/',views.edit_task,name='edit_task'),
    path('delete_task/<int:task_id>/',views.delete_task,name='delete_task'),
    path('submit_task/<int:id>/', views.submit_task, name='submit_task'),
    path('edit-fee/<int:id>/', views.edit_fee, name='edit_fee'),
    path('select_students/', views.select_students, name='select_students'),
    path('delete-fee/<int:id>/', views.delete_fee, name='delete_fee'),
    path('evaluate_task/<int:id>/', views.evaluate_task, name='evaluate_task'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('view-attendance/', views.view_attendance, name='view_attendance'),


    # ================= QUESTIONS SECTIONS =================
    path('add_q_section/', views.add_q_section, name='add_q_section'),
    path('view_all_q_sections/', views.view_all_q_sections, name='view_all_q_sections'),
   





  


    # ================= STUDENT LOGIN =================
    path('stlogin/', views.Stlogin_page_view, name='stlogin'),

    # ================= STUDENT REGISTRATION =================
    path('student_registration/', views.Strag_page_view, name='student_registration'),
    path('strag/', views.Strag_page_view, name='strag'),

    # ================= STUDENT HOME =================
    path('student_home/', views.Student_Home, name='student_home'),

    # ================= STUDENT LOGOUT =================
    path('logout/', views.Student_Logout, name='logout'),

    # ================= ADMIN LOGIN =================
    path('admin_login/', views.Admin_login, name='admin_login'),

    # ================= ADMIN DASHBOARD =================
    path('dashbord/', views.Dashbord, name='dashbord'),

    # ================= ADMIN LOGOUT =================
    path('logout/', views.Admin_Logout, name='admin_logout'),
    


       
    


    path('admin-portal/add-questions/', views.admin_add_questions, name='admin_add_questions'),
    path('admin-portal/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('student_home_1/exam/', views.student_exam_page,name='student_exam_page'),
    path('result/', views.view_result, name='view_result'),
    path('chat/', views.chat, name='chat'),



    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




